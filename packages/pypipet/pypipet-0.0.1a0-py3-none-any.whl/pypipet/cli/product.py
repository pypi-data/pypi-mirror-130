import click 
from .cli import cli
from pipet.core.shop_conn.shop_connector import ShopConnector
from pipet.core.operations.utility import get_front_shop_id
from pipet.core.operations.frontshop import update_product_to_db
from pipet.core.operations.frontshop import update_variation_to_db
from pipet.core.operations.frontshop import update_destination_to_db
from pipet.core.operations.frontshop import update_product_at_front_shop, update_product_at_front_shop_bulk
from pipet.core.operations.frontshop import add_variation_to_shop
from pipet.core.operations.frontshop  import get_product_with_variations
from pipet.core.sql.query_interface import  search_exist
from pipet.core.operations.inventory import get_inventory_by_sku
from pipet.core.fileIO.file_loader import read_csv_file
from .utility import col2dict_update
from pprint import pprint

@cli.command()
@click.argument("action", type=click.Choice(['launch', 'deactivate', 'activate',
                                             'edit', 'show']))
@click.option("--shop", 
                help="frontshop name (in setting.shops)")
@click.option("--sku",
                help="if multiple sku provided, seperate with comma")
@click.option("-f", "--filename",
                help=" edit product attributes")
@click.option("--price",
                help=" price for lauching product to frontshop")
@click.option("--currency", default='USD',
                help=" currency for lauching product to frontshop")
@click.option('--skip-shop', is_flag=True, 
                        help="skip updating front shop for action edit.")
@click.pass_context
def product(ctx, action, shop, sku, price, currency, filename, skip_shop):
    """
    add/edit products (by sku or file)
    """
    click.echo('{} products at {}...'.format(action, shop))
    if sku is None and filename is None:
        click.echo('product identifier not found')
        return

    if sku is not None:
        sku = sku.split(',')

    project = ctx.obj['project']
    config = ctx.obj["config"]
    if config is None:
        click.secho('create project first',
                   fg='yellow')
        return

    project.initialize_project(config)
    table_classes = project.get_table_objects()
    sessionmaker = project.get_session_maker()
    session = sessionmaker()
    shop_config = project.config.get('shops').get(shop)

    if shop_config is None:
        click.secho('shop setting not found: {}'.format(shop),
                fg='yellow')
        session.close()
        return 
    
    shop_conn = ShopConnector(shop, 
                                shop_config['site_type'],
                                batch_size=shop_config['batch_size']) 
    shop_conn.set_shop_api(project.get_wp_api(shop))
    project.set_shop_connector(shop, shop_conn)
    get_front_shop_id(table_classes, session, shop_conn)

    if action == 'launch':
        if sku is None:
            click.echo('missing sku')
            return 
        if price is None:
            click.echo('missing price')
            return
        price = float(price)
        _launch_to_shop(session, table_classes, shop_conn, 
                                sku, price, currency,
                                project.config.get('attr_list'),
                                project.config.get('variation_attrs'))
    elif action == 'deactivate':
        if sku is None:
            click.echo('missing sku')
            return
        _change_status(session, table_classes, shop_conn, 
                                       sku, False, skip_shop)
    elif action == 'activate':
        if sku is None:
            click.echo('missing sku')
            return
        _change_status(session, table_classes, shop_conn, 
                                       sku, True, skip_shop)
    elif action == 'edit':
        if filename is None:
            click.echo('missing data file')
            return
        prods = _get_data_from_file(filename, action)
        click.echo('total product to edit {}'.format(len(prods)))
        _edit_product(session, table_classes, 
                      shop_conn, prods, skip_shop)
    elif action == 'show':
        if sku is None:
            click.echo('missing sku')
            return
        for s in sku:
            variation_info = get_product_with_variations(
                    table_classes, session, 
                    {'sku': s}, 
                     include_published=True, 
                     front_shop_id=shop_conn.front_shop_id)
            click.echo(variation_info)
    else:
        click.secho('action not supported: {}'.format(action),
                fg='yellow')
    
    session.close()

def _launch_to_shop(session, table_classes, shop_conn, skus, 
                                    price, currency, attrs, variation_attrs):
    for sku in skus:
        res = add_variation_to_shop(table_classes, session, shop_conn, 
                             sku, price, 
                             currency=currency,
                             attr_list = attrs,
                             variation_attrs=variation_attrs)
                             
        if res is not None:
            click.echo('sku {} add to shop'.format(sku))

def _change_status(session, table_classes, shop_conn, 
                        skus, status, skip_shop):
    for sku in skus:
        update_destination_to_db(table_classes.get('destination'),
                                     session,
                                     {'available': status, 'sku': sku},
                                     shop_conn.front_shop_id
                                     )
        
        if skip_shop is False:
            update_data = {'destination': {'available': status}}
            inv = 0
            if status:
                qty = get_inventory_by_sku(table_classes,
                                           session, sku)
                if qty: inv = qty

            update_data['variation'] ={
                'in_stock': inv
            }
            res = update_product_at_front_shop(
                                 table_classes, 
                                 session, 
                                 shop_conn, 
                                 update_data, 
                                 sku) 
            if res is None:
                click.echo('sku {} update error'.format(sku))

def _edit_product(session, table_classes, shop_conn, 
                                       products, skip_shop):
    for p in products:
        click.echo('updating sku {}'.format(p['variation']['sku']))
        if len(p['product']) > 0:
            if p['product'].get('id') is None:
                product_id = _get_product_id_by_sku(table_classes.get('variation'), 
                                                   session, p['variation']['sku'])
                if product_id is None:
                    click.echo('invalid sku, product not found')
                    return
                p['product']['id'] = product_id

            update_product_to_db(table_classes, 
                           session, 
                           p['product'])
        
        if len(p['variation']) > 0:
            update_variation_to_db(table_classes.get('variation'), 
                           session, 
                           p['variation'])
        
        if len(p['destination']) > 0:
            if p['destination'].get('sku') is None:
               click.secho('missing destination sku: {}'.format(p),
                fg='yellow')  
               return 
            update_destination_to_db(table_classes.get('destination'),
                                     session,
                                     p['destination'],
                                     shop_conn.front_shop_id
                                     )
        
    if skip_shop is False:
        click.echo('updating frontshop, total {}'.format(len(products)))
        update_product_at_front_shop_bulk(table_classes, session, 
                                shop_conn, products, batch_size=50)
        

def _get_data_from_file(filename, action):
    data = read_csv_file(filename)
    products = []
    #validation
    for i, row in data.iterrows():
        sku = str(row['variation.sku'])
        if sku is None or sku.strip() == '':
            click.secho('missing {}, stop processing'\
                                 .format(key), 
                        fg='yellow')
            return 

    for i, row in data.iterrows():
        sku = str(row['variation.sku'])
        p = col2dict_update(sku, row)
        # pprint(p)
        products.append(p)

    return products


def _get_product_id_by_sku(table_obj, session, sku):
    vari = search_exist(table_obj, session, {'sku': sku})
    if len(vari) > 0:
        return vari[0].product_id
