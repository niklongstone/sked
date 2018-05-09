"""Class AWS_client"""

import boto3


class AWSClient(object):
    """Create a client to handle autoscaling scheduled action in AWS"""

    def __init__(self):
        self.__client = boto3.client('autoscaling')

    def create(self, parameters):
        """Create a scheduled scaling"""
        client_params = self._create_request_params(parameters)
        response = self.__client.put_scheduled_update_group_action(**client_params)

        return response

    def delete(self, parameters):
        """Delete a scheduled scaling"""
        client_params = {'AutoScalingGroupName': parameters['AutoScalingGroupName'],
                         'ScheduledActionName': parameters['ScheduledActionName']}
        response = self.__client.delete_scheduled_action(**client_params)

        return response

    def _create_request_params(self, config={}):
        parameters = {'AutoScalingGroupName': config['AutoScalingGroupName'],
                      'ScheduledActionName': config['ScheduledActionName']}
        if 'Time' in config:
            parameters.update({'Time': config['Time']})
        if 'StartTime' in config:
            parameters.update({'StartTime': config['StartTime']})
        if 'EndTime' in config:
            parameters.update({'EndTime': config['EndTime']})
        if 'Recurrence' in config:
            parameters.update({'Recurrence': config['Recurrence']})
        if 'MinSize' in config:
            parameters.update({'MinSize': config['MinSize']})
        if 'MaxSize' in config:
            parameters.update({'MaxSize': config['MaxSize']})
        if 'DesiredCapacity' in config:
            parameters.update({'DesiredCapacity': config['DesiredCapacity']})

        return parameters
