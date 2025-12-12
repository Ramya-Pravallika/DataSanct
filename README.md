# DataSanct - Intelligent Agentic Data Cleaning

https://data-sanct.vercel.app/

DataSanct is an advanced AI-powered application that accepts messy tabular (CSV/Excel) or image data and automatically cleans it using intelligent agents.

## Features
- **Agentic Analysis**: Automatically detects missing values, duplicates, outliers, and noise.
- **Nebula UI**: A premium, futuristic interface for seamless user experience.
- **Multimodal**: Handles both structural data and visual assets.
- **Secure**: Data is processed locally/via secure API and provided for download.

## Tech Stack
- **Frontend**: React (Vite) + Framer Motion + Lucide Icons
- **Backend**: FastAPI + Pandas + OpenCV + NumPy
- **AI/Agent**: Custom Python-based heuristic agent (extensible to LLMs)

## Installation

### Backend
```bash
cd server
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd client
npm install
npm run dev
```

## Usage
1. Upload a CSV or Image.
2. Watch the Agent analyze and formulate a plan.
3. View the cleaning results and download the sanitized file.
