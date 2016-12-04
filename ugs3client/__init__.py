'''

 (c) 2016, Vsevolod Kolchinsky
 
'''
import json
import requests
import warnings
from cached_property import cached_property
from pymemcache.client.base import Client as pymemcache_client

VERSION='0.5-dev'

class UGS3ClientException(Exception):
    pass


class UGS3Client(object):
    ''' UGS3 client
    
    Usage:
    
        ugs3 = UGS3Client(host="...",memcache=('localhost',11211))
        ugs3.find_containers(name="test")
    
    set `memcache=None` to disable client-side caching.
    
    '''
    
    def __init__(self,host='ugs3.universinet.org',memcache=('localhost',11211)):
        self.ugs3_base_url = 'https://{}'.format(host)
        self.default_headers = {
                                'Accept':'application/json',
                                'User-Agent':'{}/{}'.format(
                                    self.__class__.__name__,VERSION),
                                }
        if memcache is not None:
            self._setup_memcache(memcache)

    def _setup_memcache(self,memcache_cfg):
        self.memcache = pymemcache_client(memcache_cfg)
    
    def _cache_store(self,key,value):
        try:
            self.memcache.set(key,value)
        except Exception as e:
            warnings.warn(repr(e),RuntimeWarning)
        pass
    
    def _cache_retrieve(self,key):
        '''
        @return: None for cache miss
        '''
        try:
            return self.memcache.get(key)
        except Exception as e:
            warnings.warn(repr(e),RuntimeWarning)
        pass
    
    def get_headers(self):
        return self.default_headers

    def _get_url_hash(self,url):
        return hash(''.join([getattr(self, '_auth_username',''),
                             url]))
    
    def _build_cache_key(self,*args,**kwargs):
        return ''.join(map(lambda x: str(x),
                           [self._get_url_hash(''.join(args)),
                            hash(frozenset(kwargs.items()))]))
        
    def get_response(self,method,url,**kwargs):
        request_func = getattr(requests,method.lower())
        request_headers = self.get_headers()
        # hash kwargs and check cache for saved response and Last-Modified
        # if present, include in headers 'If-Modified-Since'
        cache_key = self._build_cache_key(method,url,**kwargs)
        local_cache_hit = self._cache_retrieve(cache_key)
        if local_cache_hit is not None:
            request_headers.update({
                                    'If-Modified-Since':local_cache_hit[0],
                                    })
        response = request_func(url,data=kwargs,headers=request_headers)
        print(response.headers)
        if 401 == response.status_code:
            # is re-authentication required and possible?
            if 'Signature has expired.' == response.json().get('detail',''):
                if hasattr(self, '_auth_username'):
                    self.login(username=self._auth_username,
                               password=self._auth_password)
                    response = request_func(url,data=kwargs,
                                            headers=self.get_headers())
        # obey Not Modified response 304 and return cached value
        if 200 == response.status_code:
            # check headers for Last-Modified
            # if present, using kwargs hash save response and 
            # Last-Modified value
            if 'Last-Modified' in response.headers:
                self._cache_store(cache_key, (response.headers['Last-Modified'],
                                              response.text))
            return response.json()
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
        return self.get_response('get','{}/auth/account/'.format(
                                        self.ugs3_base_url))['username']

    def find_containers(self,**kwargs):
        return self.get_response('post','{}/containers/find/'.format(
                                        self.ugs3_base_url),**kwargs)
        
    def get_container(self,uuid):
        return self.get_response('get','{}/containers/{}/'.format(
                                        self.ugs3_base_url,uuid))


