import os
import sys
import platform
import signal
import contextlib
from subprocess import Popen, PIPE
from .logger import Logger
from .settings import *
from .file_utils import *

def get_editor():
    if platform.system() == 'Windows':
        return WindowsEditor()
    else:
        return PosixEditor()


class EditorBase(object):

    EDITOR = None

    def get_editor_cmdline(self):
        editor = os.getenv('DSO_EDITOR') or self.EDITOR
        return editor.split(' ')  ### IMPROVEME using shellex


    def edit(self, filename):
        self.filename = filename
        cmdline = self.get_editor_cmdline()
        cmdline.append(filename)
        if not exists_on_path(cmdline[0]):
            Logger.debug(f"Editor '{cmdline[0]}' not found in PATH.")
            return
        with open(self.filename, 'r+b') as f:
            oldContent = f.read()
        returnCode = self._popen(cmdline)
        if not returnCode == 0:
            raise DSOException(f"Edit failed with exit code '{returnCode}'.")
        with open(self.filename, 'r+b') as f:
            newContent = f.read()
        changed = not newContent == oldContent
        newContent = newContent.decode('utf-8')
        ### get rid of extra '\n' appended by editors on MacOS, not tested on Linux and Win
        if newContent and newContent[-1] == '\n':
            newContent = newContent[0:len(newContent)-1]
        return newContent, changed


    def _popen(self, *args, **kwargs):
        return Popen(*args, **kwargs).wait()


class PosixEditor(EditorBase):

    EDITOR = 'nano'


class WindowsEditor(EditorBase):

    EDITOR = 'nano'

    def _popen(self, *args, **kwargs):
        kwargs['shell'] = True
        return Popen(*args, **kwargs).wait()


Editor = get_editor()
