import logging
import sublime
import sublime_plugin
import subprocess
import os


logger = logging.getLogger(__name__)


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

        # get the filename for the current view
        try:
            current_file = sublime.active_window().active_view().file_name()
        except AttributeError as e:
            logger.error(str(e))
            return

        envs = os.environ.copy()

        p = subprocess.Popen(
            ["black", current_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=envs,
        )

        stdout, stderr = p.communicate()
        print(stdout, stderr)
