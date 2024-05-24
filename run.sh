#!/bin/bash

set -e

source env_vm/bin/activate

PORT=8002 DEBUG=False HIVEMIND_PROCFILE=Procfile.local hivemind