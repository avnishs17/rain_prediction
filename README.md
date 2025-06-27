# Australia Weather Rain Prediction MLOps Pipeline

This project demonstrates a complete MLOps pipeline for predicting rain in Australia using multiple CI/CD platforms. The application uses machine learning to predict whether it will rain tomorrow based on current weather conditions.

## 🌧️ Project Overview

The pipeline includes:
- **Data processing and model training** for Australian weather data
- **Interactive web application** with modern UI/UX for rain prediction
- **Docker containerization** for consistent deployment
- **Multiple CI/CD options**: GitHub Actions, CircleCI, and GitLab CI/CD
- **Artifact storage** in Google Artifact Registry
- **Deployment** to Google Kubernetes Engine (GKE)
- **Health monitoring** and probes for production readiness

## 🎯 Features

- **Smart Rain Prediction**: Uses 24 weather features including temperature, humidity, wind, and pressure
- **Beautiful UI**: Modern, responsive web interface with guided input fields
- **Real-time Predictions**: AJAX-powered predictions without page refresh
- **Input Validation**: Comprehensive field validation with helpful tooltips and examples
- **Production Ready**: Kubernetes deployment with health checks and resource management
- **Multiple Deployment Options**: Choose from GitHub Actions, CircleCI, or GitLab CI/CD

## 📋 Prerequisites

- **Google Cloud Platform account**
- **GCP Service account** with the following permissions:
  - Artifact Registry Administrator
  - Artifact Registry Writer
  - Owner
  - Storage Object Admin
  - Storage Object Viewer
- **CI/CD Platform account** (GitHub, CircleCI, or GitLab)

## 🚀 Quick Start

### 1. Google Cloud Platform Setup

#### 1.1 Create a GCP Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select project dropdown
3. Enter project name and ID
4. Click "Create"

#### 1.2 Create Artifact Registry Repository
1. Navigate to **Artifact Registry** in the GCP Console
2. Click **"Create Repository"**
3. Set the following:
   - **Name**: `rain-prediction`
   - **Format**: Docker
   - **Location**: `asia-south1` (or your preferred region)
   - **Description**: "Docker repository for Rain Prediction MLOps project"
4. Click **"Create"**

#### 1.3 Create GKE Cluster
1. Navigate to **Kubernetes Engine > Clusters**
2. Click **"Create Cluster"**
3. Choose **"Standard"** cluster
4. Configure cluster:
   - **Name**: `rain`
   - **Location**: Select your preferred zone in `asia-south1` (e.g., `asia-south1-a`)
   - **✅ Enable Cluster DNS** (tick this option)
5. Click **"Create"**

#### 1.4 Create Service Account
1. Navigate to **IAM & Admin > Service Accounts**
2. Click **"Create Service Account"**
3. Set details:
   - **Name**: `rain-prediction-service-account`
   - **Description**: "Service account for Rain Prediction CI/CD"
4. Click **"Create and Continue"**
5. Grant the required roles (listed above)
6. Click **"Continue"** then **"Done"**

#### 1.5 Download Service Account Key
1. In **Service Accounts**, find your service account
2. Click on the service account name
3. Go to **"Keys"** tab
4. Click **"Add Key" > "Create new key"**
5. Select **JSON** format
6. Click **"Create"**
7. **Keep this file secure - DO NOT commit to version control**

## 🔧 CI/CD Setup Options

Choose one of the following CI/CD platforms:

---

## 📱 Option A: GitHub Actions (Recommended)

### Setup Steps

#### A.1 Configure GitHub Secrets
In your GitHub repository settings, add these secrets:

- **GCP_SA_KEY**: Paste the entire JSON content from your service account key file
- **GCP_PROJECT_ID**: Your Google Cloud project ID

#### A.2 Setting GitHub Secrets
1. Go to your GitHub repository
2. Click on "Settings" tab
3. Navigate to "Secrets and variables" > "Actions"
4. Click "New repository secret"
5. Add each secret with its corresponding value

#### A.3 Workflow Configuration
The GitHub Actions workflow (`.github/workflows/deploy.yaml`) is already configured with:
- **Cluster**: `rain`
- **Region**: `asia-south1`
- **Registry**: `asia-south1-docker.pkg.dev`

### Deployment Process
Push changes to the `main` branch to trigger automatic deployment.

---

## 🔵 Option B: CircleCI

### Setup Steps

#### B.1 Connect Repository to CircleCI
1. Go to [CircleCI](https://circleci.com/)
2. Sign in with your GitHub/GitLab account
3. Add your project repository

#### B.2 Configure Environment Variables
In your CircleCI project settings, add:

1. **GCLOUD_SERVICE_KEY**
   ```bash
   # Generate base64 encoded service account key
   cat gcp-key.json | base64 -w 0
   ```

2. **GOOGLE_PROJECT_ID**: Your project ID
3. **GKE_CLUSTER**: `rain`
4. **GOOGLE_COMPUTE_ZONE**: `asia-south1-a` (or your chosen zone)

#### B.3 Setting Environment Variables in CircleCI
1. Go to your project in CircleCI
2. Click on "Project Settings"
3. Navigate to "Environment Variables"
4. Click "Add Environment Variable"
5. Add each variable with its corresponding value

### Deployment Process
Push changes to trigger the CircleCI pipeline automatically.

---

## 🦊 Option C: GitLab CI/CD

### Setup Steps

#### C.1 Account Verification (Required)
**Important**: Verify your GitLab account with either:
- Mobile phone number, OR
- Credit card information

#### C.2 Push Repository to GitLab
```bash
git remote add origin <your-gitlab-repository-url>
git push -u origin main
```

#### C.3 Configure CI/CD Variables
In your GitLab project settings, add:

1. **GCP_SA_KEY**
   ```bash
   # Generate base64 encoded service account key
   cat gcp-key.json | base64 -w 0
   ```

#### C.4 Setting CI/CD Variables in GitLab
1. Go to your GitLab project
2. Navigate to **Settings > CI/CD**
3. Expand **Variables** section
4. Click **"Add variable"**
5. Set:
   - **Protect variable**: ✅
   - **Mask variable**: ✅ (for sensitive data)

#### C.5 Update Configuration Files
Update `.gitlab-ci.yml` and `kubernetes-deployment.yaml` with your specific GCP details.

### Deployment Process
Push changes to trigger the GitLab CI/CD pipeline automatically.

---

## 💻 Local Development Setup

### 1. Clone and Setup Project
```bash
git clone <your-repository-url>
cd rain_prediction

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Data Processing
```bash
python src/data_processing.py
```

### 3. Run Flask Application Locally
```bash
python app.py
```

Access the application at `http://localhost:5000`

## 🌐 Application Features

### Input Fields
The application accepts 24 weather parameters:

**Location & Time**
- Location (49 Australian weather stations)
- Year, Month, Day

**Temperature**
- Min/Max temperature
- 9 AM and 3 PM temperatures

**Rainfall & Weather**
- Rainfall amount, Rain today status
- Evaporation, Sunshine hours

**Wind Conditions**
- Wind direction and speed (9 AM and 3 PM)
- Wind gust direction and speed

**Atmospheric Conditions**
- Humidity, Pressure, Cloud cover (9 AM and 3 PM)

### User Experience
- **Guided Input**: Each field includes description, example values, and valid ranges
- **Real-time Validation**: Instant feedback on input values
- **No Page Refresh**: AJAX-powered predictions with smooth animations
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: Clear error messages and recovery guidance

## 📊 Monitoring and Verification

### Check Deployment Status
Monitor your chosen CI/CD platform:
- **GitHub Actions**: Check "Actions" tab in your repository
- **CircleCI**: Monitor builds in CircleCI dashboard
- **GitLab CI/CD**: Check "CI/CD > Pipelines" in your project

### Access Application
1. Go to **Google Cloud Console > Kubernetes Engine > Services & Ingress**
2. Find the `mlops-service`
3. Note the **External IP address**
4. Access the application at `http://<EXTERNAL-IP>`

### Health Monitoring
The application includes:
- **Health endpoint**: `/health` for Kubernetes probes
- **Liveness probes**: Automatic restart if unhealthy
- **Readiness probes**: Traffic routing control
- **Resource limits**: Memory and CPU constraints

## 📁 Project Structure

```
rain_prediction/
├── .github/workflows/          # GitHub Actions CI/CD
│   └── deploy.yaml
├── .circleci/                  # CircleCI configuration
│   └── config.yml
├── .gitlab-ci.yml             # GitLab CI/CD configuration
├── artifacts/                 # Model artifacts and data
│   ├── processed/             # Processed datasets
│   └── raw/                   # Raw data
├── src/                       # Source code modules
│   ├── data_processing.py     # Data processing pipeline
│   ├── logger.py              # Logging configuration
│   └── custom_exception.py    # Exception handling
├── static/                    # Static web assets
│   └── style.css             # Application styling
├── templates/                 # HTML templates
│   └── index.html            # Main application page
├── app.py                     # Flask application
├── Dockerfile                 # Docker configuration
├── kubernetes-deployment.yaml # Kubernetes manifests
├── requirements.txt          # Python dependencies
└── setup.py                  # Package setup
```

## 🔒 Security Notes

- **Never commit** service account keys to version control
- **Store secrets** in your CI/CD platform's secure storage
- **Use least privilege** principle for service account permissions
- **Regularly rotate** service account keys
- **Review permissions** regularly and remove unused access

## 🛠️ Troubleshooting

### Common Issues

#### 1. Authentication Errors
- Verify service account has correct permissions
- Check if secrets are properly formatted and accessible
- Ensure service account email matches the key file

#### 2. Docker Push Failures
- Confirm Artifact Registry repository exists
- Verify repository permissions and region
- Check Docker authentication configuration

#### 3. GKE Deployment Issues
- Ensure cluster exists and is accessible
- Verify kubectl configuration
- Check Kubernetes deployment YAML syntax
- Monitor cluster resources and quotas

#### 4. Application Not Accessible
- Check service external IP assignment
- Verify firewall rules allow traffic
- Review pod logs for application errors
- Confirm service and deployment are running

#### 5. Model Loading Issues
- Ensure model artifacts are present in the container
- Check file paths and permissions
- Verify model format compatibility

### Getting Help

If you encounter issues:
1. Check the CI/CD platform logs for specific error messages
2. Review Google Cloud Console for GKE cluster status
3. Monitor application logs in Kubernetes
4. Verify all configuration files match your setup

## 🎉 Success!

Once deployed successfully, you'll have a production-ready machine learning application that can predict Australian weather patterns with a beautiful, user-friendly interface!

The application demonstrates modern MLOps practices including:
- ✅ Containerized deployment
- ✅ Automated CI/CD pipeline
- ✅ Kubernetes orchestration
- ✅ Health monitoring
- ✅ Scalable architecture
- ✅ User-friendly interface

---