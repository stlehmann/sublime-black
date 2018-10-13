import sublime
import sublime_plugin
import subprocess
import os


class BlackCommand(sublime_plugin.TextCommand):
    """Black command for reformatting."""

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
