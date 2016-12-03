'''

 (c) 2016, Vsevolod Kolchinsky
 
'''

import requests
from cached_property import cached_property

VERSION='0.2'

class UGS3ClientException(Exception):
    pass


class UGS3Client(object):
    ''' minimal client implementation
    '''
    
    def __init__(self,host='ugs3.universinet.org'):
        self.ugs3_base_url = 'https://{}'.format(host)
        self.default_headers = {
                                'Accept':'application/json',
                                'User-Agent':'{}/{}'.format(self.__class__.__name__,
                                                            VERSION)
                                }

    def _response_successful(self,response):
        if 200 != response.status_code:
            raise UGS3ClientException(response.json())
        return True

    def set_authorization(self,auth_value):
        self.default_headers.update({
                                     'Authorization':auth_value,
                                     })
        
    def login(self,**kwargs):
        r = requests.post('{}/auth/token/obtain/'.format(self.ugs3_base_url),
                          data=kwargs,headers=self.default_headers)
        if self._response_successful(r):
            self.set_authorization('JWT {}'.format(r.json()['token']))
            return r.json()

    @cached_property
    def my_username(self):
        r = requests.get('{}/auth/account/'.format(self.ugs3_base_url),
                         headers=self.default_headers)
        if self._response_successful(r):
            return r.json()['username']

    def find_containers(self,**kwargs):
        r = requests.post('{}/containers/find/'.format(self.ugs3_base_url),
                          data=kwargs,headers=self.default_headers)
        if self._response_successful(r):
            return r.json()
        

    def get_container_payload(self,uuid):
        r = requests.get('{}/containers/{}/render/'.format(self.ugs3_base_url,
                                                           uuid),
                         headers=self.default_headers)
        if self._response_successful(r):
            return r.json()

    def get_container(self,uuid):
        r = requests.get('{}/containers/{}/'.format(self.ugs3_base_url,
                                                    uuid),
                         headers=self.default_headers)
        if self._response_successful(r):
            return r.json()


