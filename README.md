# Akshay Tyagi – Portfolio

React frontend + FastAPI Python backend.

## Project Structure

```
portfolio/
├── backend/
│   ├── main.py           # FastAPI backend
│   └── requirements.txt
└── frontend/
    └── index.html        # React frontend (single file)
```

## Setup & Run

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# Runs at http://localhost:8000
```

### 2. Frontend

Just open `frontend/index.html` in your browser directly.  
Or serve it with any static server:

```bash
cd frontend
npx serve .
# or
python -m http.server 3000
```

> Make sure the backend is running at `http://localhost:8000` before opening the frontend.

## Deploy

- **Backend**: Deploy `backend/` to Railway, Render, or any VPS. Update `API_BASE` in `index.html` to your deployed URL.
- **Frontend**: Deploy `frontend/` to GitHub Pages, Vercel, or Netlify.
