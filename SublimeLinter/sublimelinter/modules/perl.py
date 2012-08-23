# -*- coding: utf-8 -*-
# perl.py - sublimelint package for checking perl files

import re

from base_linter import BaseLinter

CONFIG = {
    'language': 'perl',
    'executable': 'perl',
    'lint_args': '-c'
}


class Linter(BaseLinter):
    def parse_errors(self, view, errors, lines, errorUnderlines, violationUnderlines, warningUnderlines, errorMessages, violationMessages, warningMessages):
        for line in errors.splitlines():
            match = re.match(r'(?P<error>.+?) at .+? line (?P<line>\d+)(, near "(?P<near>.+?)")?', line)

            if match:
                error, line = match.group('error'), match.group('line')
                lineno = int(line)
                near = match.group('near')

                if near:
                    error = '{0}, near "{1}"'.format(error, near)
                    self.underline_regex(view, lineno, '(?P<underline>{0})'.format(re.escape(near)), lines, errorUnderlines)

                self.add_message(lineno, lines, error, errorMessages)
