#!/usr/bin/env python
import boto3
from influxdb import InfluxDBClient

region = 'us-east-1'
ec2 = boto3.resource('ec2', region_name=region)
influxdb_client = InfluxDBClient(host='foo.dynu.net', port=8086, ssl=True, username='influxdb', password='3kr5dn40cld', database='dev')
env_tag = 'macmillan'

def lambda_handler(event, context):

	instances = ec2.instances.filter( Filters = [{ 'Name': 'tag:env',
                                               'Values': [env_tag] }])

	instance_count = 0
	for instance in instances:
	    instance_count = instance_count + 1

	print(instance_count)

	json_body = [
	    {
	        "measurement": "ec2",
	        "tags": {
	            "env": env_tag,
	            "region": region 
	        },
	        "fields": {
	            "instance_count": instance_count
	        }
	    }
	]

	print(json_body)
	
	influxdb_client.write_points(json_body)

if __name__ == '__main__':
    lambda_handler({}, {}) 
