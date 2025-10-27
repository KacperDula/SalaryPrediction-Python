# 💼 Salary Prediction App (Python + ML)

A machine learning web application that predicts salaries based on various input features such as experience, education level, and job position.  
Built with **Python**, **Flask**, **Docker**, and deployed using **Firebase Hosting + Google Cloud Run** for 24/7 uptime.

---

## 🚀 Features

- 🧠 Machine Learning salary prediction model  
- 🌐 Flask-based web interface  
- 🐳 Dockerized for portability and easy deployment  
- ☁️ Runs continuously on Firebase + Cloud Run  
- 📊 Clean, modular, and production-ready structure  

---

## 📂 Project Structure

```
SalaryPrediction-Python/
│
├── app.py                # Main Flask app
├── model/                # Model training and inference logic
├── static/               # Static assets (CSS, JS, images)
├── templates/            # HTML templates
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── start.sh              # App start script
├── firebase.json         # Firebase Hosting config
└── README.md             # Project documentation
```

---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/KacperDula/SalaryPrediction-Python.git
cd SalaryPrediction-Python
```

### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

### 3️⃣ Run the Application
```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 🐳 Run Using Docker

### Build Image
```bash
docker build -t salary-prediction .
```

### Run Container
```bash
docker run -d -p 8080:8080 salary-prediction
```

Visit: [http://localhost:8080](http://localhost:8080)

> Ensure your Flask app runs with:
> ```python
> app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
> ```

---

## ☁️ Deploy to Firebase + Cloud Run (Always-On Hosting)

### Prerequisites
- Firebase project (Blaze plan)
- Installed Firebase CLI and Google Cloud SDK:
  ```bash
  npm install -g firebase-tools
  curl https://sdk.cloud.google.com | bash
  ```

- Authenticate:
  ```bash
  gcloud auth login
  firebase login
  ```

---

### 1️⃣ Enable Required Services
```bash
gcloud services enable run.googleapis.com   artifactregistry.googleapis.com   cloudbuild.googleapis.com   firebasehosting.googleapis.com
```

---

### 2️⃣ Build & Push Image to Artifact Registry
```bash
gcloud builds submit   --tag us-central1-docker.pkg.dev/<GCP_PROJECT_ID>/app-images/salarypred:1
```

---

### 3️⃣ Deploy to Cloud Run
```bash
gcloud run deploy salarypred   --image us-central1-docker.pkg.dev/<GCP_PROJECT_ID>/app-images/salarypred:1   --platform managed   --region us-central1   --allow-unauthenticated   --port 8080   --min-instances 1   --max-instances 3
```

> `--min-instances 1` keeps the app alive 24/7.

---

### 4️⃣ Connect Firebase Hosting

Initialize Firebase Hosting:
```bash
firebase init hosting
```

Update your `firebase.json`:
```json
{
  "hosting": {
    "public": "public",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      {
        "source": "**",
        "run": {
          "serviceId": "salarypred",
          "region": "us-central1"
        }
      }
    ]
  }
}
```

Deploy Firebase Hosting:
```bash
firebase deploy --only hosting
```

Access your app via:
```
https://<your-project>.web.app
```

---

## 🧰 Tech Stack

| Category | Technology |
|-----------|-------------|
| **Language** | Python 3 |
| **Framework** | Flask |
| **Machine Learning** | scikit-learn, pandas, numpy |
| **Frontend** | HTML, CSS, Bootstrap |
| **Containerization** | Docker |
| **Hosting** | Firebase Hosting + Google Cloud Run |
| **Version Control** | Git & GitHub |

---

## 🧑‍💻 Development Notes

- Modify and retrain the ML model under the `model/` directory.  
- Ensure consistent Python versions between local and deployment environments.  
- Store sensitive info (API keys, etc.) as environment variables.

---

## 🤝 Contributing

1. Fork the repository  
2. Create a feature branch: `git checkout -b feature/your-feature`  
3. Commit your changes  
4. Push and create a Pull Request  

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).  
You’re free to use and modify it with attribution.

---

## 📧 Contact

**Author:** [Kacper Dula](https://github.com/KacperDula)  
For questions or suggestions, open an [issue](https://github.com/KacperDula/SalaryPrediction-Python/issues).

---

⭐ **If you like this project, please give it a star on GitHub!**
