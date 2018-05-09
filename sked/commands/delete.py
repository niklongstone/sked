"""The delete command."""

import sys
from sked.common import AWSClient
from .basecommand import BaseCommand


class Delete(BaseCommand):
    """Delete Scheduled Actions for autoscaling groups."""

    def run(self):
        scheduled_action = self.config_parser.read()
        if not scheduled_action:
            print('No scheduled action found, check your config and filters')
            sys.exit()
        self.__apply_scheduled_actions(scheduled_action)

    def __apply_scheduled_actions(self, actions=[]):
        self.__client = AWSClient()
        for action in actions:
            try:
                parameters = {'AutoScalingGroupName': action['AutoScalingGroupName'],
                              'ScheduledActionName': action['ScheduledActionName']}
                self.__client.delete(parameters)
                print('Success!!! Deleted ' + action['AutoScalingGroupName'] + ' : ' + action['ScheduledActionName'])
            except Exception as e:
                print('Error!!!')
                print(e)
                print(action)
                exit()
