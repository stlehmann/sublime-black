import logging
import sublime
import sublime_plugin
import subprocess
import os


SETTINGS = "SublimeBlack.sublime-settings"

logger = logging.getLogger(__name__)


class Settings:

    def __init__(self):
        self._settings = sublime.load_settings(SETTINGS)

    def __get__(self, key):
        return self._settings.get(key)


class BlackCommand(sublime_plugin.TextCommand):
    """Black command for reformatting."""

    def __init__(self):
        self.settings = Settings()

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

        # get the filename for the current view
        try:
            current_file = sublime.active_window().active_view().file_name()
        except AttributeError as e:
            logger.error(str(e))
            return

        envs = os.environ.copy()
        args = []

        # line length: set maximum line length
        if self.settings["line_length"] is not None:
            args += ["-l{0}".format(self.settings["line_length"])]

        # py36: Allow using Python 3.6 syntax
        if self.settings["py36"]:
            args += ["--py36"]

        # skip_string_normalization: Don't normalize string quotes or prefixes
        if self.settings["skip_string_normalization"]:
            args += ["-S"]

        # skip_numeric_underscore_normalization: Don't normalize numeric underscores
        if self.settings["skip_numeric_underscore_normalization"]:
            args += ["-N"]

        p = subprocess.Popen(
            ["black", current_file] + args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=envs,
        )

        stdout, stderr = p.communicate()
        print(stdout, stderr)
