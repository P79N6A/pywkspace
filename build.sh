#!/bin/bash

if [ ! -f ./env/bin/activate ]; then
    virtualenv ./env
fi

source ./env/bin/activate

pip install -r requirements
