import os
import filecmp
import sys
import logging
import sublime
import sublime_plugin
import subprocess
import shutil
import zipfile

#: name of the plugin
PLUGIN_NAME = "SublimeBlack"
#: path where the plugin is meant to be installed
INSTALLED_PLUGIN_NAME = "{0}.sublime-package".format(PLUGIN_NAME)
#: package installation path
PACKAGES_PATH = sublime.packages_path()
#: plugin installation path
PLUGIN_PATH = os.path.join(PACKAGES_PATH, PLUGIN_NAME)
#: path of the plugin file
INSTALLED_PLUGIN_PATH = os.path.abspath(os.path.dirname(__file__))
#: settings filename
SETTINGS = "SublimeBlack.sublime-settings"

logger = logging.getLogger(__name__)

sys.path.insert(0, PLUGIN_PATH)


def plugin_loaded():
    """Execute when Plugin is loaded.

    Make sure all Plugin files are in the main package directory of Sublimetext.
    This is mainly for the default settings file.

    """
    if INSTALLED_PLUGIN_PATH != PLUGIN_PATH:
        # check if installed plugin is the same as this file
        installed_plugin_path = os.path.join(PLUGIN_PATH, INSTALLED_PLUGIN_NAME)
        if os.path.exists(installed_plugin_path) and filecmp.cmp(
            installed_plugin_path, INSTALLED_PLUGIN_PATH
        ):
            return

        # remove old package data
        if os.path.exists(PLUGIN_PATH):
            try:
                shutil.rmtree(PLUGIN_PATH)
            except:  # noqa: E722
                logger.error("Could not remove old Plugin directory")

        # create new plugin dir
        if not os.path.exists(PLUGIN_PATH):
            os.mkdir(PLUGIN_PATH)

        z = zipfile.ZipFile(INSTALLED_PLUGIN_PATH, "r")
        for f in z.namelist():
            z.extract(f, PLUGIN_PATH)
        z.close()

        shutil.copyfile(INSTALLED_PLUGIN_PATH, installed_plugin_path)


class Settings:
    """Convenience class for accessing settings."""

    def __init__(self):
        try:
            self._settings = sublime.load_settings(SETTINGS)
        except Exception:
            self._settings = None
            logger.error("Could not load settings")

    def __getitem__(self, key):
        if self._settings:
            return self._settings.get(key)
        else:
            return None


class black_reformat(sublime_plugin.TextCommand):
    """Black command for reformatting."""

    def is_enabled(self):
        try:
            current_file = sublime.active_window().active_view().file_name()
            return current_file.endswith((".py", ".pyw"))

        except AttributeError:
            # catch AttributeError if sublime.active_window or active_view or file_name
            # are None, which can happen if there is no active window or no open file or
            # even if the current file has not been saved, yet
            pass

        return False

    def run(self, edit):
        settings = Settings()
        # get the filename for the current view
        try:
            current_file = sublime.active_window().active_view().file_name()
        except AttributeError as e:
            logger.error(str(e))
            return

        envs = os.environ.copy()
        args = []

        # line length: set maximum line length
        if settings["line_length"] is not None:
            args += ["-l{0}".format(settings["line_length"])]

        # py36: Allow using Python 3.6 syntax
        if settings["py36"]:
            args += ["--py36"]

        # skip_string_normalization: Don't normalize string quotes or prefixes
        if settings["skip_string_normalization"]:
            args += ["-S"]

        # skip_numeric_underscore_normalization: Don't normalize numeric underscores
        if settings["skip_numeric_underscore_normalization"]:
            args += ["-N"]

        p = subprocess.Popen(
            ["black", current_file] + args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=envs,
        )

        stdout, stderr = p.communicate()
        logger.debug("{0}, {1}".format(stdout, stderr))


class black_diff(sublime_plugin.TextCommand):
    pass
