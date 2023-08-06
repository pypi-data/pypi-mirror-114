#!/bin/bash

set -ex

function prepare_environment() {
    : ${MY_IP:=0.0.0.0}
    if test $(id -u) != 0 ; then
        SUDO=sudo
    fi
    DATA=$(pwd)/data
    mkdir -p $DATA
}

function cleanup() {
    local serial=$1
    
    for i in test-gitlab$serial test-postgres$serial test-redis$serial ; do
	docker stop $i || true
	docker rm $i || true
    done
}

function run_redis() {
    local serial=$1
    
    docker run --name=test-redis$serial -d sameersbn/redis:latest
}

function run_db() {
    local serial=$1

    $SUDO rm -fr $DATA/postgres$serial
    mkdir -p $DATA/postgres$serial
    docker run --name=test-postgres$serial -d \
	   -e 'DB_NAME=gitlabhq_production' \
	   -e 'DB_USER=gitlab' \
	   -e 'DB_PASS=Wrobyak4' \
	   -e 'DB_EXTENSION=pg_trgm,btree_gist' \
	   -v $DATA/postgres$serial/data:/var/lib/postgresql \
	   sameersbn/postgresql:11-20200524
}

function run_gitlab() {
    local serial=$1
    
    $SUDO rm -fr $DATA/gitlab$serial
    mkdir -p $DATA/gitlab$serial
    docker run --name="test-gitlab$serial" -d -it --link test-postgres$serial:postgresql --link test-redis$serial:redisio \
	   -e OAUTH_BLOCK_AUTO_CREATED_USERS=false \
	   -e 'GITLAB_SIGNUP=true' \
	   -e "GITLAB_PORT=818$serial" \
	   -e "GITLAB_HOST=${MY_IP}" \
	   -e "GITLAB_SSH_PORT=222$serial" \
	   -p 222$serial:22 \
	   -p 818$serial:80 \
	   -e PUMA_WORKERS=1 \
	   -e GITLAB_SECRETS_SECRET_KEY_BASE=4W44tm7bJFRPWNMVzKngffxVWXRpVs49dxhFwgpx7FbCj3wXCMmsz47LzWsdr7nM \
	   -e GITLAB_SECRETS_DB_KEY_BASE=4W44tm7bJFRPWNMVzKngffxVWXRpVs49dxhFwgpx7FbCj3wXCMmsz47LzWsdr7nM \
	   -e GITLAB_SECRETS_OTP_KEY_BASE=4W44tm7bJFRPWNMVzKngffxVWXRpVs49dxhFwgpx7FbCj3wXCMmsz47LzWsdr7nM \
	   -e GITLAB_ROOT_PASSWORD=Wrobyak4 \
	   -v $DATA/gitlab$serial/data:/home/git/data \
	   sameersbn/gitlab:13.12.3
}

function setup_gitlab() {
    local serial=$1
    run_redis $serial
    run_db $serial
    run_gitlab $serial
    while true ; do
	if test $(curl --silent http://${MY_IP}:818$serial -o /dev/null -w "%{http_code}") = 302 ; then
	    return
	fi
	sleep 5
    done
    false
}

function setup() {
    setup_gitlab 1
    setup_gitlab 2
}

function teardown() {
    local serial
    for serial in 1 2 ; do
	cleanup $serial
    done
}

for f in prepare_environment ${@:-teardown setup} ; do
    $f
done
