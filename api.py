import os, json, boto3

from util import response, nested_set, nested_get

dynamodb = boto3.resource('dynamodb')

def get_account(event, context):
    path = event['pathParameters']

    uid = path.get('_id')

    if not uid:
        return response({'error': 'invalid parameters provided'}, 400)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    resp = table.get_item(
        Key={
            '_id': uid
        }
    )

    item = resp.get('Item')
    if not item:
        return response({'error': 'account does not exist'}, 404)

    return response(item, 200)

def get_account_section(event, context):
    keys = event['path'].split('/')[3:]
    path = event['pathParameters']

    uid = path.get('_id')

    if not uid:
        return response({'error': 'invalid parameters provided'}, 400)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    resp = table.get_item(
        Key={
            '_id': uid
        }
    )

    item = resp.get('Item')
    if not item:
        return response({'error': 'account does not exist'}, 404)

    section = nested_get(item, keys)
    if not section:
        return response({'error': 'section does not exist'}, 404)

    if type(section) == str: 
        section = { "value":section }

    return response(section, 200)

# ------------------------------------------------------------------------------- #

def post_account(event, context):
    path = event['pathParameters']
    
    try: body = json.loads(event['body'])
    except: return response({'error': 'invalid json provided'}, 400)

    uid = path.get('_id')
    alias = body.get('alias')
    website = body.get('website')
    company = body.get('company')

    if not uid or not alias or not website or not company:
        return response({'error': 'invalid parameters provided'}, 400)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    resp = table.get_item(
        Key={
            '_id': uid
        }
    )

    new_item = {
        '_id': uid,
        'alias': alias,
        'website': website,
        'company': company
    }

    item = resp.get('Item')
    if item:
        new_item_keys = new_item.keys()
        for key in item:
            if key not in new_item_keys:
                new_item[key] = item[key]

    table.put_item(
        Item=new_item
    )

    return response(new_item, 200)

def post_account_section(event, context):
    path = event['pathParameters']
    keys = event['path'].split('/')[3:]

    try: body = json.loads(event['body'])
    except: return response({'error': 'invalid json provided'}, 400)

    uid = path.get('_id')

    if not uid:
        return response({'error': 'invalid parameters provided'}, 400)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    resp = table.get_item(
        Key={
            '_id': uid
        }
    )

    item = resp.get('Item')
    nested_set(item, keys, body)

    table.put_item(
        Item=item
    )

    return response(item, 200)

# ------------------------------------------------------------------------------- #

def put_account_section_pair_value(event, context):
    path = event['pathParameters']
    keys = event['path'].split('/')[3:]

    try: body = json.loads(event['body'])
    except: return response({'error': 'invalid json provided'}, 400)

    uid = path.get('_id')
    value = body.get('value')

    if not uid or not value:
        return response({'error': 'invalid parameters provided'}, 400)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    resp = table.get_item(
        Key={
            '_id': uid
        }
    )

    item = resp.get('Item')
    nested_set(item, keys, value)

    table.put_item(
        Item=item
    )

    return response(item, 200)