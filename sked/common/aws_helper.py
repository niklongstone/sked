"""AWS helpers"""

import hashlib
import boto3


def search_auto_scaling_by_tag(key, value):
    """Search Auto Scaling Groups by Tag"""

    auto_scaling_groups = []
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups()
    for auto_scaling in response['AutoScalingGroups']:
        for tag in auto_scaling['Tags']:
            if tag['Key'] == key:
                if tag['Value'] == value:
                    auto_scaling_groups.append(auto_scaling['AutoScalingGroupName'])

    return auto_scaling_groups

def scaling_name_generator(name):
    hash_object = hashlib.sha1(name)
    return hash_object.hexdigest()
