import sublime
import sublime_plugin
import subprocess
import os


class BlackCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        envs = os.environ.copy()
        window = sublime.active_window()
        view = window.active_view()
        print(view.file_name())
        p = subprocess.Popen(
            ["black", view.file_name()],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=envs,
        )
        print(p.communicate())
