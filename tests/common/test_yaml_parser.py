"""Test the AWS_client class"""

from unittest import TestCase
try:
    from unittest.mock import patch
except ImportError:
    from mock.mock import patch
from sked.common.yaml_parser import YamlParser
import datetime


class TestAWSClient(TestCase):

    def setUp(self):
        self.yaml_parser = YamlParser('sked.yml')

    @patch("sked.common.yaml_parser.scaling_name_generator")
    @patch("sked.common.yaml_parser.search_auto_scaling_by_tag")
    def test__parse_tag(self, search_by_tag, name_generator):
        search_by_tag.return_value = ['stack-AWSEBAutoScalingGroup-SOMETHING-A']
        name_generator.return_value = '9590b8798db4623fa16ff87cd636958a657cae4c'
        max_size = 10
        desired_capacity = 5
        recurrence = '0 7 * * *'
        yaml_config = {'auto_scaling_groups':
            [{
                'filter': {'tag': {'key': 'Name', 'value': 'TAGName'}},
                'schedule': [
                    {
                        'profile': 'small', 'times':
                        [
                            {'start_time': datetime.datetime(2018, 3, 1, 0, 0)},
                        ]
                    }
                ]
            }],
            'profiles': {'small': {'recurrence': recurrence, 'desired_capacity': desired_capacity, 'max_size': max_size}}}
        expected_auto_scaling_scheduled_update = [
            {'DesiredCapacity': desired_capacity, 'AutoScalingGroupName': search_by_tag.return_value[0],
             'Recurrence': recurrence, 'MaxSize': max_size,
             'ScheduledActionName': 'scaling-' + name_generator.return_value,
             'StartTime': '2018-03-01 00:00:00'}]

        auto_scaling_scheduled_update = self.yaml_parser._parse(yaml_config)

        self.assertEqual(expected_auto_scaling_scheduled_update, auto_scaling_scheduled_update)

    @patch("sked.common.yaml_parser.scaling_name_generator")
    @patch("sked.common.yaml_parser.search_auto_scaling_by_tag")
    def test__parse_tags(self, search_by_tag, name_generator):
        search_by_tag.return_value = ['stack-AWSEBAutoScalingGroup-SOMETHING-A']
        name_generator.return_value = '9590b8798db4623fa16ff87cd636958a657cae4c'
        max_size = 10
        desired_capacity = 5
        recurrence = '0 7 * * *'
        yaml_config = {'auto_scaling_groups':
            [{
                'filter': {'tags': [{'tag': {'key': 'Name', 'value': 'Content'}}]},
                'schedule': [{'profile': 'small', 'times':
                    [{'start_time': datetime.datetime(2018, 3, 1, 0, 0)}]}]
            }],
            'profiles': {'small': {'recurrence': recurrence, 'desired_capacity': desired_capacity, 'max_size': max_size}}}

        expected_auto_scaling_scheduled_update = [
            {'DesiredCapacity': desired_capacity, 'AutoScalingGroupName': search_by_tag.return_value[0],
             'Recurrence': recurrence, 'MaxSize': max_size,
             'ScheduledActionName': 'scaling-' + name_generator.return_value,
             'StartTime': '2018-03-01 00:00:00'}]

        auto_scaling_scheduled_update = self.yaml_parser._parse(yaml_config)

        self.assertEqual(expected_auto_scaling_scheduled_update, auto_scaling_scheduled_update)
