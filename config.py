#!/usr/bin/env python
from ConfigParser import ConfigParser, NoOptionError


def get_value(conf_dict, section, option, default=None, diff_key=None):
    config = ConfigParser()
    config.read(["fizzled.conf"])
    if not diff_key:
        diff_key = option

    try:
        value = config.get(section, option)
    except NoOptionError:
        value = default

    conf_dict[diff_key] = value
    return conf_dict

def load_generic_config(conf):
    conf = get_value(conf, 'generic', 'DATA_DIRECTORY', 'data')
    conf = get_value(conf, 'generic', 'SEED_DIRECTORY', 'seed')
    conf = get_value(conf, 'generic', 'WORK_DIRECTORY', 'work')
    conf = get_value(conf, 'generic', 'SAMPLES_DIRECTORY', 'samples')
    conf = get_value(conf, 'generic', 'CRASH_DIRECTORY', 'crash')
    conf = get_value(conf, 'generic', 'BINARY')
    conf = get_value(conf, 'generic', 'ARGUMENTS')
    return conf

def load_legion_config(conf):
    return conf

def load_stalker_config(conf):
    conf = get_value(conf, 'stalker', 'TIMESTAMP_FORMAT', '%B %dth, %l:%M %p')
    conf = get_value(conf, 'stalker', 'LOG_HANDLER', diff_key='STALKER_LOG_HANDLER')
    return conf

def load_mutilator_config(conf):
    return conf

def load_taskmaster_config(conf):
    return conf

def load_autopsy_config(conf):
    return conf

def load_config(app_name):
    conf = dict()
    conf = load_generic_config(conf)
    if app_name in ['legion', 'stalker', 'mutilator', 'taskmaster', 'autopsy']:
        # Normal
        conf = locals()["load_{}_config".format(name)](conf)
    elif not app_name:
        conf = load_legion_config(conf)
        conf = load_stalker_config(conf)
        conf = load_mutilator_config(conf)
        conf = load_taskmaster_config(conf)
        conf = load_autopsy_config(conf)

    return conf

if __name__ == '__main__':
    config = load_config(None) #  Load all.
    print(config)
    print("I should print the current config and check if it is alright.")
    print("Eg if files and folders exist.")
