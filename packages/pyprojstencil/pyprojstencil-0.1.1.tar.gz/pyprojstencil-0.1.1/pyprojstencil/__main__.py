#!/usr/bin/env python3
# -*- coding:utf-8; mode:python; -*-
#
# Copyright 2021 Pradyumna Paranjape
# This file is part of pyprojstencil.
#
# pyprojstencil is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyprojstencil is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyprojstencil.  If not, see <https://www.gnu.org/licenses/>.
#
"""
Main application call
"""

from psprint import print

from . import INFO_BASE
from .command_line import configure
from .common import edit_modify
from .copy_tree import mod_exec, tree_copy
from .errors import NoProjectNameError
from .init_git import init_git_repo
from .init_venv import init_venv

# from .make_tree import create_tree
# from .init_subs import (copy_build, copy_code_aid, copy_docs, copy_src,
#                         copy_tests)


def main():
    """
    Main routine call
    """
    config = configure()
    # correct licenses
    config.license_header = edit_modify(config.license_header, config)
    if config.project is None:
        raise NoProjectNameError
    tree_copy(config, INFO_BASE.templates, config.project, skip_deep=False)
    mod_exec(config)
    init_venv(config)
    init_git_repo(config)
    print(config, mark="info")


if __name__ == "__main__":
    main()
