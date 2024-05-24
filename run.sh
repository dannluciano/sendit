#!/bin/bash

set -e

source env_vm/bin/activate

PORT=8002 DEBUG=True HIVEMIND_PROCFILE=Procfile.local hivemind