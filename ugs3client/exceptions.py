# -*- coding: utf-8 -*-
'''
   Copyright 2018 Vsevolod Kolchinsky

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
from __future__ import unicode_literals
import json
import warnings


class UGS3ClientException(Exception):
    
    def __init__(self, status_code=None, message=None, *args):
        self.status_code = status_code
        self.message = message
        super(UGS3ClientException, self).__init__(status_code, message, *args)

    def __getitem__(self, index):
        if 0 == index:
            warnings.warn('do not index exception, use status_code property', FutureWarning)
            return self.status_code
        elif 1 == index:
            warnings.warn('do not index exception, use message property', FutureWarning)
            return self.message
        raise TypeError("'UGS3ClientException' object does not support indexing")

