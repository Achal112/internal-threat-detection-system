# 🛡️ AI-Based Internal Threat Detection System

An AI-powered cybersecurity application that detects potential insider threats by analyzing user behavior, calculating behavioral risk scores, and identifying anomalous activities. The system provides real-time monitoring through an interactive dashboard to help organizations strengthen internal security.

---

## 🚀 Features

- 🔍 Detects insider threats using behavioral analysis
- 📊 Generates dynamic behavioral risk scores
- ⚠️ Identifies anomalous user activities
- 📈 Interactive Streamlit dashboard for monitoring
- 🗄️ SQLite-based event storage and management
- 🤖 Machine Learning-assisted risk analysis
- 📅 Threat timeline visualization
- 📢 Automated security alerts for high-risk events

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Frontend | Streamlit |
| Database | SQLite |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```text
internal-threat-detection-system/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│   ├── database.py
│   ├── schema.py
│
├── modules/
│   ├── activity_simulator.py
│   ├── risk_engine.py
│   ├── baseline_seed.py
│
├── assets/
│   ├── dashboard.png
│   └── architecture.png
│
└── research/
    └── paper.pdf
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Achal112/internal-threat-detection-system.git
```

Move into the project directory

```bash
cd internal-threat-detection-system
```

Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will launch in your default browser.

---

## 📊 Project Workflow

1. Simulate user activities
2. Store activity logs in SQLite
3. Analyze behavioral patterns
4. Calculate behavioral risk scores
5. Detect anomalies
6. Generate alerts
7. Visualize insights on the dashboard

---

## 📸 Dashboard Preview

Add screenshots inside the **asset** folder and display them here.

```markdown
![Dashboard](asset/dashboard.png)
```

---

## 📖 Research Publication

This project forms the basis of a published research paper on AI-based insider threat detection using behavioral risk analysis and machine learning.

---

## 🔮 Future Enhancements

- Deep Learning-based anomaly detection
- Real-time log ingestion
- Role-Based Access Control (RBAC)
- Email/SMS alert integration
- SIEM integration
- Docker deployment
- Cloud deployment on AWS

---

## 💡 Skills Demonstrated

- Python Programming
- Object-Oriented Programming
- Machine Learning
- Behavioral Analytics
- Cybersecurity
- Risk Analysis
- SQLite Database
- Data Processing
- Streamlit Development
- Software Design
- Git & GitHub

---

## 👩‍💻 Author

**Achal Laxman Deshmukh**

- LinkedIn: https://linkedin.com/in/deshmukhachal11
- GitHub: https://github.com/Achal112

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
