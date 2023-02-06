# AskMate with Jenkins pipeline

**AskMate is a project we created in the Web module of Codecool, a Q&A application (similar to StackOverflow but more basic)
My goal was to dockerize and deploy the app with a Jenkins pipeline and create an infrastructure for it**

---

## Technologies
- Jenkins
- Terraform
- Docker
- Kubernetes
- Helm
- AWS

## Tasks
The infrastructure is created with Terraform.
The app uses PostgreSQL to store data, it is deployed separately from the app and uses persistent storage on AWS to retain data.
The app is packaged into a Helm chart.
The Helm Chart and the Docker images are pushed to ECR in AWS
