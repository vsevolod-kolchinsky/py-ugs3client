'''

 (c) 2016, Vsevolod Kolchinsky
 
'''

import requests
from cached_property import cached_property


class UGS3ClientException(Exception):
    pass


class UGS3Client(object):
    ''' minimal client implementation
    '''
    
    def __init__(self,host='ugs3.universinet.org'):
        self.ugs3_base_url = 'https://{}'.format(host)
        self.default_headers = {
                                'Accept':'application/json',
                                }

    def set_authorization(self,auth_value):
        self.default_headers.update({
                                     'Authorization':auth_value,
                                     })
        
    def login(self,username,password):
        r = requests.post('{}/auth/token/obtain/'.format(*self.ugs3_base_url),
                          headers=self.default_headers)
        return r.json()

    @cached_property
    def my_username(self):
        r = requests.get('{}/auth/account/'.format(self.ugs3_base_url),
                         headers=self.default_headers)
        return r.json()['username']

    def find_containers(self,**kwargs):
        r = requests.post('{}/containers/find/'.format(self.ugs3_base_url),
                          data=kwargs,headers=self.default_headers)
        return r.json()
        

    def get_container_payload(self,uuid):
        r = requests.get('{}/containers/{}/render/'.format(self.ugs3_base_url,
                                                           uuid),
                         headers=self.default_headers)
        return r.json()

    def get_container(self,uuid):
        r = requests.get('{}/containers/{}/'.format(self.ugs3_base_url,
                                                    uuid),
                         headers=self.default_headers)
        return r.json()


