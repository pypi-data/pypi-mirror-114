import boto3
import requests


def get_token():
    response = requests.put(
        "http://169.254.169.254/latest/api/token",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
    )
    return response.text


def get_instance_detail():
    token = get_token()
    response = requests.get(
        "http://169.254.169.254/latest/dynamic/instance-identity/document",
        headers={"X-aws-ec2-metadata-token": token}
    )
    return response.json()


def get_instance_vpc(instance_id, region):
    ec2 = boto3.resource('ec2', region_name=region)
    instance = ec2.Instance(instance_id)
    return instance.vpc.id


def get_instances_from_vpc(vpc_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(Filters=[
        {
            'Name': 'vpc-id',
            'Values': [vpc_id]
        },
    ])
    return response
