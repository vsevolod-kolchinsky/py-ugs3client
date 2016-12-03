Help on package ugs3client:

NAME
    ugs3client - (c) 2016, Vsevolod Kolchinsky

FILE
    /home/dee/py-ugs3client/ugs3client/__init__.py

PACKAGE CONTENTS


CLASSES
    __builtin__.object
        UGS3Client
    exceptions.Exception(exceptions.BaseException)
        UGS3ClientException
    
    class UGS3Client(__builtin__.object)
     |  minimal client implementation
     |  
     |  Methods defined here:
     |  
     |  __init__(self, host='ugs3.universinet.org')
     |  
     |  find_containers(self, **kwargs)
     |  
     |  get_container(self, uuid)
     |  
     |  get_container_payload(self, uuid)
     |  
     |  get_headers(self)
     |  
     |  get_response(self, method, url, **kwargs)
     |  
     |  login(self, **kwargs)
     |  
     |  my_username = <cached_property.cached_property object>
     |  set_authorization(self, auth_value)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class UGS3ClientException(exceptions.Exception)
     |  Method resolution order:
     |      UGS3ClientException
     |      exceptions.Exception
     |      exceptions.BaseException
     |      __builtin__.object
     |  
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from exceptions.Exception:
     |  
     |  __init__(...)
     |      x.__init__(...) initializes x; see help(type(x)) for signature
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from exceptions.Exception:
     |  
     |  __new__ = <built-in method __new__ of type object>
     |      T.__new__(S, ...) -> a new object with type S, a subtype of T
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from exceptions.BaseException:
     |  
     |  __delattr__(...)
     |      x.__delattr__('name') <==> del x.name
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __reduce__(...)
     |  
     |  __repr__(...)
     |      x.__repr__() <==> repr(x)
     |  
     |  __setattr__(...)
     |      x.__setattr__('name', value) <==> x.name = value
     |  
     |  __setstate__(...)
     |  
     |  __str__(...)
     |      x.__str__() <==> str(x)
     |  
     |  __unicode__(...)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from exceptions.BaseException:
     |  
     |  __dict__
     |  
     |  args
     |  
     |  message

DATA
    VERSION = '0.4'


