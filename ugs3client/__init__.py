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

__version__='0.9.0'

class UGS3ClientException(Exception):
    pass


class UGS3Client(object):
    ''' UGS3 base level operations client
    
    Usage:
    
    .. code-block:: python
        :linenos:
        
        from ugs3client import UGS3Client
        
        ugs3 = UGS3Client(host="...",memcache=('localhost',11211))
        ugs3.find_containers(name="test")
    
    set `memcache=None` to disable client-side caching using memcache
    (not recommended).
    
    '''
    
    def __init__(self,host='ugs3.universinet.org',memcache=('localhost',11211)):
        '''
        :param host: UGS3 API host
        :param memcache: memcached server (host,port) tuple or None
        
        '''
        #: API base URL
        self.ugs3_base_url = 'https://{}'.format(host)
        #: persistent request headers
        self.default_headers = {
                                'Accept':'application/json',
                                'User-Agent':'{}/{}'.format(
                                    self.__class__.__name__,__version__),
                                }
        #: next request headers
        self.request_headers = {}
        if memcache is not None:
            self._setup_memcache(memcache)

    def _setup_memcache(self,memcache_cfg):
        self._memcache = pymemcache_client(memcache_cfg)
    
    def _cache_store(self,key,value):
        try:
            self._memcache.set(key,value)
        except Exception as e:
            warnings.warn('pymemcache: {}'.format(repr(e)),RuntimeWarning)
        pass
    
    def _cache_retrieve(self,key):
        '''
        :returns: value or None for cache miss
        '''
        try:
            return self._memcache.get(key)
        except Exception as e:
            warnings.warn('pymemcache: {}'.format(repr(e)),RuntimeWarning)
        pass
    
    def _build_cache_key(self,*args,**kwargs):
        myargs = list(args) # copy
        myargs.append(getattr(self, '_auth_username',''))
        return hash(frozenset(myargs) | frozenset(kwargs.items()))
        
    def _call_request_func(self,request_func,method,url,headers,**kwargs):
        if 'get' == method.lower():
            return request_func(url,params=kwargs,headers=headers)
        return request_func(url,data=kwargs,headers=headers)

    def _get_headers(self):
        headers = self.default_headers.copy()
        headers.update(**self.request_headers)
        self.request_headers = {}
        return headers
        
    def get_response(self,method,url,**kwargs):
        '''
        :returns: JSON -- API response
        :raises: UGS3ClientException
        '''
        request_func = getattr(requests,method.lower())
        request_headers = self._get_headers()
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
        ''' Set authentication request header
        '''
        self.default_headers.update({
                                     'Authorization':auth_value,
                                     })
        
    def login(self,**kwargs):
        ''' Exchange username and password to JWT which would used in further
        requests.

        :param username: UGS account username
        :param password: password
        :raises: UGS3ClientException
        '''
        r = requests.post('{}/auth/token/obtain/'.format(self.ugs3_base_url),
                          data=kwargs,headers=self.default_headers)
        if 200 != r.status_code:
            raise UGS3ClientException(r.status_code,r.json())
        map(lambda x: setattr(self,'_auth_{}'.format(x),kwargs.get(x)),kwargs)
        self.set_authorization('JWT {}'.format(r.json()['token']))
        return r.json()

    @cached_property
    def my_username(self):
        '''
        
        :returns: string -- currently authenticated username
        :raises: UGS3ClientException
        '''
        return self.get_response('get','{}/auth/account/'.format(
                                        self.ugs3_base_url))['username']


    def create_container(self,**kwargs):
        ''' Creates container
        
        :returns: JSON -- created container instance
        :raises: UGS3ClientException
        '''
        return self.get_response('post','{}/containers/'.format(
                                    self.ugs3_base_url),**kwargs)
        
    def update_container(self,uuid,ETag,**kwargs):
        ''' Update container
        
        :param uuid: existing Container UUID
        :param ETag: Containers last-known ETag assumed as actual
        :returns: JSON -- updated container instance
        :raises: UGS3ClientException
        '''
        if 'payload' in kwargs.keys() and \
                isinstance(kwargs.get('payload',None), dict):
            # serialize payload JSON
            kwargs['payload'] = json.dumps(kwargs.get('payload'))
        self.request_headers.update({
                                     'If-Match':ETag,
                                     })
        return self.get_response('patch','{}/containers/{}/'.format(
                                    self.ugs3_base_url,uuid),**kwargs)

    def find_containers(self,**kwargs):
        ''' Query containers
        
        :returns: list -- paginated query results
        :raises: UGS3ClientException
        '''
        return self.get_response('get','{}/containers/paginated_find/'.format(
                                        self.ugs3_base_url),**kwargs)
        
    def get_container(self,uuid):
        ''' Get container by uuid
        
        :param uuid: existing Container UUID
        :returns: JSON -- container data
        :raises: UGS3ClientException
        '''
        return self.get_response('get','{}/containers/{}/'.format(
                                        self.ugs3_base_url,uuid))


