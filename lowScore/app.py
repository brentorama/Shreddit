"""This module contains script entrypoints for lowScore.
"""
import argparse
import yaml
import logging
import os
import pkg_resources
from appdirs import user_config_dir
from lowScore.lowScore import LowScore

default_config = {"username": None,
                  "password": None,
                  "verbose": True,
                  "save_directory": "/tmp",
                  "whitelist": [],
                  "whitelist_ids": [],
                  "multi_blacklist": [],
                  "multi_whitelist": [],
                  "item": "overview",
                  "sort": "new",
                  "whitelist_distinguished": True,
                  "whitelist_gilded": True,
                  "max_score": 100,
                  "hours": 24,
                  "nuke_hours": 4320,
                  "keep_a_copy": False,
                  "save_directory": None,
                  "trial_run": False,
                  "clear_vote": False,
                  "replacement_format": "random",
                  "edit_only": False,
                  "batch_cooldown": 10}

def main():
    global default_config
    parser = argparse.ArgumentParser(description="Command-line frontend to the lowScore library.")
    parser.add_argument("-c", "--config", help="Config file to use instead of the default lowScore.yml")
    parser.add_argument("-g", "--generate-configs", help="Write lowScore and praw config files to current directory.",
                        action="store_true")
    parser.add_argument("-u", "--user", help="User section from praw.ini if not default", default="default")
    args = parser.parse_args()

    if args.generate_configs:
        if not os.path.isfile("lowScore.yml"):
            print("Writing lowScore.yml file...")
            with open("lowScore.yml", "wb") as fout:
                fout.write(pkg_resources.resource_string("lowScore", "lowScore.yml.example"))
        if not os.path.isfile("praw.ini"):
            print("Writing praw.ini file...")
            with open("praw.ini", "wb") as fout:
                fout.write(pkg_resources.resource_string("lowScore", "praw.ini.example"))
        return

    config_dir = user_config_dir("lowScore/lowScore.yml")

    if args.config:
        config_filename = args.config
    elif os.path.exists(config_dir):
        config_filename = config_dir
    else:
        config_filename = "lowScore.yml"

    if not os.path.isfile(config_filename):
        print("No lowScore configuration file was found or provided. Run this script with -g to generate one.")
        return

    with open(config_filename) as fh:
        # Not doing a simple update() here because it's preferable to only set attributes that are "whitelisted" as
        # configuration options in the form of default values.
        user_config = yaml.safe_load(fh)
        for option in default_config:
            if option in user_config:
                default_config[option] = user_config[option]

    lowScore = LowScore(default_config, args.user)
    lowScore.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("LowScore aborted by user")
        quit()
