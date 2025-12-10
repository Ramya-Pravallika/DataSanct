# How to Publish (Deploy) DataSanct

Since this project has two parts (Frontend and Backend), you need to deploy them separately.

## 1. Deploying the Backend (FastAPI)
We recommend **Render** or **Railway** for the Python backend.

### Steps for Render.com (Free Tier):
1.  Push your latest code to GitHub (Already done!).
2.  Sign up at [render.com](https://render.com).
3.  Click **New +** -> **Web Service**.
4.  Connect your GitHub repository (`DataSanct`).
5.  **Settings**:
    - **Root Directory**: `server`
    - **Runtime**: `Python 3`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6.  Click **Deploy**.
7.  Once live, you will get a URL like `https://datasanct-api.onrender.com`.

## 2. Deploying the Frontend (React)
We recommend **Vercel** or **Netlify**.

### Steps for Vercel:
1.  Sign up at [vercel.com](https://vercel.com).
2.  Click **Add New...** -> **Project**.
3.  Import your `DataSanct` repository.
4.  **Settings**:
    - **Framework Preset**: Vite
    - **Root Directory**: `client` (Click Edit to change this!)
5.  **Environment Variables**:
    - You need to tell the frontend where the backend lives.
    - We need to update `App.jsx` to use an environment variable first! (See below).
6.  Click **Deploy**.

## 3. Important Code Adjustment
Before deploying, we need to make the API URL in the frontend dynamic, so it works on the cloud (not just localhost).

**In `client/src/App.jsx` & `client/src/components/DataView.jsx`:**
Change `http://localhost:8000` to utilize:
`const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"`

Then in Vercel, set `VITE_API_URL` to your Render Backend URL.
