#!/bin/bash
# aws-show-my-undeleted-searches.sh: This script shows my undeleted searches in
# AWS and their status
#
# Author: Christiam Camacho (camacho@ncbi.nlm.nih.gov)
# Created: Sat 07 Aug 2021 11:01:46 AM EDT

set -euo pipefail
shopt -s nullglob

TMP=`mktemp -t $(basename -s .sh $0)-XXXXXXX`
trap " /bin/rm -fr $TMP " INT QUIT EXIT HUP KILL ALRM

aws sts get-caller-identity --output json | jq -Mr .Arn

aws batch describe-compute-environments --output json | \
    jq -Mr ".computeEnvironments[] | select(.tags.creator==\"$USER\") | [ .tags.results, .tags.created ] | @tsv" > $TMP

while read -r results created; do 
    echo "##### $results"
    echo "##### Created $created"
    elastic-blast status --results $results
done < $TMP
echo

# Show also those CloudFormation stacks that failed to delete
aws cloudformation describe-stacks --output json | \
    jq -Mr ".Stacks[] | select( (.StackName|contains(\"$USER\")) and (.StackStatus|contains(\"DELETE\")) ) | [ (.Tags[] | select(.Key==\"results\") | .Value), (.Tags[] | select(.Key==\"created\") | .Value), .StackStatus ] | @tsv" > $TMP
[ ! -s $TMP ] && exit

echo "These are your failed CloudFormation stacks, please be sure to delete them with the commands listed below"

while read -r results created status; do 
    echo "##### $results"
    echo "##### Created $created"
    echo "##### Status $status"
    echo elastic-blast delete --results $results
done < $TMP
