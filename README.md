# 🚀 EasyPay Infrastructure Automation using Ansible & Kubernetes on AWS

![AWS](https://img.shields.io/badge/AWS-EC2-orange)
![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.30-blue)
![Docker](https://img.shields.io/badge/Docker-Container-blue)
![Ansible](https://img.shields.io/badge/Ansible-Automation-red)
![Helm](https://img.shields.io/badge/Helm-Charts-0F1689)
![Python](https://img.shields.io/badge/Python-3.x-green)
![License](https://img.shields.io/badge/License-Educational-success)

---

# 📖 Project Overview

This project demonstrates how to build a **production-style Kubernetes environment on AWS** using **Infrastructure as Code (Ansible)**.

The project automates:

- AWS Infrastructure provisioning
- Kubernetes Cluster installation
- Docker image deployment
- AWS Network Load Balancer integration
- Metrics Server installation
- Horizontal Pod Autoscaling (HPA)
- Network Policies
- RBAC
- ETCD Backup & Restore

The objective is to automate the entire infrastructure and application deployment lifecycle using Ansible.

---

# 🏗 Architecture

```text
                        Local Machine
                              │
                              │
                     Ansible Playbooks
                              │
                              ▼
                    AWS Infrastructure
                              │
          ┌───────────────────┴────────────────────┐
          │                                        │
          ▼                                        ▼
   Control Plane Node                      Worker Node(s)
          │                                        │
          └───────────────────┬────────────────────┘
                              │
                     Kubernetes Cluster
                              │
                         MySQL Database
                              │
                         Backend API
                              │
                      Frontend Service
                              │
                  AWS Network Load Balancer
                              |
                        External Users


```

---

# 🎯 Features Implemented

- ✅ Infrastructure Provisioning using Ansible
- ✅ Kubernetes Cluster Creation
- ✅ Dockerized Application
- ✅ AWS Load Balancer Controller
- ✅ Metrics Server
- ✅ Horizontal Pod Autoscaler
- ✅ Network Policies
- ✅ RBAC
- ✅ ETCD Backup
- ✅ Automated Deployment

---

# 📂 Repository Structure

```text
├── README.md
├── ansible
│   ├── 0.provision.yml                                     # Used to create 3 subnets , Security groups, Route table etc.
│   ├── 1.prepare-nodes.yml                                 # Install kubectl/kubelet/kubeadm on nodes. Also install helm/docker/containerd packages.
│   ├── 2.cluster-init-node-join.yml                        # Initializes Kubernets cluster from control plane node. Generates Join command
│   ├── 3.set-provider-ids.yml                              # Patches the Worker nodes Spec.ProviderID to allow LoadBalancers to work properly.
│   ├── 4.install-nlb-controller-metrics-server.yml         # Install LoadBalancerController and metrics-server addon in k8s cluster.
│   ├── 5.etcdctl-install.yml                               # Install etcdctl utilities in control plane node, required for etcd backup task.
│   ├── ansible.cfg                                         # ansible specific common config, no need to modify unless required
│   ├── files
│   │   ├── aws-load-balancer-controller-iam-policy.json    # Permission policy required for AWS NLB
│   │   └── metrics-server.yaml                             # Single manifest for metrics server deployment.
│   ├── group_vars
│   │   └── all.yml                                         # Variables used in ansible playbook.
│   ├── inventory
│   │   └── hosts.ini                                       # Inventory file for ansible                         
│   └── requirements.yml                                    # Required plugoins and modules
├── kubernetes
│   ├── 1.application.yaml                                  # For deploying Front/backend and DB pods and services.
│   ├── 2.hpa.yaml                                          # For deploying HPA for Back/Frontend targetting CPU utilization.
│   ├── 3.network-policy.yaml                               # For deploying custom network polciy allowing only frontend -> backend -> DB connectivity. 
│   ├── 4.rbac.yaml                                         # For creating a custom user with custom permissions. 
│   ├── 5.etcd-snapshot.sh                                  # Shell script for taking the ETCD Snapshot and verifying it.
│   ├── backend
│   │   ├── Dockerfile                                      # Dockerfile for building Backend application container image.
│   │   ├── app.py                                          # File for building Backend application
│   │   └── requirements.txt                                # Python modules required to run aplication. Will be used in docker build.
│   └── frontend
│       ├── Dockerfile                                      # Dockerfile for building Frontend application container image.
│       ├── index.html                                      # Application files for building Frontend application container image.
│       ├── nginx.conf                                      # Application files for building Frontend application container image.
│       ├── script.js                                       # Application files for building Frontend application container image.
│       └── style.css                                       # Application files for building Frontend application container image.

```

---

# 📑 Table of Contents

- Project Overview
- Architecture
- Prerequisites
- AWS Infrastructure Provisioning
- Node Preparation
- Kubernetes Cluster Initialization
- Worker Node Join
- Metrics Server
- AWS Load Balancer Controller
- Application Deployment
- HPA
- Network Policies
- RBAC
- ETCD Snapshot
- Troubleshooting

---

# ⚙ Prerequisites

## AWS

- AWS Account
- IAM User
- Access Key
- Secret Key

Configure AWS CLI

```bash
aws configure
```

Verify credentials

```bash
aws sts get-caller-identity
```

---

## Install Python Dependencies

```bash
pip install boto3 botocore
```

---

## Install Required Ansible Collections

```bash
ansible-galaxy collection install -r requirements.yml
```

---

# ☁ AWS Infrastructure Provisioning

The first playbook provisions the complete AWS infrastructure.

Playbook

```bash
ansible-playbook -i inventory.ini 0.provision.yml
```

---

## What does this playbook do?

The playbook performs the following tasks automatically.

### Networking

- Creates VPC
- Creates Public Subnets
- Creates Internet Gateway
- Configures Route Tables

---

### Security

Creates Security Groups allowing

- SSH (22)
- Kubernetes API Server (6443)
- NodePort Range
- Required Kubernetes Ports

---

### Compute

Creates

- Kubernetes Control Plane
- Worker Node(s)

---

### IAM

Creates

- IAM Roles
- Instance Profiles
- Required Policies

---

### SSH

Generates

```text
~/.ssh/generated-key
```

Automatically registers the key pair in AWS.

---

### Inventory

Updates

```text
inventory.ini
```

with the newly created EC2 instance IP addresses.

---

### Variables

Updates

```text
vars.yml
```

with dynamically generated values required by subsequent playbooks.

---

# 🔄 Infrastructure Provisioning Workflow

```text
Ansible Playbook
        │
        ▼
Create VPC
        │
        ▼
Create Security Groups
        │
        ▼
Create IAM Role
        │
        ▼
Generate SSH Keys
        │
        ▼
Launch EC2 Instances
        │
        ▼
Update inventory.ini
        │
        ▼
Update vars.yml
```

---

# 📸 Expected Output

> Insert the original provisioning screenshots from the document here **without changing their order or captions**.

---

# ✅ Verification

Verify the newly created infrastructure.

List EC2 instances

```bash
aws ec2 describe-instances
```

Verify Ansible inventory

```bash
cat inventory.ini
```

Verify generated variables

```bash
cat vars.yml
```

Test SSH connectivity

```bash
ssh -i ~/.ssh/generated-key ubuntu@<CONTROL-PLANE-IP>
```

---

# ✔ End of Part 1

In **Part 2**, we'll cover:

- Preparing Kubernetes Nodes
- Installing Docker & Container Runtime
- kubeadm Installation
- Initializing the Control Plane
- Joining Worker Nodes
- Cluster Verification
- ProviderID Configuration


# 🚀 Part 2 - Kubernetes Cluster Setup

---

# 📦 Preparing Kubernetes Nodes

Once the AWS infrastructure has been provisioned successfully, the next step is to prepare all EC2 instances by installing the required Kubernetes components.

The following playbook installs:

- Docker / Container Runtime
- containerd
- kubeadm
- kubelet
- kubectl
- Helm
- Required system packages

Execute:

```bash
ansible-playbook 1.prepare-nodes.yml
```

---

# 🏗 What does this playbook do?

| Component | Purpose |
|-----------|----------|
| Docker | Container Engine |
| containerd | Kubernetes Container Runtime |
| kubeadm | Cluster Bootstrap Tool |
| kubelet | Kubernetes Node Agent |
| kubectl | Kubernetes CLI |
| Helm | Kubernetes Package Manager |

---

# 🔄 Node Preparation Workflow

```text
Ansible
      │
      ▼
Install Docker
      │
      ▼
Install containerd
      │
      ▼
Install kubeadm
      │
      ▼
Install kubelet
      │
      ▼
Install kubectl
      │
      ▼
Install Helm
      │
      ▼
Enable Services
```

---

# 📸 Expected Output

> Insert the screenshots from the **Node Preparation** section of the original document here.

---

# 🔍 Verify Node Connectivity

After the playbook completes successfully, verify SSH connectivity to the Control Plane node.

```bash
ssh -i ~/.ssh/easypay-k8s ec2-user@<CONTROL_PLANE_PUBLIC_IP>
```

Exit the node after verifying access.

```bash
exit
```

---

# ☸ Initialize Kubernetes Cluster

The following playbook initializes the Kubernetes Control Plane and automatically joins the worker nodes.

Execute:

```bash
ansible-playbook 2.cluster-init-node-join.yml
```

---

## What happens during cluster initialization?

This playbook performs the following tasks:

- Initializes Kubernetes Control Plane
- Creates certificates
- Initializes ETCD
- Starts API Server
- Generates the Worker Join command
- Executes the Join command on Worker Nodes
- Configures kubeconfig

---

# 🔄 Cluster Initialization Workflow

```text
Control Plane
      │
      ▼
kubeadm init
      │
      ▼
Generate Join Token
      │
      ▼
Worker Node 1 joins
      │
      ▼
Worker Node 2 joins
      │
      ▼
Cluster Ready
```

---

# 📸 Expected Output

> Insert the screenshots showing successful `kubeadm init` and worker node join.

---

# ✅ Verify Kubernetes Cluster

Login to the Control Plane node.

```bash
ssh -i ~/.ssh/easypay-k8s ec2-user@<CONTROL_PLANE_PUBLIC_IP>
```

Verify nodes.

```bash
kubectl get nodes -o wide
```

Expected output:

```text
NAME          STATUS   ROLES           VERSION
master        Ready    control-plane
worker-1      Ready    <none>
worker-2      Ready    <none>
```

Verify all pods.

```bash
kubectl get pods -A -o wide
```

---

# 🏗 Kubernetes Cluster Architecture

```text
                 Kubernetes Cluster

                +-------------------+
                |   Control Plane   |
                |-------------------|
                | API Server        |
                | Scheduler         |
                | ControllerManager |
                | ETCD              |
                +---------+---------+
                          |
         -------------------------------------
         |                                   |
         ▼                                   ▼
 +--------------------+              +--------------------+
 |    Worker Node 1   |              |    Worker Node 2   |
 |--------------------|              |--------------------|
 | kubelet            |              | kubelet            |
 | containerd         |              | containerd         |
 | kube-proxy         |              | kube-proxy         |
 +--------------------+              +--------------------+
```

---

# 🔗 Configure Provider IDs

AWS Load Balancer Controller requires Kubernetes worker nodes to have their AWS ProviderID configured.

Execute:

```bash
ansible-playbook 3.set-provider-ids.yml
```

---

# Why is ProviderID required?

ProviderID maps a Kubernetes node to its corresponding EC2 instance.

Without it:

- AWS Load Balancer Controller cannot discover EC2 instances.
- LoadBalancer Services will fail to register targets correctly.

---

# 🔍 Verify ProviderID

```bash
kubectl describe node | egrep -i "^Name|provider"
```

Only Worker Nodes should display a ProviderID.

Example:

```text
ProviderID: aws:///us-east-1/i-0123456789abcdef0
```

---

# 📸 Expected Output

> Insert the ProviderID verification screenshot from the original document.

---

# ⚖ Install AWS Load Balancer Controller & Metrics Server

The next playbook installs:

- AWS Load Balancer Controller
- Metrics Server

It also copies the Kubernetes deployment manifests from the local machine to the Control Plane node.

Execute:

```bash
ansible-playbook 4.install-nlb-controller-metrics-server.yml
```

---

# Components Installed

| Component | Purpose |
|-----------|----------|
| AWS Load Balancer Controller | Creates AWS NLBs from Kubernetes Services |
| Metrics Server | Provides CPU & Memory metrics for HPA |
| Kubernetes Manifests | Application deployment YAMLs |

---

# 🔄 Installation Workflow

```text
Ansible
      │
      ▼
Install Helm Charts
      │
      ▼
Deploy AWS Load Balancer Controller
      │
      ▼
Deploy Metrics Server
      │
      ▼
Copy Kubernetes Manifests
      │
      ▼
Cluster Ready for Application Deployment
```

---

# 📂 Verify Manifest Files

SSH into the Control Plane node and verify the copied manifests.

```bash
ls -latr ~/kubernetes
```

You should see files similar to:

```text
1.application.yaml
2.hpa.yaml
3.network-policy.yaml
4.rbac.yaml
```

---

# 📸 Expected Output

> Insert the screenshots showing successful installation of the AWS Load Balancer Controller, Metrics Server, and copied manifest files.

---

# 📋 Cluster Verification Checklist

| Check | Command |
|--------|---------|
| Verify Nodes | `kubectl get nodes -o wide` |
| Verify Pods | `kubectl get pods -A` |
| Verify ProviderID | `kubectl describe node` |
| Verify Metrics Server | `kubectl top nodes` |
| Verify Controller | `kubectl get deployment -A` |

---

# 💡 Notes

> **Important**
>
> All `kubectl` commands should be executed **only from the Control Plane node**.

> **Tip**
>
> If the worker nodes do not join the cluster, verify:
>
> - Security Group rules
> - Join token validity
> - EC2 instance connectivity
> - `kubelet` service status

---

# ✔ End of Part 2

In **Part 3**, we'll cover:

- Building Docker images
- ARM64 vs AMD64 image considerations
- Docker Hub / AWS ECR login
- Tagging and pushing images
- Deploying the EasyPay application to Kubernetes
- Verifying Pods, Services, and the AWS Network Load Balancer


# 🚀 Part 3 - Build Docker Images & Deploy the EasyPay Application

---

# 🐳 Application Deployment Overview

Once the Kubernetes cluster is ready, the next phase is to build the application images and deploy the EasyPay application into the Kubernetes cluster.

The deployment consists of:

- Backend (Flask API)
- Frontend (React/Next.js)
- MySQL StatefulSet
- Kubernetes Services
- Secrets
- Persistent Storage
- AWS Network Load Balancer

---

# 🏗 Application Architecture

```text
                    Internet
                        │
                        ▼
             AWS Network Load Balancer
                        │
                        ▼
               Frontend Service (80)
                        │
                        ▼
               Frontend Deployment
                        │
                  REST API Calls
                        │
                        ▼
               Backend Service (5000)
                        │
                        ▼
              Backend Deployment (Flask)
                        │
                        ▼
                 MySQL ClusterIP Service
                        │
                        ▼
                 MySQL StatefulSet
                        │
                        ▼
              Persistent Volume Claim
```

---

# ⚠ Important Note – ARM64 vs AMD64

> **Important**
>
> The Simplilearn Lab machine is **ARM64**, while the Amazon Linux EC2 worker nodes are **AMD64**.
>
> Docker images built on ARM64 **will not run** on AMD64 worker nodes unless they are built as multi-architecture images.
>
> Therefore, build the Docker images **from the Control Plane node**, which matches the worker node architecture.

---

# 🐳 Docker Build Workflow

```text
Application Source
        │
        ▼
docker build
        │
        ▼
Local Docker Image
        │
        ▼
docker tag
        │
        ▼
Docker Repository Format
        │
        ▼
docker login
        │
        ▼
docker push
        │
        ▼
Docker Hub / AWS ECR
```

---

# 🔐 Login to Docker Registry

Before pushing Docker images, authenticate with your image repository.

## Docker Hub

```bash
docker login
```

Or use a Personal Access Token (PAT).

---

## AWS Public ECR

```bash
aws ecr-public get-login-password --region us-east-1 \
| docker login \
--username AWS \
--password-stdin public.ecr.aws/<ECR_ID>
```

---

## AWS Private ECR

```bash
aws ecr get-login-password --region us-east-1 \
| docker login \
--username AWS \
--password-stdin <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
```

---

# 🏗 Build Backend Image

Navigate to the backend source directory.

```bash
cd ~/kubernetes/backend
```

Build the image.

```bash
docker build -t easypay-backend:v1 .
```

Tag the image.

```bash
docker tag easypay-backend:v1 \
saurabhnegi2306/easypay:backend-v1
```

Push the image.

```bash
docker push saurabhnegi2306/easypay:backend-v1
```

---

# 🔄 Backend Image Lifecycle

```text
Backend Source Code
        │
        ▼
Dockerfile
        │
        ▼
docker build
        │
        ▼
easypay-backend:v1
        │
        ▼
docker tag
        │
        ▼
saurabhnegi2306/easypay:backend-v1
        │
        ▼
docker push
```

---

# 🏗 Build Frontend Image

Navigate to the frontend directory.

```bash
cd ../frontend
```

Build the image.

```bash
docker build -t easypay-frontend:v1 .
```

Tag it.

```bash
docker tag easypay-frontend:v1 \
saurabhnegi2306/easypay:frontend-v1
```

Push the image.

```bash
docker push saurabhnegi2306/easypay:frontend-v1
```

---

# 🔄 Frontend Image Lifecycle

```text
Frontend Source
        │
        ▼
Dockerfile
        │
        ▼
docker build
        │
        ▼
Local Image
        │
        ▼
docker tag
        │
        ▼
Docker Hub
        │
        ▼
docker push
```

---

# 📸 Expected Output

> Insert the original screenshots showing:
>
> - Docker build output
> - Docker tag
> - Docker push
> - Docker Hub repository

---

# 📝 Update Kubernetes Deployment Manifest

After pushing the images, update the deployment manifest with your image names.

File:

```text
kubernetes/1.application.yaml
```

Example:

```yaml
image: saurabhnegi2306/easypay:backend-v1
```

```yaml
image: saurabhnegi2306/easypay:frontend-v1
```

If you are using the same repository names as the lab guide, no changes are required.

---

# ☸ Deploy the EasyPay Application

Deploy all Kubernetes resources.

```bash
kubectl apply -f 1.application.yaml
```

This manifest deploys:

- Namespace
- Secret
- Configurations
- Frontend Deployment
- Backend Deployment
- MySQL StatefulSet
- ClusterIP Services
- LoadBalancer Service

---

# 📦 Kubernetes Resources Created

| Resource | Purpose |
|----------|----------|
| Namespace | Isolates application resources |
| Secret | Stores credentials |
| Deployment | Frontend |
| Deployment | Backend |
| StatefulSet | MySQL Database |
| Service | Backend ClusterIP |
| Service | Frontend LoadBalancer |
| PVC | Persistent Storage |

---

# 🏗 Kubernetes Resource Relationships

```text
Namespace (easypay)
│
├── Secret
│
├── Backend Deployment
│      │
│      ▼
│   Backend Service
│
├── Frontend Deployment
│      │
│      ▼
│ Frontend LoadBalancer Service
│
└── MySQL StatefulSet
       │
       ▼
 Persistent Volume Claim
```

---

# 🔍 Verify the Deployment

List all Pods.

```bash
kubectl get pods -n easypay -o wide
```

List all Services.

```bash
kubectl get svc -n easypay
```

Expected resources:

```text
frontend
backend
mysql
```

---

# 🌐 Verify AWS Network Load Balancer

The Frontend Service is exposed as a Kubernetes **LoadBalancer** Service.

Retrieve the external endpoint.

```bash
kubectl get svc frontend -n easypay
```

Example:

```text
NAME        TYPE           EXTERNAL-IP
frontend    LoadBalancer   a12345.elb.amazonaws.com
```

You should also see a Network Load Balancer created automatically in the AWS EC2 Console.

---

# 🌍 Application Request Flow

```text
Browser
    │
    ▼
AWS Network Load Balancer
    │
    ▼
Frontend Service
    │
    ▼
Frontend Pod
    │
REST API
    │
    ▼
Backend Service
    │
    ▼
Backend Pod
    │
SQL Queries
    │
    ▼
MySQL Service
    │
    ▼
MySQL StatefulSet
```

---

# 📸 Expected Output

> Insert the screenshots showing:
>
> - Successful Pods
> - Services
> - LoadBalancer EXTERNAL-IP
> - AWS Network Load Balancer
> - Application UI

---

# ✅ Deployment Verification Checklist

| Verification | Command |
|--------------|---------|
| Namespace | `kubectl get ns` |
| Pods | `kubectl get pods -n easypay` |
| Services | `kubectl get svc -n easypay` |
| Deployments | `kubectl get deploy -n easypay` |
| StatefulSets | `kubectl get sts -n easypay` |
| PVCs | `kubectl get pvc -n easypay` |

---

# 💡 Notes

> **Tip**
>
> If the Pods remain in `ImagePullBackOff`, verify:
>
> - The Docker images were pushed successfully.
> - The image names in `1.application.yaml` match the repository.
> - The worker nodes have internet access (or access to the image registry).
> - Docker Hub/ECR credentials are configured if using a private repository.

---

# ✔ End of Part 3

In **Part 4**, we'll demonstrate:

- Horizontal Pod Autoscaler (HPA)
- CPU Stress Testing
- Kubernetes Network Policies
- Role-Based Access Control (RBAC)
- ETCD Snapshot & Backup
- Complete Troubleshooting Guide



# 🚀 Part 4 - Kubernetes Operations, Security & Backup

---

# 📈 Horizontal Pod Autoscaler (HPA)

Horizontal Pod Autoscaler automatically increases or decreases the number of running pods based on resource utilization.

In this project, HPA monitors **CPU utilization** and scales the backend deployment accordingly.

---

# 🏗 HPA Architecture

```text
                Client Requests
                       │
                       ▼
                Backend Deployment
                       │
                       ▼
                CPU Utilization
                       │
                       ▼
               Metrics Server
                       │
                       ▼
       Horizontal Pod Autoscaler (HPA)
              │                 │
              ▼                 ▼
        Scale Up Pods      Scale Down Pods
```

---

# Deploy HPA

Apply the HPA manifest.

```bash
kubectl apply -f 2.hpa.yaml
```

Verify the HPA.

```bash
kubectl get hpa -n easypay
```

Expected Output

```text
NAME          REFERENCE                 TARGETS     MINPODS   MAXPODS
backend-hpa   Deployment/backend        10%/50%     1         5
```

---

# Verify Resource Metrics

Check pod resource consumption.

```bash
kubectl top pods -A
```

Check node resource utilization.

```bash
kubectl top nodes
```

---

# Simulate CPU Load

Identify the backend pod.

```bash
kubectl get pods -n easypay
```

Install the stress utility.

```bash
kubectl exec -it -n easypay <BACKEND_POD> \
-- sh -c "apt update && apt install -y stress"
```

Run the stress test.

```bash
kubectl exec -n easypay <BACKEND_POD> \
-- sh -c "stress --cpu 2 --timeout 300 >/dev/null 2>&1 &"
```

---

# Monitor Autoscaling

Watch the HPA status.

```bash
watch -d kubectl get hpa -n easypay
```

or

```bash
kubectl get hpa -n easypay
```

During the stress test, the backend deployment should scale out.

Example

```text
1 Pod
   │
   ▼
2 Pods
   │
   ▼
3 Pods
   │
   ▼
4 Pods
```

After the CPU load ends, Kubernetes automatically scales the deployment back down.

---

# 📸 Expected Output

> Insert the HPA screenshots from the original document:
>
> - `kubectl top pods`
> - `kubectl get hpa`
> - Scaling demonstration

---

# 🔒 Kubernetes Network Policies

By default, Kubernetes allows unrestricted communication between pods unless Network Policies are enforced.

This project demonstrates restricting pod-to-pod communication using Kubernetes Network Policies.

---

# Default Behavior

```text
Frontend Pod
       │
       ▼
Database

Backend Pod
       │
       ▼
Database

BusyBox Pod
       │
       ▼
Database

All Allowed
```

---

# Create Test Pods

Create a BusyBox pod in the application namespace.

```bash
kubectl run unauthorized-client \
-n easypay \
--image=busybox:1.36 \
--restart=Never \
-- sleep 3600
```

Create another BusyBox pod in the default namespace.

```bash
kubectl run unauthorized-client2 \
-n default \
--image=busybox:1.36 \
--restart=Never \
-- sleep 3600
```

---

# Verify Connectivity

Test MySQL connectivity.

```bash
kubectl exec -n easypay unauthorized-client \
-- nc -zv mysql 3306 -w 3
```

```bash
kubectl exec -n default unauthorized-client2 \
-- nc -zv mysql.easypay.svc.cluster.local 3306 -w 3
```

Test Backend Health API.

```bash
kubectl exec -n easypay unauthorized-client \
-- wget -qO- http://backend:5000/health
```

```bash
kubectl exec -n default unauthorized-client2 \
-- wget -qO- \
http://backend.easypay.svc.cluster.local:5000/health
```

Before applying the Network Policy, all requests should succeed.

---

# Apply Network Policy

```bash
kubectl apply -f 3.network-policy.yaml
```

Re-run the connectivity tests.

Unauthorized access should now be denied.

---

# Remove the Policy

```bash
kubectl delete -f 3.network-policy.yaml
```

Connectivity should be restored.

---

# Network Policy Flow

```text
Before

Any Pod
    │
    ▼
MySQL

Allowed

--------------------------------

After

Frontend
    │
    ▼
MySQL

Allowed

BusyBox
    │
    ▼
MySQL

Blocked
```

---

# 📸 Expected Output

> Insert the Network Policy screenshots from the original document.

---

# 👤 Role-Based Access Control (RBAC)

RBAC limits what authenticated users or service accounts are allowed to perform within the cluster.

---

# Deploy RBAC Resources

```bash
kubectl apply -f 4.rbac.yaml
```

---

# Verify Allowed Operations

```bash
kubectl auth can-i list pods \
-n easypay \
--as=lab-user
```

```bash
kubectl auth can-i get pods \
-n easypay \
--as=lab-user
```

```bash
kubectl auth can-i update pods \
-n easypay \
--as=lab-user
```

```bash
kubectl auth can-i delete pods \
-n easypay \
--as=lab-user
```

Expected Output

```text
yes
```

---

# Verify Restricted Operations

```bash
kubectl auth can-i delete deployments \
-n easypay \
--as=lab-user
```

```bash
kubectl auth can-i get secrets \
-n easypay \
--as=lab-user
```

```bash
kubectl auth can-i get nodes \
--as=lab-user
```

Expected Output

```text
no
```

---

# RBAC Architecture

```text
            User
              │
              ▼
         RoleBinding
              │
              ▼
            Role
              │
              ▼
 Allowed Kubernetes Actions
```

---

# 📸 Expected Output

> Insert the RBAC screenshots from the original document.

---

# 🌐 Application Verification

Retrieve the frontend service.

```bash
kubectl get svc frontend -n easypay
```

Open the AWS Network Load Balancer URL in your browser.

The application allows you to:

- Add Customer
- Enter Name
- Enter Email
- Enter Balance

The request flow is shown below.

```text
Browser
     │
     ▼
AWS Network Load Balancer
     │
     ▼
Frontend Pod
     │
 REST API
     │
     ▼
Backend Pod
     │
     ▼
Database Service
     │
     ▼
MySQL StatefulSet
```

---

# 📸 Expected Output

> Insert the application UI screenshots from the original document.

---

# 💾 ETCD Snapshot

The Kubernetes control plane stores all cluster state information in ETCD.

Backing up ETCD enables cluster recovery in the event of failures.

---

# Install ETCDCTL

Execute the Ansible playbook.

```bash
ansible-playbook 5.etcdctl-install.yml
```

---

# Create ETCD Snapshot

The commands are available in the provided script.

```bash
5.etcd-snapshot.sh
```

Alternatively, execute the commands individually as documented in the source guide.

---

# ETCD Backup Flow

```text
ETCD
   │
   ▼
etcdctl snapshot save
   │
   ▼
snapshot.db
   │
   ▼
Backup Storage
```

---

# 📸 Expected Output

> Insert the ETCD snapshot screenshots from the original document.

---

# 🛠 Troubleshooting

| Problem | Resolution |
|----------|------------|
| Worker node not joining | Verify the join token, security groups, and kubelet service. |
| Pods in `ImagePullBackOff` | Confirm image names and registry accessibility. |
| Metrics unavailable | Verify the Metrics Server deployment. |
| HPA shows `<unknown>` | Ensure Metrics Server is running and healthy. |
| Network Load Balancer not created | Confirm ProviderID configuration and AWS Load Balancer Controller deployment. |
| ProviderID missing | Re-run `3.set-provider-ids.yml`. |
| Network Policy not enforced | Verify the CNI plugin supports Network Policies and ensure the policy is applied in the correct namespace. |
| ETCD snapshot fails | Verify `etcdctl` installation and certificate paths. |

---

# 🎯 Learning Outcomes

This project demonstrates:

- Infrastructure as Code (IaC) with Ansible
- AWS infrastructure provisioning
- Kubernetes cluster bootstrapping
- Containerized application deployment
- AWS Network Load Balancer integration
- Docker image management
- Horizontal Pod Autoscaling
- Kubernetes Network Policies
- Role-Based Access Control
- ETCD backup and recovery

---

# 🧰 Technologies Used

| Category | Technologies |
|----------|--------------|
| Cloud | AWS EC2, VPC, IAM |
| Containerization | Docker |
| Orchestration | Kubernetes |
| Automation | Ansible |
| Package Management | Helm |
| Programming | Python |
| Database | MySQL |
| Monitoring | Metrics Server |
| Scaling | Horizontal Pod Autoscaler |
| Networking | AWS Load Balancer Controller |
| Security | RBAC, Network Policies |

---

# 📚 References

- Kubernetes Documentation
- Ansible Documentation
- Docker Documentation
- Helm Documentation
- AWS EC2 Documentation
- AWS Load Balancer Controller Documentation

---

# 👨‍💻 Author

**Saurabh Negi**

Cloud Infrastructure & DevOps Engineer

- AWS
- Kubernetes
- Docker
- Terraform
- Ansible
- Python
- CI/CD
- Cloud Automation

---

# ⭐ If you found this project useful, consider giving it a star on GitHub!



  
