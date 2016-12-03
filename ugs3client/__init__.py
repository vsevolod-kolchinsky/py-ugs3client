'''

 (c) 2016, Vsevolod Kolchinsky
 
'''

import requests
from cached_property import cached_property

VERSION='0.4'

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

    def get_headers(self):
        return self.default_headers
    
    def get_response(self,method,url,**kwargs):
        request_func = getattr(requests,method.lower())
        response = request_func(url,data=kwargs,headers=self.get_headers())
        if 401 == response.status_code:
            if 'Signature has expired.' == response.json().get('detail',''):
                if hasattr(self, '_auth_username'):
                    self.login(username=self._auth_username,
                               password=self._auth_password)
                    return request_func(url,data=kwargs,
                                        headers=self.get_headers())
        if 200 == response.status_code:
            return response
        raise UGS3ClientException(response.status_code,response.json())

    def set_authorization(self,auth_value):
        self.default_headers.update({
                                     'Authorization':auth_value,
                                     })
        
    def login(self,**kwargs):
        r = requests.post('{}/auth/token/obtain/'.format(self.ugs3_base_url),
                          data=kwargs,headers=self.default_headers)
        if 200 != r.status_code:
            raise UGS3ClientException(r.status_code,r.json())
        for kwarg in kwargs:
            setattr(self, '_auth_{}'.format(kwarg), kwargs.get(kwarg))
        self.set_authorization('JWT {}'.format(r.json()['token']))
        return r.json()

    @cached_property
    def my_username(self):
        r = self.get_response('get','{}/auth/account/'.format(
                                            self.ugs3_base_url))
        return r.json()['username']

    def find_containers(self,**kwargs):
        r = self.get_response('post','{}/containers/find/'.format(
                                self.ugs3_base_url),**kwargs)
        return r.json()
        

    def get_container_payload(self,uuid):
        r = self.get_response('get','{}/containers/{}/render/'.format(
                                self.ugs3_base_url,uuid))
        return r.json()

    def get_container(self,uuid):
        r = self.get_response('get','{}/containers/{}/'.format(
                                self.ugs3_base_url,uuid))
        return r.json()


