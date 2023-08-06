from pypipetcore.sql.query_interface import *
# from pypipetcore.shop_conn.gateway import *
from pypipetcore.model.product import Destination, Product, Variation
from .utility import get_front_shop_id
# from pypipetcore.transform.wc_to_model import parse_product
from copy import deepcopy

import logging
logger = logging.getLogger('__default__')

_DEBUG_ = True


def add_taxonomy_to_db(table_obj, session, shop_connector):
    categories = shop_connector.get_category_taxonomy(
                                            shop_connector.shop_type,
                                            shop_connector.shop_api
                                    )
    if categories:
        for cat in categories:
            db_insert_raw(table_obj, session, cat)
    else:
        logger.info('fetching taxonomy failed')


def load_products_from_shop(table_objs, session, shop_connector, 
                         start_from=1,  currency='USD'):
    start_page = start_from
    while True:
        logger.debug(f'page {start_page}')
        res = shop_connector.get_products_at_shop(
                                  shop_connector.shop_type, 
                                  shop_connector.shop_api, 
                                  batch_size=shop_connector.batch_size, 
                                  page=start_page,
                                  field_mapping=shop_connector.field_mapping)
        if res or len(res) == 0:
            logger.debug('done sync')
            break
        
        # if shop_connector.shop_type == 'wc':
        #     res =[parse_product(r, shop_connector.field_mapping)
        #               for r in res]
        add_product_to_db_bulk(table_objs, session, 
                                       shop_connector,res)
        start_page += 1
        if _DEBUG_ : break


def get_product_from_shop(table_objs, session, shop_connector, 
                                destination_product_id, currency='USD'):
    res = shop_connector.get_product_at_shop(
                                  shop_connector.shop_type, 
                                  shop_connector.shop_api, 
                                  destination_product_id,
                                  field_mapping=shop_connector.field_mapping
                                  )
    if res:
        return res

def add_product_to_db_bulk(table_objs, session, 
                            shop_connector,products:list, currency='USD'):
    for p in products:
        # logger.debug(p)
        if p is None: continue
        add_product_to_db(table_objs, session, p['product'])
        if p.get('destinations') is None \
                  or len(p['destinations']) == 0: 
            continue
        for dest in p['destinations']:
            #print(p['destinations'])
            add_destination_to_db(table_objs, 
                              session, 
                              shop_connector, 
                              dest,
                              currency=currency)

def add_product_to_db(table_objs, session, product_info: dict):
    if product_info is None: return 
    product = Product()
    #check category
    if product_info.get('category') is not None \
    and product_info.get('category').strip() != '' \
    and type(product_info.get('category')) is str:
        # print(product_info['product_name'])
        cat = _get_category_by_name(
                            table_objs.get('category'), 
                            session, 
                            product_info['category'])
        
        product_info.update(cat)
        del product_info['category']
    
    product.set_product(table_objs, product_info)
    
    return add_new_product(table_objs, session, product)


# def add_variation_to_db(table_objs, session, product_id: int,  variation_data: dict):
#     if variation_data.get('sku') is None:
#         logger.debug(f'missing {sku}')
#         return None

#     variation  = Variation() 
#     variation.set_variation(table_objs, variation_data)
    
#     #validate non-duplicate sku
#     exists = search_exist(table_objs.get(variation.__table_name__), 
#                           session, 
#                           {'sku': variation.sku})
#     if len(exists) > 0:
#         logger.debug(f'duplicate {variation.sku}')
#         return None

    
#     variation.set_attr('product_id', product_id)

#     res = add_to_db(table_objs.get(variation.__table_name__), 
#                      session, 
#                      variation)
#     if res is not None:
#         return variation


def add_destination_to_db(table_objs, session, shop_connector, 
                                        dest_data, currency='USD'):
    if shop_connector.front_shop_id is None:
        get_front_shop_id(table_objs, session, shop_connector)
    
    dest_data.update({
        'front_shop_id': shop_connector.front_shop_id,
        'is_current_price': True,
        'currency': currency
    })
    if dest_data.get('available') is None:
        dest_data['available'] = True 

    exist = is_exist_destination(table_objs.get('destination'), 
                                 session, dest_data)
    if exist:
        #update 
        #update_data(table_objs.get('destination'),  session,
                  #dest_data, {'id': dest_data['id']})
        pass
    else:
        #add new 
        dest = Destination()
        dest.set_destination(table_objs, dest_data)
        
        add_to_db(table_objs.get(dest.__table_name__), session, dest)

def is_exist_destination(table_obj, session, dest_data):
    dest = search_exist(table_obj, session,{
        'front_shop_id': dest_data['front_shop_id'],
        'sku': dest_data['sku']
    })
    if dest is None or len(dest) == 0:
        return False 
    else:
        for d in dest:
            if d.is_current_price:
                logger.debug(f'data exist id {d.id}')
                dest_data['id'] = d.id
                return True 
        return False



def get_product_info(table_objs, session, shop_connector, identifier=None,
                    sku=None, product_id=None, include_published=False,
                    include_category=False, **kwargs):
    params = None
    if identifier is not None:
        params = {'identifier': identifier}
    elif product_id is not None:
        params = {'product_id': product_id}
    elif sku is not None:
        params = {'sku': sku}
    if params is None:
        logger.debug('invalid product params')
        return 

    variation_info = get_product_with_variations(
                     table_objs, 
                     session, 
                     params, 
                     include_published=include_published,
                     include_category=include_category, 
                     front_shop_id=shop_connector.front_shop_id)

    return variation_info

def add_product_to_shop(table_objs, session, shop_connector, product_info, 
                                                    price=None, prices=None, **kwargs):
    if product_info.get('destinations'):
        logger.debug(f"has destinations, {product_info['destinations']}")
        return
    if (price is None and prices is None) or \
    (prices is not None and type(prices) is not dict):
        logger.debug('invalid product params')
        return 
    
    currency = kwargs.get('currency', 'USD')
    if product_info.get('variations') is None:
        #product without variations
        product_info['price'] = price
        product_info['currency'] = currency
        res = shop_connector.add_product_to_shop(shop_connector.shop_type, 
                                             shop_connector.shop_api, 
                                             product_info,
                                             attr_list=kwargs['attr_list']
                                             ) 
        if res is None:
            logger.debug(f"adding product to front shop failed {product_info['sku']}")
            return None
        #add to database
        res = add_json_to_db(table_objs.get('destination'), session, 
                    {
                        'sku': product_info['sku'],
                        'destination_product_id': res['id'],
                        'front_shop_id': shop_connector.front_shop_id,
                        'price': price,
                        'is_current_price': True,
                        'available': True,
                        'currency': currency
                    })
        return res
    else:
        for i, vari in enumerate(product_info['variations']):
            product_info['variations'][i]['currency'] = currency 
            if price: 
                product_info['variations'][i]['price'] = price 
            else:
                product_info['variations'][i]['price'] = \
                             prices.get(vari['sku'])
       
        assert kwargs.get('variation_attrs') is not None
        
        parent_id = None
        if kwargs.get('parent_id') is not None: parent_id = kwargs['parent_id']
        else: parent_id = product_info.get('parent_id')
        
        res = shop_connector.add_product_to_shop(shop_connector.shop_type, 
                                             shop_connector.shop_api, 
                                             product_info,
                                             parent_id=parent_id,
                                             **kwargs) # return dict to res
        
        if res is None or len(res) == 0:
            logger.debug(f"adding product to front shop failed {product_info['identifier']}")
            return None
   
        for i, vari in enumerate(product_info['variations']):
            if res.get(vari['sku']):
                if price is None:
                    price =  prices.get(vari['sku'])
                add_json_to_db(table_objs.get('destination'), session, 
                        {
                            'sku': vari['sku'],
                            'destination_product_id': res[vari['sku']]['id'],
                            'front_shop_id': shop_connector.front_shop_id,
                            'price': price,
                            'is_current_price': True,
                            'available': True,
                            'currency': currency,
                            'destination_parent_id': res[vari['sku']]['parent_id']
                        })
            else:
                logger.debug(f"missing results for sku {vari['sku']}")  
        return res  

def add_variation_to_shop(table_objs, session, shop_connector, 
                             sku:str, price:float, **kwargs):
    if shop_connector.front_shop_id is None:
        get_front_shop_id(table_objs, session, shop_connector)
    
    #transform data
    # variation_info = get_variation_info_by_sku(table_objs, session, sku, 
    #                  front_shop_id=shop_connector.front_shop_id)
    variation_info = get_product_with_variations(table_objs, session, 
                    {'sku': sku}, 
                     include_published=False, 
                     front_shop_id=shop_connector.front_shop_id)
    
    if variation_info is None:
        return 
    
    #check if it has been added but available flag need update
    if variation_info.get('set_available_flag'):
        #activate again 
        update_data(table_objs.get('destination'), 
                    session, 
                    {'available': True}, 
                    {'id': variation_info['destination_id'] })
        logger.info(f"variation sku {sku} reactivated")
            
        return 

    if variation_info.get('destinations') is not None:
        del variation_info['destinations']
    
    # if the sku is one of the variations of a product
    if variation_info.get('variations') and type(variation_info['variations']) is list:
        if variation_info.get('variations') is None or kwargs.get('ignore_variations'):
            variation_info.update(variation_info['variations'][0])
            del variation_info['variations']
        else:
            logger.info('add as variation')
            return add_product_to_shop(table_objs, session, shop_connector, 
                       variation_info, price=price, **kwargs)

    #add to frontshop 
    variation_info['price'] = price
    variation_info['currency'] = kwargs.get('currency', 'USD')
    res = shop_connector.add_product_to_shop(shop_connector.shop_type, 
                                             shop_connector.shop_api, 
                                             variation_info,
                                             **kwargs)
    # if res is None:
    #     #if exist, update
    #     res = _update_product_at_frontshop_by_sku(table_objs, session, 
    #                                       shop_connector, 
    #                                       sku, variation_info)
    #    
    if res is None:
        logger.debug(f'adding product to front shop failed {sku}')
        return None
    #add to database
    res = add_json_to_db(table_objs.get('destination'), session, 
                   {
                       'sku': sku,
                       'destination_product_id': res['id'],
                       'front_shop_id': shop_connector.front_shop_id,
                       'price': price,
                       'is_current_price': True,
                       'available': True,
                       'currency': variation_info['currency']
                   })
    return res


def get_cost_by_sku_from_db(table_obj, session, sku, params: dict={}):
    """apply when  skus have multiple suppliers"""
    params['sku'] = sku
    exists = search_exist(table_obj, session, params)
    if len(exists) > 0:
        prices = [inv.cost for inv in exists]
        return sum(prices)/len(prices)

def update_product_to_db(table_objs, session, product_info: dict):
    params = {}
    if product_info.get('id') is not None:
        params['id'] = product_info['id']
    elif product_info.get('identifier') is not None:
        params['identifier'] = product_info['identifier']
    else:
        logger.debug('missing product id and identifier')
        return 
    #check category
    if product_info.get('category') is not None \
    and product_info.get('category').strip() != '' \
    and type(product_info.get('category')) is str:
        # print(product_info['product_name'])
        cat = _get_category_by_name(
                            table_objs.get('category'), 
                            session, 
                            product_info['category'])
        
        product_info.update(cat)
        del product_info['category'] 
    
    if product_info.get('short_description'):
        product_info['short_description'] = product_info['short_description'][:1000]
    update_data(table_objs.get('product'), session, product_info, 
                params)    

def update_variation_to_db(table_obj, session, variation_info: dict):
    update_data(table_obj, session, variation_info, 
                {'sku': variation_info['sku']})     

def update_destination_to_db(table_obj, session, dest_info: dict, front_shop_id):
    params ={
        'sku': dest_info['sku'],
        'front_shop_id': front_shop_id,
        'is_current_price': True
    }
    if dest_info.get('price') is not None:
        destination = update_destination_price(table_obj, 
                                    session, dest_info['price'], params)
    
    update_data(table_obj, session, dest_info, params)  

def update_front_shop_price_bulk(table_objs, session, shop_connector, data: [dict]):
    if shop_connector.front_shop_id is None:
        get_front_shop_id(table_objs, session, shop_connector)
    for d in data:
        if d.get('price') is None: continue
        price = d['price']
        del d['price']

        d['front_shop_id'] = shop_connector.front_shop_id
        update_front_shop_price(table_objs, session, 
                            shop_connector, price, d)
    return data

def update_front_shop_price(table_objs, session, shop_connector, price:float, params:dict):
    if shop_connector.front_shop_id is None:
        get_front_shop_id(table_objs, session, shop_connector)
    #udpate database
    destination = update_destination_price(table_objs.get('destination'), 
                                              session, price, params)
    # print(destination.destination_product_id)
    if destination:
        #udpate front shop
        res = shop_connector.update_shop_product(
                            shop_connector.shop_type, 
                            shop_connector.shop_api,
                            {'price': price}, 
                            product_id=destination.destination_product_id,
                            parent_id=destination.destination_parent_id
                            )
        
        return res

def update_product_at_front_shop_bulk(table_objs, session, shop_connector, 
                                   data_list: list, batch_size=50,  **kwargs):
    update_batch = []
    

    for data in data_list:
        product_info = deepcopy({})
        product_id = None
        parent_id = None
        sku = data['variation']['sku']
        if data.get('destination') is None or \
        data['destination'].get('destination_product_id') is None:
            exists = search_exist(table_objs.get('destination'), 
                                session, 
                                {'sku': sku,
                                'front_shop_id': shop_connector.front_shop_id,
                                #    'available': True,
                                'is_current_price': True})
            if exists is None or len(exists) == 0:
                logger.info(f"variation sku {sku} not at shop or not available")
                continue
            product_id = exists[0].destination_product_id
            parent_id = exists[0].destination_parent_id
            if data['destination'].get('price') is None:
                data['destination']['price'] = exists[0].price
        else:
            product_id = data['destination']['destination_product_id']
            parent_id = data['destination'].get('destination_parent_id')
        
        product_info.update(data.get('product', {}))
        product_info.update(data.get('variation', {}))
        product_info.update(data.get('destination', {}))
        product_info['id'] = product_id
        product_info['parent_id'] = parent_id
        # print(product_info)
        update_batch.append(product_info)

        if len(update_batch) == batch_size:
            res_shop = shop_connector.update_shop_product_batch(
                    shop_connector.shop_type,
                    shop_connector.shop_api,
                    update_batch)
            # print(res_shop)
            #print(f'last update {product_id} ')
            update_batch = []

    if len(update_batch) > 0:
        res_shop = shop_connector.update_shop_product_batch(
                shop_connector.shop_type,
                shop_connector.shop_api,
                update_batch)
        # print(res_shop)
        print(f'last update {product_id} ')



def update_product_at_front_shop(table_objs, session, shop_connector, 
                                   data, sku, **kwargs):
    if shop_connector.front_shop_id is None:
        get_front_shop_id(table_objs, session, shop_connector)
    product_id = None
    parent_id = None
    product_info = {}
    if data.get('destination') is None or \
    data['destination'].get('destination_product_id') is None:
        exists = search_exist(table_objs.get('destination'), 
                              session, 
                              {'sku': sku,
                               'front_shop_id': shop_connector.front_shop_id,
                            #    'available': True,
                               'is_current_price': True})
        if exists is None or len(exists) == 0:
            logger.info(f"variation sku {sku} not at shop or not available")
            return None
        product_id = exists[0].destination_product_id
        parent_id = exists[0].destination_parent_id
        if data['destination'].get('price') is None:
            data['destination']['price'] = exists[0].price
    else:
        product_id = data['destination']['destination_product_id']
        parent_id = data['destination'].get('destination_parent_id')
    
    product_info.update(data.get('product', {}))
    product_info.update(data.get('variation', {}))
    product_info.update(data.get('destination', {}))
    #update frontshop 
    res = shop_connector.update_shop_product(
                                   shop_connector.shop_type, 
                                   shop_connector.shop_api, 
                                   product_info, 
                                   str(product_id), 
                                   parent_id=parent_id,
                                   **kwargs)
    logger.debug(f'{product_id}, {sku}')
    return res

def _get_category_by_name(table_obj, session, name):
    exists = search_exist(table_obj, session, {'category': name})
    if exists and len(exists) > 0:
        return {'category_id': exists[0].id}
    new_cat = add_json_to_db(table_obj, session, {'category': name})
    return {'category_id': new_cat['id']}

def _update_product_at_frontshop_by_sku(table_objs, session, shop_connector, 
                                          sku:str, data:dict):
    """search product at frontshop by sku, 
       if exist, update"""
    product_id = shop_connector.get_destination_product_id(
                                   shop_connector.shop_type, 
                                   shop_connector.shop_api,
                                   sku)
    if product_id is not None:
        return shop_connector.update_shop_product(shop_connector.shop_type, 
                                   shop_connector.shop_api, 
                                   data, 
                                   str(product_id),
                                   formated=True)