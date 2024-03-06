#!/bin/bash

set -e

source env_vm/bin/activate

DEBUG=True HIVEMIND_PROCFILE=Procfile.local hivemind