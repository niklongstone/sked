"""Test the AWS_client class"""

from unittest import TestCase
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock.mock import MagicMock, patch
import boto3
from sked.common.aws_client import AWSClient


class TestAWSClient(TestCase):

    @patch("boto3.client")
    def setUp(self, aws_client):
        self.mock_autoscaling = MagicMock(autospec=boto3.client)
        aws_client.return_value = self.mock_autoscaling

        self.client = AWSClient()
        self.params = {
            'AutoScalingGroupName': 'Name',
            'ScheduledActionName': 'ActionName',
            'Time': '2018-01-01T00:00:00Z',
            'StartTime': '2018-01-01T00:00:00Z',
            'EndTime': '2018-01-01T00:00:00Z',
            'Recurrence': '1 * * * *',
            'MinSize': 1,
            'MaxSize': 3,
            'DesiredCapacity': 2
        }

    def test_create_request_params(self):
        request_params = self.client._create_request_params(self.params)

        self.assertEqual(request_params, self.params)

    def test_create(self):
        self.client.create(self.params)

        self.mock_autoscaling.put_scheduled_update_group_action.assert_called_once_with(**self.params)

    def test_delete(self):
        client_params = {'AutoScalingGroupName': self.params['AutoScalingGroupName'],
                         'ScheduledActionName': self.params['ScheduledActionName']}
        self.client.delete(client_params)

        self.mock_autoscaling.delete_scheduled_action.assert_called_once_with(**client_params)
