# A Python API wrapper for SimpleRelevance
# free to use and unlicensed
# you can download requests using pip

import requests
import json as simplejson

#  You can get an API key by signing up for SimpleRelevance on the site.
# Signup is free.
#
#  Async: When you are done testing, set async=1. This will speed up API
# response times by a factor of 2 or 3.
#
#  Predictions: this is the part of SimpleRelevance that eventually costs
# money to use. They will not be available right away, as our automated
# model builds happen nightly. Please get in touch during business hours
# (inquiries@simplerelevance.com) if you want us to build a model sooner.

# Documentation:
#   Note that documentation is available at simplerelevance.com/docs/api2

class SRAPI():
    def __init__(self, api_key, async=0):
        self.base_url = "https://www.simplerelevance.com/api/v2/"
        self.api_key = api_key
        self.async = async

    def _post(self, endpoint, post_data):
        data = {
            'api_key':self.api_key,
            'async':self.async,
            'data':post_data
        }
        return requests.post("%s%s" % (self.base_url, endpoint), data=data)

    def _get(self,endpoint,get_params):
        params = {'api_key': self.api_key}
        params.update(get_params)
        return requests.get("%s%s" % (self.base_url, endpoint), params=params)

    def add_user(self,email,zipcode=None,user_id=None,data_dict={}):
        payload = [
            {
                "email":email,
                "user_id":user_id,
                "data_dict":data_dict
            }
        ]
        encoded_payload = simplejson.dumps(payload)
        return self._post('users/', encoded_payload)

    def add_item(self, item_name, item_id, 
                 item_type='product', data_dict={}, variants={}):
        
        payload = [
            {
                "item_name":item_name,
                "item_id":item_id,
                "item_type":item_type,
                "data_dict":data_dict,
                "variants":variants
            }
        ]
        encoded_payload = simplejson.dumps(payload)
        return self._post('items/', encoded_payload)

    # action_hook should be "clicks/" or "purchases/"
    def add_action(self, action_hook="purchases/", user_id=None, 
                   item_id=None, email=None, item_name=None, 
                   timestamp=None, price=None, zipcode=None):
        
        payload = [
            {
                'user_id':user_id,
                'item_id':item_id,
                'price':price,
                'email':email,
                'item_name':item_name,
                'timestamp':timestamp,
                'zipcode':zipcode
            }
        ]
        encoded_payload = simplejson.dumps(payload)
        return self._post(action_hook,encoded_payload)

    def add_batch_users(self,payload):
        encoded_payload = simplejson.dumps(payload)
        return self._post('users/', encoded_payload)

    def add_batch_items(self,payload):
        encoded_payload = simplejson.dumps(payload)
        return self._post('items/', encoded_payload)

    def add_batch_actions(self, payload, action_hook='purchases/'):
        encoded_payload = simplejson.dumps(payload)
        return self._post(action_hook,encoded_payload)

    def get_predictions(self, email, market=None, starts=None, expires=None):
        return self._get('items/',
                            {
                                'email':email,
                                'market':market,
                                'starts':starts,
                                'expires':expires
                            }
        )
