#!/bin/bash

# Automate the deployment of 3-tier web application on gcp

# Functions:

services.yaml() {

echo "creating services.yaml ..."
kubectl create -f services.yaml


}
ingress.yaml() {

echo "kubectl create -f ingress.yaml!"
kubectl create -f ingress.yaml

}

deployments.yaml() {

echo "kubectl create -f deployments.yaml!"
kubectl create -f deployments.yaml

}


secrets.yaml() {

echo "secrets.yaml"
kubectl create -f secrets.yaml

}

completed() {
echo "deplyments created..."
exit

}


# Execution

# deploying services.yaml, ingress.yaml,deployments.yaml, secrets.yaml

var="services.yaml"

if [ "$var" == "services.yaml" ]; then
    services.yaml
    ingress.yaml
    deployments.yaml
    secrets.yaml
    completed

fi

if [  -n "$var"  ]; then
echo  "Error Invalid argument"

fi

    services.yaml
    ingress.yaml
    deployments.yaml
    secrets.yaml
    completed
