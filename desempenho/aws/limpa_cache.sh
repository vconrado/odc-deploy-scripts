#!/bin/bash

sudo sysctl -w vm.drop_caches=3
ssh esensing-004 sudo sysctl -w vm.drop_caches=3
