'''
   Copyright 2016 Vsevolod Kolchinsky

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
 
'''
import json
import requests
import warnings
from cached_property import cached_property
from pymemcache.client.base import Client as pymemcache_client

__version__='0.8'

class UGS3ClientException(Exception):
    pass


class UGS3Client(object):
    ''' UGS3 client
    
    Usage:
    
        ugs3 = UGS3Client(host="...",memcache=('localhost',11211))
        ugs3.find_containers(name="test")
    
    set `memcache=None` to disable client-side caching using memcache
    (not recommended).
    
    '''
    
    def __init__(self,host='ugs3.universinet.org',memcache=('localhost',11211)):
        self.ugs3_base_url = 'https://{}'.format(host)
        self.default_headers = {
                                'Accept':'application/json',
                                'User-Agent':'{}/{}'.format(
                                    self.__class__.__name__,__version__),
                                }
        if memcache is not None:
            self._setup_memcache(memcache)

    def _setup_memcache(self,memcache_cfg):
        self.memcache = pymemcache_client(memcache_cfg)
    
    def _cache_store(self,key,value):
        try:
            self.memcache.set(key,value)
        except Exception as e:
            warnings.warn('pymemcache: {}'.format(repr(e)),RuntimeWarning)
        pass
    
    def _cache_retrieve(self,key):
        '''
        @return: None for cache miss
        '''
        try:
            return self.memcache.get(key)
        except Exception as e:
            warnings.warn('pymemcache: {}'.format(repr(e)),RuntimeWarning)
        pass
    
    def get_headers(self):
        return self.default_headers

    def _build_cache_key(self,*args,**kwargs):
        myargs = list(args) # copy
        myargs.append(getattr(self, '_auth_username',''))
        return hash(frozenset(myargs) | frozenset(kwargs.items()))
        
    def _call_request_func(self,request_func,method,url,headers,**kwargs):
        if 'get' == method.lower():
            return request_func(url,params=kwargs,headers=headers)
        return request_func(url,data=kwargs,headers=headers)
        
    def get_response(self,method,url,**kwargs):
        request_func = getattr(requests,method.lower())
        request_headers = self.get_headers()
        cache_key = self._build_cache_key(method,url,**kwargs)
        local_cache_hit = self._cache_retrieve(cache_key)
        if local_cache_hit is not None:
            cache_hit_data = json.loads(local_cache_hit)
            request_headers.update({
                                    'If-Modified-Since':cache_hit_data[0],
                                    })

        response = self._call_request_func(request_func,method,url,
                                           headers=request_headers,**kwargs)

        if 401 == response.status_code:
            # is re-authentication required and possible?
            if 'Signature has expired.' == response.json().get('detail',''):
                if hasattr(self, '_auth_username'):
                    self.login(username=self._auth_username,
                               password=self._auth_password)
                    response = self._call_request_func(request_func,method,url,
                                                       headers=request_headers,
                                                       **kwargs)
        if 304 == response.status_code:
            return json.loads(cache_hit_data[1])
        if 200 == response.status_code:
            if 'Last-Modified' in response.headers:
                self._cache_store(cache_key,
                                  json.dumps([
                                    response.headers['Last-Modified'],
                                    response.text]))
            return response.json()
        raise UGS3ClientException(response.status_code,response.text)

    def set_authorization(self,auth_value):
        self.default_headers.update({
                                     'Authorization':auth_value,
                                     })
        
    def login(self,**kwargs):
        r = requests.post('{}/auth/token/obtain/'.format(self.ugs3_base_url),
                          data=kwargs,headers=self.default_headers)
        if 200 != r.status_code:
            raise UGS3ClientException(r.status_code,r.json())
        map(lambda x: setattr(self,'_auth_{}'.format(x),kwargs.get(x)),kwargs)
        self.set_authorization('JWT {}'.format(r.json()['token']))
        return r.json()

    @cached_property
    def my_username(self):
        return self.get_response('get','{}/auth/account/'.format(
                                        self.ugs3_base_url))['username']

    def find_containers(self,**kwargs):
        return self.get_response('get','{}/containers/find/'.format(
                                        self.ugs3_base_url),**kwargs)
        
    def get_container(self,uuid):
        return self.get_response('get','{}/containers/{}/'.format(
                                        self.ugs3_base_url,uuid))


