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

# NOTE: You MUST alter some parts of this script, eg: pypi's username, password

set_vars () {
    usage="usage: $0 [-h] [--help] [-r|--release] [*]"
    cwd="${PWD}"
    realenv=
    up_flags=
    release="testpypi"
    project_dir="$(dirname "$(dirname "$(realpath "${0}")")")"
    project_name="$(basename "${project_dir}")"
    help_msg="

    DESCRIPTION: Distribute package to [test]pypi

    Optional Arguments
    -h:\t\t\tshow usage command line and exit
    --help:\t\tshow this detailed help message and exit
    -r|--release:\tupload to pypi repository instead of testpypi

    Positional Arguments
    All are passed \033[1mverbatim\033[m to twine
"
}

unset_vars () {
    cd "${cwd}" || exit 5
    unset usage
    unset help_msg
    unset cwd
    unset release
    unset up_flags
    unset project_dir
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
            -r|--release)
                release="pypi"
                shift
                ;;
            *)
                up_flags="${up_flags} ${1}"
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
        printf "%s/.venv/bin/activate\033[m\n\n" "${project_dir}">&2
        printf "    \033[31m[Risky]\033[m " >&2
        printf "else, use --realenv flag to override this error\n" >&2
        printf "        \033[33mDo this only if " >&2
        printf "you understand virtualenv\033[m\n\n" >&2
        echo "Aborting..."
        exit 1
    fi
}

pip_twine () {
    # start from scratch
    rm -rf "${project_dir}/build" "${project_dir}/dist"

    # build
    python3 -m "build" "${project_dir}"

    # upload
    # NOTE: edit this suitably
    # NOTE: this will upload to testpypi repo by default
    # shellcheck disable=SC2086
    twine upload \
          --skip-existing \
          --sign \
          --sign-with gpg2 \
          --identity <EMAIL> \
          --username <UNAME> \
          --password "$(pass show pypi.org/<UNAME>)" \
          --repository "${release}" \
          ${up_flags} \
          "${project_dir}"/dist/*
}

main () {
    set_vars "$*"
    cli "$*"
    check_venv
    cd "${project_dir}/code-aid" || exit 5
    pip_twine
    clean_exit
}

main "$*"
