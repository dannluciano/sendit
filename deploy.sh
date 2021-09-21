#!/bin/bash

set -e

ssh-add dokku.ssh.priv_key
git push dokkur master