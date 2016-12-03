'''

 (c) 2016, Vsevolod Kolchinsky
 
'''

import requests


class UGS3Client(object):
    ''' minimal client implementation
    '''
    
    def __init__(self,host='ugs3.universinet.org'):
        self.ugs3_base_url = 'https://{}'.format(host)
        self.default_headers = {
                                'Accept':'application/json',
                                }

    @cached_property
    def my_username(self):
        r = requests.get('{}/auth/account/'.format(self.ugs3_base_url),
                         headers=self.default_headers)
        return r.json()['username']

    def set_authorization(self,auth_value):
        self.default_headers.update({
                                     'Authorization':auth_value,
                                     })

    def find(self,**kwargs):
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


