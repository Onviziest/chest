#!/usr/bin/env bash
set -eux

arguments=$@

__main(){
    echo ${arguments}
}

__main
