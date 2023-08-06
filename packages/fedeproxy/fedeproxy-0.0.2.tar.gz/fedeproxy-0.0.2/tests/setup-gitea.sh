#!/bin/bash

set -ex

function prepare_environment() {
    : ${MY_IP:=0.0.0.0}
}

function wait_for() {
    success=false
    for delay in 1 1 5 5 15 15 15 30 30 30 30 ; do
	if "$@" |& tee tests/setup-gitea.out ; then
	    success=true
	    break
	fi
	sleep $delay
    done
    $success
}

function setup_gitea() {
    local serial=$1

    docker run --name gitea$serial -p 878$serial:3000 -p 272$serial:22 \
	   -e "GITEA__security__INSTALL_LOCK=true" \
	   -e "GITEA__server__DOMAIN=${MY_IP}" \
	   -e "GITEA__server__SSH_DOMAIN=${MY_IP}" \
	   -e "GITEA__server__ROOT_URL=http://${MY_IP}:878$serial/" \
	   -e "GITEA__service__DEFAULT_KEEP_EMAIL_PRIVATE=true" \
	   -d gitea/gitea:1.14.2
    sleep 5 # for some reason trying to run "gitea admin" while gitea is booting will permanently break everything
    wait_for docker exec gitea$serial gitea admin user create --access-token --admin --username root --password Wrobyak4 --email admin@example.com
}

function setup() {
    local serial
    for serial in $serials ; do
	setup_gitea $serial
    done
}

function teardown() {
    local serial
    for serial in $serials ; do
	docker stop gitea$serial || true
	docker rm -f gitea$serial || true
    done
}

: ${serials:=1 2}

for f in prepare_environment ${@:-teardown setup} ; do
    $f
done
