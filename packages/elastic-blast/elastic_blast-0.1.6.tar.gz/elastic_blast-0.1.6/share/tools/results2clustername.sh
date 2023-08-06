#!/bin/bash
# results2clustername.sh: Script to convert ElasticBLAST results to the default
# cluster name
#
# Author: Christiam Camacho (camacho@ncbi.nlm.nih.gov)
# Created: Thu 08 Apr 2021 04:07:29 PM EDT

export PATH=/bin:/usr/local/bin:/usr/bin
if [ $# -ne 1 ] ; then
    echo "Usage: $0 <ElasticBLAST results path>"
    exit 1
fi
elb_results=$1
results_hash=$(printf $elb_results | md5sum | cut -b-9)
echo elasticblast-$USER-$results_hash
