#!/bin/bash

set -e

if test $(id -u) != 0 ; then
    SUDO=sudo
fi

$SUDO apt-get install -qq -y mercurial git

tests/setup-gitlab.sh "$@"
tests/setup-gitea.sh "$@"
