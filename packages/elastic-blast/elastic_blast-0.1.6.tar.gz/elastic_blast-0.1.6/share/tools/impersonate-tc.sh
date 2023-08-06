#!/bin/bash -xe
# Script to "impresonate" TC and delete GKE clusters that are lingering
export ELB_GCP_PROJECT=ncbi-sandbox-blast
export ELB_CLUSTER_NAME=${1-"elb-blastx-wb4-2-0811-nr-319-tomcat"}
export ELB_CONFIG_FILE=${2-"share/etc/elb-blastx-nr-WB4_2_0811.ini"}
export ELB_RESULTS=${3:-"gs://elasticblast-tomcat"}
export ELB_GCP_ZONE=us-east4-b
export ELB_GCP_REGION=us-east4
export ELB_DONT_DELETE_SETUP_JOBS=1
export KUBECONFIG=${PWD}/kubeconfig.yaml

./elastic-blast delete --loglevel DEBUG --logfile stderr --cfg ${ELB_CONFIG_FILE} 
