[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/97WR5HaV)

# Kubernetes Flask Application with PostgreSQL

This project demonstrates how to deploy a Flask application with a PostgreSQL database on a Kubernetes cluster using Minikube.

## Prerequisites

- Minikube
- kubectl
- Docker

## Directory Structure

```
k8s-flask-app/
│── manifests/
│   │── deployment/
│   │   │── flask-deployment.yaml
│   │   │── postgres-deployment.yaml
│   │── service/
│   │   │── flask-service.yaml
│   │   │── postgres-service.yaml
│   │── configmap/
│   │   │── postgres-configmap.yaml
│   │── secret/
│   │   │── postgres-secret.yaml
│── app/
│   │── Dockerfile
│   │── requirements.txt
│   │── app.py
│── README.md
```

## Setup Instructions

### 1. Start Minikube

```bash
minikube start
```

### 2. Enable the Minikube Docker environment

```bash
eval $(minikube docker-env)
```

### 3. Build the Flask application Docker image

```bash
cd app
docker build -t flask-app:latest .
cd ..
```

### 4. Deploy PostgreSQL

```bash
kubectl apply -f manifests/configmap/postgres-configmap.yaml
kubectl apply -f manifests/secret/postgres-secret.yaml
kubectl apply -f manifests/deployment/postgres-deployment.yaml
kubectl apply -f manifests/service/postgres-service.yaml
```

### 5. Deploy the Flask application

```bash
kubectl apply -f manifests/deployment/flask-deployment.yaml
kubectl apply -f manifests/service/flask-service.yaml
```

### 6. Access the application

```bash
minikube service flask-app
```

## Testing

1. Access the root endpoint to verify the application is running:
   - `http://<minikube-ip>:<node-port>/`

2. Test the database connection:
   - `http://<minikube-ip>:<node-port>/db-test`

## Scaling the Application

You can scale the Flask application by changing the number of replicas:

```bash
kubectl scale deployment flask-app --replicas=3
```

## Cleanup

To delete all resources:

```bash
kubectl delete -f manifests/
minikube stop
```
