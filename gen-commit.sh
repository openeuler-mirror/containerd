#!/bin/sh

# Copyright (c) Huawei Technologies Co., Ltd. 2020. All rights reserved.
# Description: This shell script is used to generate commitID store file.
# Author: liuzekun@huawei.com
# Create: 2020-06-10

change_id=$(git log -1 | grep Change-Id | awk '{print $2}')
if [[ "${change_id}" = "" ]]; then
    change_id=$(date | sha256sum | head -c 40)
fi
echo "${change_id}" > git-commit
