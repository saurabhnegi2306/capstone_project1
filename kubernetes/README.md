# EasyPay Demo

This is a starter project for Kubernetes demos.

Contents:
- application.yaml (placeholder)
- backend/app.py
- frontend/index.html
- mysql/init.sql

This scaffold is intended to be extended into a full demo.


docker login <<DOCKERHUB/ECR>>
docker build -t easypay-backend:v1 ./backend/
docker tag easypay-backend:v1 saurabhnegi2306/easypay:backend-v1
docker push saurabhnegi2306/easypay:backend-v1


docker build -t easypay-frontend:v1 ./frontend/
docker tag easypay-frontend:v1 saurabhnegi2306/easypay:frontend-v1
docker push saurabhnegi2306/easypay:frontend-v1


kubectl apply -f application.yaml