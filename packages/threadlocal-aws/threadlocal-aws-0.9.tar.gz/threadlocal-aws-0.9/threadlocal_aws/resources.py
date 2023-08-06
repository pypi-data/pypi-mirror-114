import sys
from threadlocal_aws import _get_local_resource, _get_local_subresource, session, PY37
from threadlocal_aws.pep562 import Pep562

def __getattr__(name):
    if name.startswith("r_"):
        name = name[2:]
    if len(name.split("_")) == 2:
        client_name, resource_name = name.split("_")
        return lambda *args, **kwargs: _get_local_subresource(resource_name, _get_local_resource(client_name, **kwargs), *args)
    else:
        return lambda **kwargs: _get_local_resource(name, **kwargs)

if not PY37:
    Pep562(__name__)