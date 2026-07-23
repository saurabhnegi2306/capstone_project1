# AWS Self-Managed Kubernetes Lab

                    AWS Load Balancer
                           |
                           v
                    Worker NodePort
                           |
          +----------------+----------------+
          |                                 |
     t3.small                         t3.small
     WORKER 1                         WORKER 2
     2 GB RAM                         2 GB RAM
          \                               /
           \                             /
            +---------------------------+
                         |
                    t3.small
                  CONTROL PLANE
                     2 GB RAM
                         |
                       etcd
                       
Three-node kubeadm cluster on AWS:
- 1 x t3.small control plane
- 2 x t3.small workers


.
├── README.md     # README file with instructions to deploy the infrastructure for k8s and application
├── ansible       # Directory with ansible related config.
│   ├── 0.provision.yml          # Used to create 3 subnets , Security groups, Route table etc.
│   ├── 1.prepare-nodes.yml      # Install kubectl/kubelet/kubeadm on nodes. Also install helm/docker/containerd packages.
│   ├── 2.cluster-init-node-join.yml     # Initializes Kubernets cluster from control plane node. Generates Join command
│   ├── 3.set-provider-ids.yml  # Patches the Worker nodes Spec.ProviderID to allow LoadBalancers to work properly.
│   ├── 4.install-nlb-controller-metrics-server.yml # Install LoadBalancerController and metrics-server addon in k8s cluster.
│   ├── 5.etcdctl-install.yml   # Install etcdctl utilities in control plane node, required for etcd backup task.
│   ├── ansible.cfg             # config file for ansible, with some required parameters, no need to modify. 
│   ├── files        # Directory having support files. Installed during 5.install-nlb-controller-metrics-server.yml
│   │   ├── aws-load-balancer-controller-iam-policy.json  # Permissions required to create Loadbalancer (during 0.provision.yml).
│   │   └── metrics-server.yaml      # Deployment file for metrics server ( during 5.install-nlb-controller-metrics-server.yml)
│   ├── group_vars
│   │   └── all.yml     # Common Variables and inputs for "all" nodes. ONLY file that you need to update as per requirements
│   ├── inventory
│   │   └── hosts.ini   # inventory file, gets auto updated via ansible when new EC2 instances are launched after 0.provision.yml.
│   └── requirements.yml   # Required plugins for ansible.
└── kubernetes
    ├── README.md
    ├── backend
    │   ├── Dockerfile   # Dockerfile to build backend container image
    │   ├── app.py       # Sample python flask application file.
    │   └── requirements.txt #  Required python modules for building the image
    ├── frontend
    │   ├── Dockerfile   # Dockerfile to build frontend container image
    │   ├── index.html   # Config files for frontend application
    │   ├── nginx.conf   # Config files for frontend application
    │   ├── script.js    # Config files for frontend application
    │   └── style.css    # Config files for frontend application
    ├── 1.application.yaml    # kubectl apply -f 1.application.yaml => Installs backend,frontend and DB pods, service & loadbalancer. Make sure to update the images for  Front/backend if you build your own images.
    ├── 2.hpa.yaml       # Config files for HPA Horizontal Pod Autoscaler for both front/backend.
    ├── 3.network-policy.yaml  # Network policy to allow only frontend -> Backend -> DB flow.
    ├── 4.rbac.yaml      # Create user with specific permissions.
    └── 5.etcd-snapshot.sh  # Run this file to take ETCD Snapshot and verifiy it. You can run commands 1by1 as well.


## Step 1 : Preparation 

Only few AWS inputs are required in `ansible/group_vars/all.yml`:
- `aws_region`  # In which AWS Region you want to deploy the resources in lab/personal account.
- `vpc_id`      # should be present in your accocunt's region. If no VPC is visible, go to CREATE-VPC-> VPC and More -> It will auto create VPC, public/Private subnets, route table etc for you.
- `ami_id`      # This is important. Choose AMI ID based on if you want worker/master nodes to have Ubuntu/CentOS/AmazonLinux etc. 


- `control_plane_subnet_cidr`: "172.31.96.0/24"  # Replace with any subnet inside your VPC
- `worker_1_subnet_cidr`: # Replace with any subnet inside your VPC
- `worker_2_subnet_cidr`: # Replace with any subnet inside your VPC


VERY IMPORTANT #  that respective commands/package name will differ based on your instance AMI. For lab i have chose AmazonLinux 2023 which is RHEL based so "yum" packages work on it.  Also note that if you have amd64 based worker nodes you will need docker images which are build on amd64 terminal. Our Simplilearn Lab machin is not amd64 ( its ARM64 based archtecture) so if you build docker images on your lab machine and then deploy on worker nodes created by AmazonLinux2023 ( which is amd64 based) your pods will not come up. 


Ansible core only includes basic execution plugins. To manage specific infrastructure platforms, specialized modules and plugins are packaged into Collections:
* amazon.aws: Contains modules to manage AWS resources like EC2, S3, VPCs, IAM, and Security Groups.
community.general: Provides a broad suite of general utility modules maintained by the Ansible community (e.g., managing specific databases, system utilities, third-party software).
* community.crypto: Supplies modules and plugins for generating, managing, and signing SSL/TLS certificates, OpenSSL keys, and SSH credentials.
* kubernetes.core: Provides modules (k8s, k8s_info, helm, etc.) to interact directly with Kubernetes cluster APIs and manage Kubernetes manifests.

## Run the following command from your terminal: :  ansible-galaxy collection install -r requirements.yml


The provisioning playbook creates:
- Internet Gateway
- Public subnet
- Public route table and default route
- Security group
- Local SSH private/public key pair
- AWS EC2 key pair
- 3 EC2 instances
- Dynamic Ansible inventory

## Step 2 : Run

```bash
cd ansible
python3 -m pip install --user ansible boto3 botocore
ansible-galaxy collection install -r requirements.yml



ansible-playbook 0.provision.yml    # 


ansible all -m ping






```

After the cluster is healthy, continue with the Kubernetes manifests and etcd scripts.


ansible control_plane -m copy -a "src=../kubernetes/ dest=/home/ec2-user/kubernetes/"       # To copy k8s manifests from local to inside control plane node.

ssh -i ~/.ssh/easypay-k8s ec2-user@32.192.4.90              # To login inside control plane node.


# EasyPay Demo

This is a starter project for Kubernetes demos.

Contents:
- application.yaml (placeholder)
- backend/app.py
- frontend/index.html
- mysql/init.sql

This scaffold is intended to be extended into a full demo.



You need to first login to remote repository where you are planning to push the docker image : 

For Docker hub : you need username/repo-name and PAT ( PersonalAccessToken)
For Public AWS ECR Repo: aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/<<ECR_UNIQUE_ID>>
For Private Repo : aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <<AWS_ACCOUNT_ID>>.dkr.ecr.<<REGION>>>>.amazonaws.com

## Correct sequence :  Docker Login -> Docker Build -> Docker Tag ( with target Docker Repo Format) -> Docker Push

## For Backend Application : 
```
cd kubernetes/backend
docker build -t easypay-backend:v1 .       # Picks up application and Dockerfile from backend folder and builds a local image easypay-backend:v1.
docker tag easypay-backend:v1 saurabhnegi2306/easypay:backend-v1   # Tags/renames easypay-backend:v1 into saurabhnegi2306/easypay:backend-v1 as per docker Repo format.
docker push saurabhnegi2306/easypay:backend-v1                     # Pushes newly tagged image to dockerHub account names "saurabhnegi2306" and inside repo "easypay" with tag "backend-v1".

```
cd ../frontend
docker build -t easypay-frontend:v1 .      # Picks up application and Dockerfile from frontend folder and builds a local image easypay-frontend:v1.
docker tag easypay-frontend:v1 saurabhnegi2306/easypay:frontend-v1 # Tags/renames easypay-frontend:v1 into saurabhnegi2306/easypay:frontend-v1 as per docker Repo format.
docker push saurabhnegi2306/easypay:frontend-v1   # Pushes newly tagged image to dockerHub account names "saurabhnegi2306" and inside repo "easypay" with tag "frontend-v1".

Now you should have 2 docker images ready for use from your dockerhub container repository.

kubectl apply -f application.yaml