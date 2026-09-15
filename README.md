# Iris Classification MLOps Pipeline

An end-to-end MLOps project for Iris classification with **data drift monitoring, automated retraining, model validation, security scanning, Docker, GitHub Actions, Docker Hub, and Kubernetes**.

---

## 🚀 Project Overview

This project demonstrates how a machine learning application can be taken from model development through automated testing, security scanning, containerization, Docker image publishing, and Kubernetes deployment.

The project includes:

* Data drift monitoring
* Conditional model retraining
* Model validation
* Unit and API testing
* SAST using Semgrep
* SCA/configuration scanning using Trivy
* DAST using OWASP ZAP
* Docker containerization
* GitHub Actions CI/CD
* Docker Hub image publishing
* Kubernetes deployment manifests

---

## 🏗️ Architecture

```text
                         Git Push
                            │
                            ▼
                    ┌───────────────┐
                    │    GitHub     │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ GitHub Actions│
                    └───────┬───────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       Drift Check      Security        Testing
             │            Scanning          │
             ▼              │               ▼
       Retraining           │          Model/API Tests
             │              │
             └──────────────┼──────────────┘
                            ▼
                    ┌───────────────┐
                    │ Docker Build  │
                    └───────┬───────┘
                            ▼
                    Docker Container
                         Testing
                            │
                            ▼
                    ┌───────────────┐
                    │   Docker Hub   │
                    └───────┬───────┘
                            ▼
                  Update Kubernetes
                       Manifest
                            │
                            ▼
                     Kubernetes /
                       Minikube
```

---

# 🛠️ Technologies Used

* **Python 3.10**
* **FastAPI**
* **Scikit-learn**
* **NumPy**
* **SciPy**
* **Joblib**
* **Pytest**
* **Docker**
* **GitHub Actions**
* **Docker Hub**
* **Kubernetes**
* **Minikube**
* **Semgrep**
* **Trivy**
* **OWASP ZAP**

---

# 📁 Project Structure

```text
AI-MLOps-Iris-Classification/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── k8s/
│   ├── deployment.yml
│   └── service.yml
│
├── tests/
│   └── test_model.py
│
├── app.py
├── drift_monitor.py
├── retrain.py
├── validate_model.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

`model.pkl` is generated locally during model training/retraining and is excluded from Git using `.gitignore`.

---

# 🤖 Machine Learning Application

The project uses the **Iris dataset** with a Random Forest classification model.

The model artifact is saved as:

```text
model.pkl
```

The API accepts four Iris features:

```text
1. Sepal length
2. Sepal width
3. Petal length
4. Petal width
```

Example input:

```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

---

# 🔄 Data Drift Monitoring

Data drift is monitored using the **Kolmogorov-Smirnov (KS) test**.

The `drift_monitor.py` script compares reference data with current data and checks each feature using:

```text
p-value < 0.05
```

as the drift threshold.

### Run locally

```bash
python drift_monitor.py
```

Example output:

```text
Running Data Drift Check (KS-Test)...
Drift detected in feature 0
Drift detected in feature 1
Drift detected in feature 2
Feature 3 stable
```

The drift result is passed to GitHub Actions using the `GITHUB_OUTPUT` environment variable.

---

# 🔁 Automated Model Retraining

When data drift is detected, GitHub Actions conditionally executes:

```text
retrain.py
```

The script trains a new Random Forest model and saves:

```text
model.pkl
```

Run manually:

```bash
python retrain.py
```

---

# ✅ Model Validation

The trained model is validated using the Iris dataset.

The validation script:

```text
validate_model.py
```

calculates model accuracy.

The pipeline fails if the accuracy is below:

```text
0.90
```

Run locally:

```bash
python validate_model.py
```

---

# 🧪 Testing

Unit tests are located in:

```text
tests/test_model.py
```

Run the tests:

```bash
pytest
```

The GitHub Actions workflow also performs FastAPI smoke and integration tests.

---

# 🌐 FastAPI

The application provides two main endpoints.

### Health Check

```text
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Prediction

```text
POST /predict
```

Example request:

```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

Example response:

```json
{
  "model_version": "1.0.0",
  "prediction": 0
}
```

FastAPI Swagger documentation is available at:

```text
/docs
```

when the application is running.

---

# 🔐 Security Scanning

Security checks were performed using three tools:

```text
SAST → Semgrep
SCA / Configuration Scanning → Trivy
DAST → OWASP ZAP
```

---

## 1. SAST — Semgrep

Semgrep was used for Static Application Security Testing.

From the project directory:

```cmd
docker run --rm -v "%cd%:/src" semgrep/semgrep semgrep scan --config p/python --exclude v1 /src
```

The scan completed with:

```text
Findings: 0
```

---

## 2. SCA / Configuration Scanning — Trivy

Trivy was used for security scanning of the project configuration/filesystem.

### Trivy configuration scan

From the project directory:

```cmd
docker run --rm -v "%cd%:/src" aquasec/trivy:latest config /src
```

Trivy was also tested against the project filesystem for vulnerability scanning.

Example:

```cmd
docker run --rm -v "%cd%:/src" aquasec/trivy:latest fs --scanners vuln /src
```

The Trivy scans were performed as part of the project's security assessment.

---

## 3. DAST — OWASP ZAP

OWASP ZAP was used for Dynamic Application Security Testing against the running FastAPI application.

Example:

```cmd
docker run --rm -v "%cd%:/zap/wrk/:rw" zaproxy/zap-stable zap-baseline.py -t http://host.docker.internal:8000 -r zap_report.html
```

The scan reported:

```text
High: 0
Medium: 0
Low: 0
Informational: 1
```

The informational finding was related to storable/cacheable content on endpoints returning `404`.

The generated report is:

```text
zap_report.html
```

---

# 🐳 Docker

The application is containerized using Docker.

## Build Docker image

```cmd
docker build -t iris-mlops-api:latest .
```

## Run Docker container

```cmd
docker run -d --name iris-mlops-container -p 8000:8000 iris-mlops-api:latest
```

## Test health endpoint

```cmd
curl http://localhost:8000/health
```

## Test prediction endpoint

```cmd
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"features\":[5.1,3.5,1.4,0.2]}"
```

---

# 📦 Docker Hub

The Docker image is published to:

```text
stelabiju/iris-mlops-api
```

GitHub Actions creates a Docker image using the Git commit SHA as the image tag.

Example:

```text
stelabiju/iris-mlops-api:<commit-sha>
```

Using the Git SHA provides a unique image version for each pipeline execution.

---

# ⚙️ GitHub Actions CI/CD

The workflow is located at:

```text
.github/workflows/deploy.yml
```

The automated pipeline performs:

```text
1. Checkout source code
2. Set up Python
3. Install dependencies
4. Check data drift
5. Retrain model when drift is detected
6. Validate model
7. Run unit tests
8. Run FastAPI tests
9. Build Docker image
10. Run Docker container
11. Test Docker container
12. Login to Docker Hub
13. Push Docker image
14. Update Kubernetes deployment image
15. Commit updated Kubernetes manifest
16. Push updated manifest to GitHub
```

The workflow uses GitHub Actions' repository write permission to commit the updated Kubernetes manifest.

---

# ☸️ Kubernetes

Kubernetes configuration is stored under:

```text
k8s/
├── deployment.yml
└── service.yml
```

## Deployment

The application is deployed as:

```text
iris-mlops-api
```

The deployment uses the Docker image published to Docker Hub.

The GitHub Actions workflow automatically updates the image tag in `deployment.yml` to the latest Git commit SHA.

## Service

The application is exposed using a Kubernetes `NodePort` service:

```text
iris-mlops-service
```

---

# 🚢 Deploy to Minikube

Start Minikube:

```cmd
minikube start
```

Apply the deployment:

```cmd
kubectl apply -f k8s/deployment.yml
```

Apply the service:

```cmd
kubectl apply -f k8s/service.yml
```

Check deployments:

```cmd
kubectl get deployments
```

Check pods:

```cmd
kubectl get pods
```

Check services:

```cmd
kubectl get svc
```

Open the service:

```cmd
minikube service iris-mlops-service
```

---

# 🔄 Complete MLOps Flow

```text
Developer
    │
    │ git push
    ▼
GitHub
    │
    ▼
GitHub Actions
    │
    ├── Data Drift Detection
    │
    ├── Conditional Retraining
    │
    ├── Model Validation
    │
    ├── Unit Tests
    │
    ├── API Tests
    │
    ├── SAST - Semgrep
    │
    ├── SCA / Config Scan - Trivy
    │
    ├── DAST - OWASP ZAP
    │
    ├── Docker Build
    │
    └── Docker Container Test
    │
    ▼
Docker Hub
    │
    │ Versioned Docker Image
    ▼
Kubernetes Manifest
    │
    ▼
Minikube / Kubernetes
    │
    ▼
Iris Classification API
```

---

# 🖥️ Useful Command-Line References

## Check Current Directory

### Windows CMD

```cmd
cd
```

### PowerShell

```powershell
Get-Location
```

### Linux / Git Bash

```bash
pwd
```

---

## Change Directory

### Windows CMD

```cmd
cd C:\Users\user\Downloads\ml-lab-project
```

### PowerShell

```powershell
cd C:\Users\user\Downloads\ml-lab-project
```

### Linux / Git Bash

```bash
cd /path/to/ml-lab-project
```

---

## Example Project Navigation

Windows:

```cmd
cd C:\Users\user\Downloads\ml-lab-project
```

Check the current directory:

```cmd
cd
```

Then run Docker security scans from the project root:

```cmd
docker run --rm -v "%cd%:/src" aquasec/trivy:latest config /src
```

---

# 🎯 Project Goals

This project demonstrates practical implementation of:

* Machine learning model serving
* Data drift detection
* Automated model retraining
* Model validation
* Unit testing
* API testing
* Static security analysis
* Software/configuration security scanning
* Dynamic security testing
* Docker containerization
* Docker image versioning
* CI/CD using GitHub Actions
* Docker Hub integration
* Kubernetes deployment configuration

---

## 👩‍💻 Author

**Stella Biju**

B.Tech Computer Science

GitHub: [stelabiju](https://github.com/stelabiju)
