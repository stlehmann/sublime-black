import sublime
import sublime_plugin
import subprocess
import os


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
        window = sublime.active_window()
        view = window.active_view()
        file_name = view.file_name()

        envs = os.environ.copy()

        p = subprocess.Popen(
            ["black", file_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=envs,
        )

        p.communicate()
