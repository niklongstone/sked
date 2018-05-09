"""Test the Create command"""

from unittest import TestCase
try:
    from unittest.mock import patch
except ImportError:
    from mock.mock import patch
from sked.commands.create import Create


class TestCreate(TestCase):

    @patch("docopt.docopt")
    @patch("os.path.exists", return_value=True)
    def setUp(self, file_exists, docopt):
        self.create_command = Create(docopt)

    @patch("sked.common.yaml_parser.YamlParser")
    @patch("sked.common.AWSClient")
    def test_run_with_empty_config(self, aws_client, yaml_parser):
        """
        If the config file is empty the cli exits

        """
        self.create_command.config_parser = yaml_parser
        yaml_parser.read.return_value = {}
        with patch('sys.exit') as exit_mock:
            self.create_command.run()

        self.assertTrue(exit_mock.called)
        aws_client.assert_not_called()

    @patch("sked.common.yaml_parser.YamlParser")
    @patch("sked.commands.create.AWSClient.create")
    def test_run(self, aws_client, yaml_parser):
        self.create_command.config_parser = yaml_parser
        self.create_command.__client = aws_client
        autoscaling = [{'AutoScalingGroupName': 'Name', 'ScheduledActionName': 'Action Name'}]
        yaml_parser.read.return_value = autoscaling

        self.create_command.run()

        aws_client.assert_called_with(autoscaling[0])
