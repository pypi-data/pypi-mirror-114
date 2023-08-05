import re
import json

camel_pat = re.compile(r'([A-Z])')
under_pat = re.compile(r'_([a-z])')

def camel_to_underscore(name):
    return camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)

def underscore_to_camel(name):
    if isinstance(name,str) and not re.search(r'-', name):
        return under_pat.sub(lambda x: x.group(1).upper(), name)
    return name

def convert_json(d, convert):
    new_d = {}
    for k, v in d.items():
        new_d[convert(k)] = convert_json(v,convert) if isinstance(v,dict) else v
    return new_d

def convert_loads(*args, **kwargs):
    json_obj = json.loads(*args, **kwargs)
    return convert_json(json_obj, camel_to_underscore)

def convert_dumps(*args, **kwargs):
    args = (convert_json(args[0], underscore_to_camel),) + args[1:]
    return json.dumps(*args, **kwargs)