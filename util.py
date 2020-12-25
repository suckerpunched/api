import json
import encoder

def response(obj, status):
    return {
        "statusCode": status, 
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        "body": json.dumps(obj, cls=encoder.DecimalEncoder)}

def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

def nested_get(dic, keys):
    ndic = dic
    for key in keys:
        ndic = ndic.get(key)
        if not ndic: return None
    return ndic
