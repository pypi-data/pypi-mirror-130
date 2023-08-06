
import pypipet.core.shop_conn.wc as wc
import pypipet.core.transform.wc_to_model as wc_to_model
import pypipet.core.transform.model_to_wc as model_to_wc

import logging
logger = logging.getLogger('__default__')

def _clean_up_data(data):
    keys = set(list(data.keys()))
    if 'created_at' in keys:
        del data['created_at']
    if 'updated_at' in keys:
        del data['updated_at']


def validate_product_info(product_info):
    if product_info.get('images') is None:
        logger.debug('missing images info')
        return False

    if product_info.get('price') is None:
        logger.debug('missing price info')

    if product_info.get('sku') is None:
        logger.debug('missing sku info')

    return True

class ShopConnector():
    def __init__(self, shop_name, shop_type, **kwargs):
        self.shop_name = shop_name
        self.shop_type = shop_type
        self.shop_api = kwargs.get('api', None)
        self.front_shop_id = kwargs.get('front_shop_id', None)
        self.field_mapping = kwargs.get('field_mapping', None)
        self.batch_size = kwargs.get('batch_size', 10)

    def set_shop_api(self, api):
        self.shop_api = api 

    def set_front_shop_id(self, shop_id):
        self.front_shop_id = shop_id

    def set_field_mapping(self, mapping):
        self.field_mapping = mapping

    def get_shop_info(self):
        return {
            'shop_name': self.shop_name,
            'shop_type': self.shop_type,
            'front_shop_id': self.front_shop_id
        }

    @staticmethod
    def add_product_to_shop(shop_type, shop_api, product_info, **kwargs):
        # _clean_up_data(product_info)
        if shop_type == 'wc':
            attr_list = kwargs.get('attr_list', ['brand', 'upc', 'size', 'color'])
            if kwargs.get('variation_attrs') is None or product_info.get('variations') is None:
                if model_to_wc.parse_to_wp_product(shop_api, product_info, attr_list, 
                                         status=kwargs.get('publish_type', 'publish')):
                    return wc.add_product(shop_api, product_info)
            else:
                product = model_to_wc.parse_to_wp_product_variable(shop_api, product_info, 
                                              attr_list,kwargs['variation_attrs'],
                                              parent_id=kwargs.get('parent_id'))
                
                if product:
                    return wc.add_product_variations(shop_api, product, parent_id=kwargs.get('parent_id'))

        else:
            logger.debug('missing shop info')

    @staticmethod
    def add_product_to_shop_bulk(shop_type, shop_api, products:list,  **kwargs):
        """for woocommerce, bulk add only for non-variable product"""
        if shop_type == 'wc':
            attr_list = kwargs.get('attr_list', ['brand', 'upc', 'size', 'color'])
            batch = []
            for product_info in products:
                if model_to_wc.parse_to_wp_product(shop_api, product_info, attr_list):
                    batch.append(product_info)
            #batch add 
            res = wc.update_product_batch(shop_api, 'create', batch)

        else:
            logger.debug('missing shop info')


    @staticmethod
    def get_destination_product_id(shop_type, shop_api, sku:str):
        """
        shop: dict with keys (front_shop_id, shop_api, shop_type)
        """
        if shop_type == 'wc':
            product = wc.get_product_by_sku(shop_api, sku)
            if product:
                return product['id']

        return None

    @staticmethod
    def update_shop_product(shop_type, shop_api, data:dict, product_id:str, **kwargs ):
        if shop_type == 'wc':
            attr_list = kwargs.get('attr_list', ['brand', 'upc', 'size', 'color'])
            if kwargs.get('formated') is None or kwargs['formated'] == False:
                if not model_to_wc.parse_to_wp_product(shop_api, data, attr_list, update_only=True):
                    logger.debug('wp parsing failed')
                    return 
            # print(data)
            if kwargs.get('parent_id') is not None:
                # print(kwargs['parent_id'], data)
                return wc.update_variation(shop_api, kwargs['parent_id'], product_id, data)
            return wc.update_product(shop_api, product_id, data)

    @staticmethod
    def update_shop_product_batch(shop_type, shop_api, data:list, **kwargs):
       if shop_type == 'wc':
            attr_list = kwargs.get('attr_list', ['brand', 'upc', 'size', 'color'])
            batch = []
            for i, d in enumerate(data):
                # print(d)
                if kwargs.get('formated') is None or kwargs['formated'] == False:
                    if model_to_wc.parse_to_wp_product(shop_api, d, attr_list, update_only=True):
                        if d.get('parent_id') is not None:
                            # print(d)
                            wc.update_variation(shop_api, d['parent_id'] , d['id'], d)
                        else:
                            batch.append(d)
                else:
                    batch.append(d)
            
            res = wc.update_product_batch(shop_api, 'update', batch)
            return res

    @staticmethod
    def sync_shop_orders(shop_type, shop_api, field_mapping, **kwargs):
        res = []
        if shop_type == 'wc':
            wp_orders = wc.get_new_orders(
                shop_api,
                start_from_order=kwargs.get('latest_order_id', '0'), 
                page_start=kwargs.get('page_start', 1), 
                per_page=kwargs.get('per_page', 20))
        
            for order in wp_orders:
                print('prcessing order', order['id'])
                # todo: get tax based on geo
                data = wc_to_model.wp_parse_order(order, field_mapping, 
                                shipping_tax_id=kwargs.get('shipping_tax_id',2), 
                                item_tax_id=kwargs.get('item_tax_id', 1)) 
                res.append(data)

        return res


    @staticmethod
    def update_order_status_at_shop(shop_type, shop_api, destination_order_id, 
                                   status,**kwargs):
        if shop_type == 'wc':
            res = wc.update_order(shop_api,
                                destination_order_id,
                                data={'status': status})
            return res

    @staticmethod
    def update_order_at_shop(shop_type, shop_api, destination_order_id, 
                             data, **kwargs):
        if shop_type == 'wc':
            res = wc.update_order(shop_api,
                                destination_order_id,
                                data=data)
            return res

    @staticmethod
    def update_order_item_at_shop(shop_type, shop_api, destination_order_id, 
                             items, **kwargs):
        if shop_type == 'wc':
            order = ShopConnector.get_order_at_shop(shop_type, shop_api,
                            destination_order_id=destination_order_id)
            item_list = model_to_wc.transform_order_item(order, items)
            res = wc.update_order(shop_api,
                                destination_order_id,
                                data={'line_items': item_list})
            return res

    @staticmethod
    def get_order_at_shop(shop_type, shop_api, **kwargs):
        # print(kwargs.get('destination_order_id'))
        if shop_type == 'wc':
            res = wc.get_order_by_id(shop_api,
                                kwargs.get('destination_order_id'))
            if kwargs.get('field_mapping') is not None:
                # todo: get tax based on geo
                res = wc_to_model.wp_parse_order(res, kwargs.get('field_mapping'), 
                                shipping_tax_id=kwargs.get('shipping_tax_id',2), 
                                item_tax_id=kwargs.get('item_tax_id', 1)) 
            return res

            

    @staticmethod        
    def get_products_at_shop(shop_type, shop_api, **kwargs):
        if shop_type == 'wc':
            data = wc.list_products(shop_api, 
                                params={
                                    'page': kwargs.get('page', 1), 
                                    'per_page': kwargs.get('batch_size', 10)
                                }) 
            for i, d in enumerate(data):
                data[i] = ShopConnector._parse_product(shop_type, shop_api, 
                                      d, kwargs.get('field_mapping'))
            return data
                
                            
    @staticmethod        
    def get_product_at_shop(shop_type, shop_api, product_id, **kwargs):
        if shop_type == 'wc':
            res = wc.get_product_by_id(shop_api, product_id) 
            return ShopConnector._parse_product(shop_type, shop_api, 
                                      res, kwargs.get('field_mapping'))
            
                

    @staticmethod    
    def get_category_taxonomy(shop_type, shop_api, **kwargs):
        if shop_type == 'wc':
            page = 1
            cats = []
            while True:
                batch_cats = wc.list_categories(shop_api, 
                                        page, 
                                        params=kwargs) 
                if batch_cats is None:
                    return None
                if len(batch_cats) == 0:
                    break
                cats += batch_cats 
                page += 1
            wc_to_model.wp_category_to_taxonomy(cats)
            return cats
    
    @staticmethod
    def update_customer_at_shop(shop_type, shop_api, destination_order_id, 
                             data, **kwargs):
        if shop_type == 'wc':
            model_to_wc.transform_customer(data)
            update = {}
            if kwargs.get('is_billing'):
                update['billing'] = data
            elif kwargs.get('is_shipping'):
                update['shipping'] = data
            else:
                logger.debug('need to specify biling or shipping')
                return 
            return wc.update_order(shop_api, destination_order_id, update) 

    @staticmethod
    def add_tracking(shop_type, shop_api, destination_order_id, 
                            message, **kwargs):
        if shop_type == 'wc':
            assert message.get('tracking_id')
            assert message.get('provider')
            tracking = f"tracking code {message['tracking_id']} service by \
                         {message['provider']}"
            res = wc.send_wc_message(shop_api,
                                destination_order_id,
                                tracking)
            return res

    @staticmethod
    def send_message(shop_type, shop_api, destination_order_id, 
                            message, **kwargs):
        if shop_type == 'wc':
            res = wc.send_wc_message(shop_api,
                                destination_order_id,
                                message)
            return res

    @staticmethod
    def _parse_product(shop_type, shop_api, product, field_mapping):
        if shop_type == 'wc':
            parsed = wc_to_model.parse_product(product, field_mapping)
            if parsed == 0:
                return 
            elif parsed == 1:
                variations = []
                for pid in product['variations']:
                    vari = wc.get_product_by_id(shop_api, pid) 
                    if vari: variations.append(vari)
                product['variations'] = variations 
                
                parsed = wc_to_model.parse_product_with_variations(product, field_mapping)
                
            return parsed
