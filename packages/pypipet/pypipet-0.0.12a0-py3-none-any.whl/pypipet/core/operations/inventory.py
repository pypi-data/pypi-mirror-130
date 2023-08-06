
# from pypipet.core.sql.query import *
# from pypipet.core.shop_conn.gateway import update_shop_product, update_shop_product_batch
from pypipet.core.sql.query_interface import get_server_timestamp
from pypipet.core.sql.query_interface import add_json_to_db, search_exist
from pypipet.core.sql.query_interface import update_data, update_inventory,update_bulk
# from pypipet.core.sql.query_interface import get_inventory_update_after
from pypipet.core.sql.query_interface import get_variation_instock_qty
from pypipet.core.sql.query_interface import aggregate_inventory_qty
from pypipet.core.model.product import Inventory
from .utility import _object2dict
# from pypipet.core.sql.model2query import add_new_product_inventory
import logging
from datetime import datetime, timedelta

logger = logging.getLogger('__default__')

# def _get_params(data: dict, param_list:list):
#     params = {}
#     for param in param_list:
#         if data.get(param): params[param] = data[param]
#     return params

def get_supplier_id(table_obj, session, params):
    suppliers = search_exist(table_obj, 
                             session, 
                             params)
    if len(suppliers) >0:
        return suppliers[0].id 



def update_inventory_bulk(table_objs, session, invs:[dict], 
                                   batch_size=500, ignore_new=True):
    """ignore_new: if sku already in inventory table (updated before)"""
    if ignore_new:
        update_bulk(table_objs.get('inventory'), session, invs)
        update_instock_qty_db(table_objs, session, batch_size=batch_size)
        return invs
    
    sku_qty = {}
    for inv in invs:
        params ={
            'supplier_id': inv['supplier_id'],
        }
        if inv.get('sku') is not None:
            params['sku'] = inv['sku']
        if inv.get('supplier_item_id') is not None:
            params['supplier_item_id'] = inv['supplier_item_id']
        else:
            params['supplier_item_id'] = inv['sku']
        
        logger.debug(f"processing inv {inv}")
        update_inventory(table_objs.get('inventory'), session, inv, params)

        if sku_qty.get(inv['sku']) is None:
            sku_qty[inv['sku']] = {'sku': inv['sku'], 'in_stock': inv['qty']}
        else:
            sku_qty[inv['sku']]['in_stock'] += inv['qty']

    logger.debug(f"updating variation table")
    #update variation table
    update_bulk(table_objs.get('variation'), session, list(sku_qty.values()))
    return invs


def update_inventory_db_by_sku(table_objs, session, sku, inv:dict, params:dict ={}):
    """update inventory table with supplier info"""
    params['sku'] = sku
    if params.get('supplier_item_id') is None:
        params['supplier_item_id'] = sku

    if inv.get('qty') is None:
        inv['qty'] = 0
  
    update_inventory(table_objs.get('inventory'), session, inv, params)
    sku_inv = get_inventory_by_sku(table_objs, session, sku, by_supplier=True)
    qty = sum([item['qty'] for item in sku_inv])
    return update_data(table_objs.get('variation'), 
                        session, 
                        {'in_stock': qty}, 
                        {'sku': sku})

def update_instock_qty_db(table_objs, session, batch_size=50, 
                        params:dict={}, latest_hours=24):
    """aggregate instock from inventory table"""
    start_sku = None
    while True:
        logger.debug(f'start from {start_sku}')
        batch = aggregate_inventory_qty(table_objs, session, 
                       start_sku, params=params, 
                       batch_size=batch_size, latest_hours=latest_hours)

        if batch is None or len(batch) == 0:
            logger.debug('done')
            break
       
        update_bulk(table_objs.get('variation'), session, batch)
        # for rd in batch:
        #     update_data(table_objs.get('variation'), 
        #                 session, 
        #                 {'in_stock': rd['qty']}, 
        #                 {'sku': rd['sku']})

        start_sku = batch[-1]['sku']



def update_instock_front_shop(table_objs, session, shop_connector,
                                batch_size=50, params:dict={},latest_hours=24):
    """update all product at front shop stock number"""
    pid = None
    while True:
        res = get_variation_instock_qty(table_objs, session, 
                    pid, params=params, batch_size=batch_size, 
                    latest_hours=latest_hours)
        if res is None or len(res) == 0:
            logger.debug('done')
            break
        
        logger.debug(f"updating {res[0]['product_id']}, batch {len(res)}")
        pid = res[-1]['product_id']
        res_shop = shop_connector.update_shop_product_batch(
                    shop_connector.shop_type,
                    shop_connector.shop_api,
                    res)
        # print(f'last update {pid} ')

def update_instock_front_shop_by_sku(table_objs, session, shop_connector,
                                sku, params:dict={}):
    params.update({'sku': sku, 
                   'front_shop_id': shop_connector.front_shop_id})
    dest = search_exist(table_objs.get('destination'), session, params)
    if dest and len(dest) >0:
        dest = dest[0]
        qty = get_inventory_by_sku(table_objs, session, sku)
        if qty is None:
            logger.debug(f"invalid sku{sku}")
            return 
        res_shop = shop_connector.update_shop_product(
                        shop_connector.shop_type,
                        shop_connector.shop_api,
                        {
                        'qty': qty,
                        'sku': sku},
                        dest.destination_product_id,
                        parent_id=dest.destination_parent_id)
        logger.debug(f"updated product {dest.destination_product_id}")
    else:
        logger.debug(f"invalid sku {sku}")
        
def get_inventory_by_sku(table_objs, session, sku, by_supplier=False):
    if not by_supplier:
        inv = search_exist(table_objs.get('variation'), 
                                session, 
                                {'sku': sku})
        if len(inv) >0:
            return inv[0].in_stock 
    else:
        inv = search_exist(table_objs.get('inventory'), 
                                session, 
                                {'sku': sku})
        if len(inv) >0:
            return [_object2dict(r) for r in inv]

def match_variation_sku_by_upc(table_obj, session, invs:[dict]):
    for i, inv in enumerate(invs):
        if inv['upc'] is not None and inv.get('sku') is None:
            exist = search_exist(table_obj, session, {'upc': inv['upc']})
            if exist and len(exist) > 0:
                invs[i]['sku'] = exist[0].sku
    return invs
    
# def update_instock_qty_db_simple(table_objs, session, inv_list: [dict]):
#     """if do not inventory table, update by sku"""
#     for rd in inv_list:
#         if rd.get('sku') is not None and rd.get('qty') is not None:
#             update_data(table_objs.get('variation'), 
#                         session, 
#                         {'in_stock': rd['qty']}, 
#                         {'sku': rd['sku']})