#!/usr/bin/env sh
# -*- coding: utf-8; mode: shell-script; -*-
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

# Always run this script from its immediate parent folder


set_vars () {
    usage="usage: $0 [-h] [--help] [-y|--assume-yes] [-r|--realenv] [*]"
    cwd="${PWD}"
    realenv=
    assume_yes=""
    in_flags=""
    project_root="$(dirname "$(dirname "$(realpath "${0}")")")"
    project_name="$(basename "${project_root}")"
    help_msg="

    DESCRIPTION: [Uninstall \033[3m${project_name}\033[m if it exists and re-]
    install \033[3m${project_name}\033[m
       on ${VIRTUAL_ENV:-user\'s environment}


    Optional Arguments
    -h:\t\t\tshow usage command line and exit
    --help:\t\tshow this detailed help message and exit
    -r|--realenv:\tforce-override virtualenv check
    -y|--assume-yes:\tassume \033[3myes\033[m for uninstallation prompt

    Positional Arguments
    All are passed \033[1mverbatim\033[m to pip install
"
}

unset_vars () {
    cd "${cwd}" || exit 5
    unset usage
    unset help_msg
    unset cwd
    unset realenv
    unset assume_yes
    unset in_flags
    unset project_root
    unset project_name
}

clean_exit () {
    unset_vars
    if [ -z "${1}" ]; then
        exit 0
    else
        exit "${1}"
    fi
}

cli() {
    while test $# -gt 0; do
        case "${1}" in
            -h)
                printf "%s\n" "${usage}"
                clean_exit 0
                ;;
            --help)
                printf "%s\n" "${usage}"
                # shellcheck disable=SC2059
                printf "${help_msg}\n"
                clean_exit 0
                ;;
            -r|--realenv)
                realenv=true
                shift
                ;;
            -y|--assume-yes)
                assume_yes="-y"
                shift
                ;;
            *)
                in_flags="${in_flags} ${1}"
                shift
                ;;
        esac
    done
}

check_venv() {
    if [ -z "${VIRTUAL_ENV}" ] && [ ! ${realenv} ]; then
        printf "\033[1;31m[ERROR]\033[m Not working in a virtualenv\n\n" >&2
        printf "    \033[32m[Recommended]\033[m " >&2
        echo "activate virtualenv by typing without '# ':" >&2
        printf "        # \033[97msource " >&2
        printf "%s/.venv/bin/activate\033[m\n\n" "${project_root}">&2
        printf "    \033[31m[Risky]\033[m " >&2
        printf "else, use --realenv flag to override this error\n" >&2
        printf "        \033[33mDo this only if " >&2
        printf "you understand virtualenv\033[m\n\n" >&2
        echo "Aborting..."
        exit 1
    fi
}

pip_uninstall() {
    if command -v "${project_name}" >/dev/null 2>&1; then
        pip uninstall ${assume_yes} "${project_name}" || clean_exit "$?"
    fi
}

pip_install () {
    # DONT: we do WANT to glob this
    # shellckeck disable=SC2086
    pip install ${in_flags} ".."
}

main () {
    set_vars "$*"
    cli "$*"
    check_venv
    cd "${project_root}/code-aid" || exit 5
    pip_uninstall
    pip_install
    clean_exit
}

main "$*"
