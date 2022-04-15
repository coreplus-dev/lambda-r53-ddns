# 参考
# https://docs.aws.amazon.com/lambda/latest/dg/urls-invocation.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html


import json
import boto3

def route53Update(zone_id, domain_name, record_value):
    client = boto3.client('route53')
    return client.change_resource_record_sets(
        HostedZoneId = zone_id,
        ChangeBatch = {
            'Changes' : [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': domain_name,
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': record_value,
                            },
                        ],
                    },
                },
            ],
        },
    )
    
def recordGet(zone_id, domain_name):
    client = boto3.client('route53')
    return client.list_resource_record_sets(
        HostedZoneId = zone_id,
        StartRecordName = domain_name
    )

def lambda_handler(event, context):
    source_ip = event['requestContext']['http']['sourceIp']
    request_body = json.loads(event['body'])
    zone_id = request_body['zone_id']
    domain_name = request_body['domain_name']
    
    print('zoneid : ' + zone_id)
    print('domainname : ' + domain_name)
    
    record = recordGet(zone_id, domain_name)
    if record['ResourceRecordSets'][0]['ResourceRecords'][0]['Value'] == source_ip:
        # IP 変更なし
        response = {'status': 'success', 'record' 'not changed' 'request_data': event['body']}
    else:
        # IP 変更あり
        route53Update(zone_id, domain_name, source_ip)
        response = {'status': 'success', 'record': 'changed', 'source_ip': source_ip, 'request_data': request_body}
    
    # response = 'OK'
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
