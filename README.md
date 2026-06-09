# DataSanct - AI-Powered Intelligent Data Profiling & Cleaning Platform

🌐 **Live Demo:** https://data-sanct.vercel.app/

<img width="1024" height="572" alt="DataSanct" src="https://github.com/user-attachments/assets/9750b3a2-2a3c-45f7-b36c-7c70aafa36f2" />

---

## 📖 Overview

**DataSanct** is an AI-powered intelligent data cleaning and profiling platform that automates the process of analyzing, validating, cleaning, and transforming structured and image-based datasets.

The system combines **LLM-assisted reasoning** with **deterministic Python execution**, ensuring intelligent recommendations while maintaining secure, reproducible, and transparent data transformations.

DataSanct supports **CSV, Excel, and image datasets**, providing comprehensive profiling reports, automated cleaning, validation logs, and downloadable cleaned outputs.

---

## 🚀 Features

### 📊 Intelligent Data Profiling

- Exploratory Data Analysis (EDA)
- Dataset statistics and summaries
- Structural analysis
- Data quality assessment
- Missing value detection
- Duplicate identification
- Outlier analysis

### 🤖 AI-Assisted Cleaning Recommendations

- Understands dataset context using an LLM interaction layer
- Suggests appropriate cleaning strategies
- Recommends preprocessing actions based on data characteristics

### 🧹 Automated Data Cleaning

#### Tabular Data

- Missing value handling
- Text normalization
- Duplicate removal
- Data standardization
- Categorization
- PII reduction

#### Image Data

- Image validation
- Quality filtering
- Resizing
- Normalization
- Preprocessing

### ✅ Validation & Auditing

- Tracks every transformation
- Generates before/after diffs
- Creates audit logs
- Ensures transparent and reproducible cleaning

### 📈 Reporting & Visualization

- Data profiling reports
- Before vs after comparison
- Cleaning summaries
- Quality metrics visualization

### 💾 Clean Data Export

Processed datasets are ready for:

- Machine Learning
- Data Analytics
- Business Intelligence
- ETL Pipelines

---

# 🏗️ Architecture

```
                           User
                             │
           Upload / Download / View Results
                             │
                             ▼
                    Streamlit Frontend UI
                             │
                        JSON API Calls
                             │
                             ▼
                  FastAPI Backend Service
               (Backend Logic & Orchestration)
                             │
      ┌──────────────────────┼──────────────────────┐
      │                      │                      │
      ▼                      ▼                      ▼

Data Profiling        LLM Interaction        Cleaning Engine
 & Analysis Layer          Layer             (Safe Python)

      │                      │                      │
      │          Cleaning Suggestions              │
      └──────────────────────┼──────────────────────┘
                             │
                             ▼

                 Validation & Auditing System

                             │
      ┌──────────────────────┼──────────────────────┐
      │                      │                      │
      ▼                      ▼                      ▼

 Profile Reports      Clean Data Storage      Audit Logs
 & Visualization      (ML / Analytics)        & Diffs
```

---

# ⚙️ Tech Stack

## Frontend

- Streamlit
- HTML/CSS
- Python

## Backend

- FastAPI
- Python REST APIs

## AI Layer

- OpenAI LLM API
- Prompt Engineering
- Intelligent Cleaning Recommendation Engine

## Data Processing

- Pandas
- NumPy

## Image Processing

- OpenCV
- Pillow

## Validation

- Safe Python Functions
- Audit Log Generation
- Diff Tracking

## Deployment

- Vercel
- FastAPI Backend Services

---

# 🔄 Workflow

```
Upload Dataset
      │
      ▼
Frontend Interface
      │
      ▼
FastAPI Backend
      │
      ▼
Data Profiling Engine
      │
      ▼
LLM Understanding Layer
      │
      ▼
Cleaning Recommendations
      │
      ▼
Cleaning Execution Engine
      │
      ▼
Validation & Auditing
      │
      ▼
Generate Reports
      │
      ▼
Download Clean Dataset
```

---

# 📂 Project Structure

```
DataSanct/

├── client/
│   ├── UI Components
│   ├── Upload Interface
│   └── Visualization
│
├── server/
│   ├── FastAPI Backend
│   ├── API Routes
│   ├── Data Profiling
│   ├── Cleaning Engine
│   ├── Validation Engine
│   └── LLM Integration
│
├── reports/
│   ├── Profiling Reports
│   ├── Audit Logs
│   └── Visualization
│
└── storage/
    └── Clean Processed Data
```

---

# 🛠️ Installation

## Clone Repository

```bash
git clone https://github.com/Ramya-Pravallika/DataSanct.git

cd DataSanct
```

---

## Backend Setup

```bash
cd server

pip install -r requirements.txt

python main.py
```

---

## Frontend Setup

```bash
cd client

npm install

npm run dev
```

---

# ▶️ Usage

1. Upload a **CSV**, **Excel**, or **image dataset**.
2. The system performs **data profiling and quality analysis**.
3. The **AI interaction layer** recommends cleaning strategies.
4. The cleaning engine safely applies transformations.
5. Validation and auditing modules record all changes.
6. Review profiling reports and download the cleaned dataset.

---

# 🔒 Design Principles

- AI-assisted decision making
- Safe deterministic execution
- Transparent audit trail
- Explainable cleaning workflow
- Reproducible data transformations
- Production-ready architecture

---

# 🌟 Use Cases

- Data preprocessing for Machine Learning
- Data quality management
- Business Intelligence
- ETL workflows
- Research datasets
- Enterprise analytics
- Data governance

---

# 🚀 Future Roadmap

- Multi-agent orchestration
- Human-in-the-loop validation
- Domain-specific cleaning policies
- Data quality scoring
- RAG-powered schema understanding
- Real-time streaming data cleaning
- Enterprise governance integrations

---

# 📜 License

This project is intended for educational, research, and intelligent data engineering applications.

---

## ⭐ DataSanct

**DataSanct** bridges the gap between AI reasoning and reliable data engineering by combining **LLM-guided recommendations**, **automated profiling**, **safe cleaning execution**, and **transparent auditing** into a unified intelligent data preparation platform.
