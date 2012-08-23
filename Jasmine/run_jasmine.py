import os
import re
import thread
import subprocess
import functools
import time
import sublime
import sublime_plugin

class JasmineSwitchBetweenCodeAndSpec(sublime_plugin.TextCommand):
  def window(self):
    return self.view.window()

  class BaseFile(object):
    def __init__(self, file_name): self.folder_name, self.file_name = os.path.split(file_name)
    def possible_alternate_files(self): return []

  class JavascriptFile(BaseFile):
    def possible_alternate_files(self): return [self.file_name.replace(".js", "_spec.js")]

  class JasmineFile(BaseFile):
    def possible_alternate_files(self): return [self.file_name.replace("_spec.js", ".js")]

  def current_file(self):
    file_name = self.view.file_name()
    if re.search('\w+\_spec.js', file_name):
      return JasmineSwitchBetweenCodeAndSpec.JasmineFile(file_name)
    elif re.search('\w+\.js', file_name):
      return JasmineSwitchBetweenCodeAndSpec.JavascriptFile(file_name)
    else:
      return JasmineSwitchBetweenCodeAndSpec.BaseFile(file_name)

  def is_enabled(self):
    return self.current_file().possible_alternate_files()

  def run(self, args):
    possible_alternates = self.current_file().possible_alternate_files()
    alternates = self.project_files(lambda(file): file in possible_alternates)
    if alternates:
      self.window().open_file(alternates.pop())
    else:
      sublime.error_message("could not find " + str(possible_alternates))

  def walk(self, directory, ignored_directories = []):
    ignored_directories = ['.git', 'vendor']  # Move this into config
    for dir, dirnames, files in os.walk(directory):
      dirnames[:] = [dirname for dirname in dirnames if dirname not in ignored_directories]
      yield dir, dirnames, files

  def project_files(self, file_matcher):
    directories = self.window().folders()
    return [os.path.join(dirname, file) for directory in directories for dirname, _, files in self.walk(directory) for file in filter(file_matcher, files)]
