# devops-2025S-demo

Class demo for DevOps: GitHub, Docker, Terraform, AWS ECR, and Kubernetes.

## CI/CD Overview

- Source code is hosted on GitHub.
- GitHub Actions builds the Docker image and pushes it to a private AWS ECR repository:
  - Uses repository secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, `ECR_REGISTRY`.
  - Image is tagged with the commit SHA.
- Terraform is used to provision the ECR repository and to store state in Terraform Cloud.

## Local Kubernetes Deployment (Docker Desktop)

These steps run the Campus Notifier app on a local Kubernetes cluster provided by Docker Desktop.

### Prerequisites

- Docker Desktop with **Kubernetes enabled**.
- `kubectl` installed and current context set to `docker-desktop`:

```bash
kubectl config current-context
kubectl get nodes
```

You should see `docker-desktop` and one node in `Ready` state.

### 1. Build the Docker Image Locally

From the project root (`devops-2025S-demo`):

```bash
docker build -t my-k8s-app:latest .
```

The Kubernetes `Deployment` uses this local image (`my-k8s-app:latest`) when running on Docker Desktop.

### 2. Apply Kubernetes Manifests

Apply the deployment and service manifests:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Check that the pod and service are created:

```bash
kubectl get pods
kubectl get service my-app-service
```

You should see:
- A pod named similar to `my-app-xxxxx` with `STATUS` = `Running`.
- A service `my-app-service` of type `LoadBalancer` with `EXTERNAL-IP` = `localhost` and a node port (e.g. `80:30503/TCP`).

### 3. Run Database Migrations Inside the Pod

Run Django migrations so the database tables are created.

First, get the pod name:

```bash
kubectl get pods

# Example output:
# NAME                      READY   STATUS    AGE
# my-app-556b6d9bc9-7bg5c   1/1     Running   5m

# Use the pod name from the first column:
kubectl exec -it my-app-556b6d9bc9-7bg5c -- python manage.py migrate
```

> Note: the pod name changes whenever Kubernetes recreates the pod. Always copy the
> current pod name from `kubectl get pods` instead of hard-coding it.

### 4. Access the App

Open the app in your browser using the node port shown in the service:

```text
http://localhost:<node-port>/
```

Example (from the lab):

```text
http://localhost:30503/
```

You should see the **Campus Notifier** UI with the "Upcoming Events" page.

### 5. Clean Up

To remove the resources from the cluster:

```bash
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
```

Optionally, remove the local image:

```bash
docker rmi my-k8s-app:latest
```

