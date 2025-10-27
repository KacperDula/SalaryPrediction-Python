# Deploying the Streamlit App to Google Cloud Run with Firebase Hosting

These steps package the Streamlit salary predictor into a container, deploy it to Cloud Run for 24/7 availability, and optionally front the service with a Firebase Hosting rewrite.

## 1. Prerequisites
- Google Cloud project with billing enabled.
- Firebase project linked to the same Google Cloud project (only needed for the optional rewrite).
- Local tools: `gcloud`, `firebase-tools`, and Docker (or Cloud Build) installed and authenticated.

Authenticate once:
```bash
gcloud auth login
gcloud auth application-default login
firebase login
```

Set the active project (replace `PROJECT_ID`):
```bash
gcloud config set project PROJECT_ID
firebase use PROJECT_ID
```

## 2. Build the Container Image
Run from the repository root.

With Docker:
```bash
docker build -t gcr.io/PROJECT_ID/salary-predictor .
docker push gcr.io/PROJECT_ID/salary-predictor
```

Without Docker (Cloud Build):
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/salary-predictor
```

## 3. Deploy to Cloud Run
Choose a region (e.g. `us-central1`) and deploy:
```bash
gcloud run deploy salary-predictor \
  --image gcr.io/PROJECT_ID/salary-predictor \
  --region REGION \
  --platform managed \
  --allow-unauthenticated
```

Cloud Run returns a service URL such as `https://salary-predictor-xxxxx-uc.a.run.app`. This URL is already publicly accessible and HTTPS enabled.

## 4. (Optional) Proxy via Firebase Hosting
If you want your Firebase-hosted site to surface the app, add a rewrite in `firebase.json`:
```json
{
  "hosting": {
    "public": "public",
    "rewrites": [
      {
        "source": "**",
        "run": {
          "serviceId": "salary-predictor",
          "region": "REGION"
        }
      }
    ]
  }
}
```

Deploy the updated Hosting config:
```bash
firebase deploy --only hosting
```

## 5. Verification & Maintenance
- Use `gcloud run services describe salary-predictor --region REGION` to review logs and settings.
- Scale settings can be tuned with `--min-instances` if you want to keep at least one container warm.
- Update the deployment by rebuilding the container and re-running the Cloud Run deploy command.
