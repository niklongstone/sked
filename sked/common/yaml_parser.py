"""YamlParser."""

import yaml
from .config_parser import ConfigParser
from .aws_helper import search_auto_scaling_by_tag, scaling_name_generator


class YamlParser(ConfigParser):
    """Read yml file."""

    def read(self):
        with open(self.filename, 'r') as stream:
            try:
                config = yaml.load(stream)
                return self._parse(config)

            except yaml.YAMLError as e:
                print(e)

    def _parse(self, config):
        """Parse the scaling config"""

        auto_scaling_scheduled_update = []
        for as_config in config['auto_scaling_groups']:
            auto_scaling_groups = []
            if 'tag' in as_config['filter']:
                tag = as_config['filter']['tag']
                auto_scaling_groups = search_auto_scaling_by_tag(tag['key'], tag['value'])
            elif 'tags' in as_config['filter']:
                tags = as_config['filter']['tags']
                for tag in tags:
                    tag_key = tag['tag']['key']
                    tag_value = tag['tag']['value']
                    tag_auto_scaling_groups = search_auto_scaling_by_tag(tag_key, tag_value)
                    auto_scaling_groups.extend(tag_auto_scaling_groups)
            elif 'name' in as_config['filter']:
                auto_scaling_groups = as_config['name']
            else:
                print('You must specify either a tag or a name in the auto_scaling_groups filter')

            auto_scaling_scheduled_update.extend(self._build_scheduled_definition(auto_scaling_groups, as_config, config))

        return auto_scaling_scheduled_update

    def _build_scheduled_definition(self, auto_scaling_groups, as_config, config):
        auto_scaling_scheduled_update = []
        for auto_scaling_group in auto_scaling_groups:
            for schedule in as_config['schedule']:
                i = 0
                for scaling_time in schedule['times']:
                    profile_name = schedule['profile']
                    profile = config['profiles'][profile_name]
                    scheduled = {}
                    schedule_action_name = ''
                    scheduled['AutoScalingGroupName'] = auto_scaling_group
                    if 'start_time' in scaling_time:
                        scheduled['StartTime'] = str(scaling_time['start_time'])
                        schedule_action_name += scheduled['StartTime']
                    if 'end_time' in scaling_time:
                        scheduled['EndTime'] = str(scaling_time['end_time'])
                        schedule_action_name += scheduled['EndTime']
                    if 'desired_capacity' in profile:
                        scheduled['DesiredCapacity'] = profile['desired_capacity']
                    if 'min_size' in profile:
                        scheduled['MinSize'] = profile['min_size']
                    if 'max_size' in profile:
                        scheduled['MaxSize'] = profile['max_size']
                    if 'recurrence' in profile:
                        scheduled['Recurrence'] = profile['recurrence']
                    scheduled['ScheduledActionName'] = 'scaling-' + scaling_name_generator(schedule_action_name)
                    i += 1
                    auto_scaling_scheduled_update.append(scheduled)

        return auto_scaling_scheduled_update
