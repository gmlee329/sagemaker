import json
from boto3.session import Session

def lambda_handler(event, context):
    
    try:
        # API Gateway GET method
        if event['httpMethod'] == 'GET':
            result = {
                'message' : 'GET method does not support'
            }
            return json.dumps(result)
        # API Gateway POST method
        elif event['httpMethod'] == 'POST':
            payload = event['body']

    except KeyError:
        # direct invocation
        img = event['img']
        data = {
            'img' : img
        }
        payload = json.dumps(data)

    session = Session()
    runtime = session.client("runtime.sagemaker")
    response = runtime.invoke_endpoint(
        EndpointName='resnet',
        ContentType='application/json',
        Body=payload)

    body = json.loads(response["Body"].read())
    body = json.dumps(body)
    result = {
        "headers": {
            "content-type": "application/json"
            },
        "body": body,
        "statusCode": 200
        }
    return result