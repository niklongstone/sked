"""Test the Delete command"""

from unittest import TestCase
try:
    from unittest.mock import patch
except ImportError:
    from mock.mock import patch
from sked.commands import Delete


class TestDelete(TestCase):

    @patch("docopt.docopt")
    @patch("os.path.exists", return_value=True)
    def setUp(self, file_exists, docopt):
        self.delete_command = Delete(docopt)

    @patch("sked.common.yaml_parser.YamlParser")
    @patch("sked.common.AWSClient")
    def test_run_with_empty_config(self, aws_client, yaml_parser):
        """
        If the config file is empty the cli exits

        """
        self.delete_command.config_parser = yaml_parser
        yaml_parser.read.return_value = {}
        with patch('sys.exit') as exit_mock:
            self.delete_command.run()

        self.assertTrue(exit_mock.called)
        aws_client.assert_not_called()

    @patch("sked.common.yaml_parser.YamlParser")
    @patch("sked.commands.delete.AWSClient.delete")
    def test_run(self, aws_client, yaml_parser):
        self.delete_command.config_parser = yaml_parser
        self.delete_command.__client = aws_client
        autoscaling = [{'AutoScalingGroupName': 'Name', 'ScheduledActionName': 'Action Name'}]
        yaml_parser.read.return_value = autoscaling

        self.delete_command.run()

        aws_client.assert_called_with(autoscaling[0])
