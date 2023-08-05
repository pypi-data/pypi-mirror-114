import os
import logging
import sys
import textwrap

import cli_ui
import yaml
from pathlib import Path

from gitlabform import EXIT_INVALID_INPUT


class ConfigurationCore:

    config = None
    config_dir = None

    def __init__(self, config_path=None, config_string=None):

        if config_path and config_string:
            cli_ui.fatal(
                "Please initialize with either config_path or config_string, not both."
            )
            sys.exit(EXIT_INVALID_INPUT)

        try:
            if config_string:
                cli_ui.debug("Reading config from provided string.")
                self.config = yaml.safe_load(textwrap.dedent(config_string))
                self.config_dir = "."
            else:  # maybe config_path
                if "APP_HOME" in os.environ:
                    # using this env var should be considered unofficial, we need this temporarily
                    # for backwards compatibility. support for it may be removed without notice, do not use it!
                    config_path = os.path.join(os.environ["APP_HOME"], "config.yml")
                elif not config_path:
                    # this case is only meant for using gitlabform as a library
                    config_path = os.path.join(
                        str(Path.home()), ".gitlabform", "config.yml"
                    )
                elif config_path in [os.path.join(".", "config.yml"), "config.yml"]:
                    # provided points to config.yml in the app current working dir
                    config_path = os.path.join(os.getcwd(), "config.yml")

                cli_ui.debug(f"Reading config from file: {config_path}")

                with open(config_path, "r") as ymlfile:
                    self.config = yaml.safe_load(ymlfile)
                    logging.debug("Config parsed successfully as YAML.")

                # we need config path for accessing files for relative paths
                self.config_dir = os.path.dirname(config_path)

                if self.config.get("example_config"):
                    cli_ui.fatal(
                        "Example config detected, aborting.\n"
                        "Haven't you forgotten to use `-c <config_file>` parameter?\n"
                        "If you created your config based on the example config.yml,"
                        " then please remove 'example_config' key."
                    )
                    sys.exit(EXIT_INVALID_INPUT)

                if self.config.get("config_version", 1) != 2:
                    cli_ui.fatal(
                        "This version of GitLabForm requires 'config_version: 2' entry in the config.\n"
                        "This ensures that when the application behavior changes in a backward incompatible way,"
                        " you won't apply unexpected configuration to your GitLab instance.\n"
                        "Please read the upgrading guide here: https://bit.ly/3ub1g5C\n"
                    )
                    sys.exit(EXIT_INVALID_INPUT)

                try:
                    self.config.get("projects_and_groups")
                except KeyNotFoundException:
                    cli_ui.fatal("'projects_and_groups' key in the config is required.")
                    sys.exit(EXIT_INVALID_INPUT)

        except (FileNotFoundError, IOError):
            raise ConfigFileNotFoundException(config_path)

        except Exception:
            if config_path:
                raise ConfigInvalidException(config_path)
            else:
                raise ConfigInvalidException(config_string)

    def get(self, path, default=None):
        """
        :param path: "path" to given element in YAML file, for example for:

        group_settings:
          sddc:
            deploy_keys:
              qa_puppet:
                key: some key...
                title: some title...
                can_push: false

        ..a path to a single element array ['qa_puppet'] will be: "group_settings|sddc|deploy_keys".

        To get the dict under it use: get("group_settings|sddc|deploy_keys")

        :return: element from YAML file (dict, array, string...)
        """
        tokens = path.split("|")
        current = self.config

        try:
            for token in tokens:
                current = current[token]
        except:
            if default is not None:
                return default
            else:
                raise KeyNotFoundException

        return current


class ConfigFileNotFoundException(Exception):
    pass


class ConfigInvalidException(Exception):
    pass


class KeyNotFoundException(Exception):
    pass
