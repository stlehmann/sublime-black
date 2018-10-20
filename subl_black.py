import logging
import sublime
import sublime_plugin
import subprocess
import os


SETTINGS = "SublimeBlack.sublime-settings"

logger = logging.getLogger(__name__)


def plugin_loaded():
    print("SublimeBlack loaded")


class Settings:
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


class BlackCommand(sublime_plugin.TextCommand):
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
        print(stdout, stderr)
