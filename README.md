# AI Health Report Interpreter

An AI-powered clinical report interpreter that helps patients understand complex medical PDFs (laboratory blood tests and imaging scans) in plain language across **English and 8 Indian languages**.

## Live Deployment
- **Frontend (Vercel):** https://ai-health-report-interpeter.vercel.app
- **Backend (Render):** https://ai-health-report-interpeter.onrender.com

## Key Features
- **PDF Upload & Multimodal OCR:** Extracts biomarkers and clinical findings using **Google Gemini** (`gemini-3.5-flash-lite` with `gemini-2.5-flash` fallback) and local **PyMuPDF / Tesseract** fallback.
- **Biomarker & Triage Analysis:** Compares extracted lab values against reference ranges (Low / Normal / High), computes concern levels, and enriches results with a medical knowledge base (`backend/knowledge_base/medical_knowledge.json`).
- **8 Indian Languages + English:** Supports English, Hindi, Telugu, Tamil, Kannada, Malayalam, Marathi, and Bengali, with automatic re-analysis when switching languages.
- **Interactive AI Assistant:** Patients can ask follow-up questions about their uploaded report (`POST /ask`).
- **Local Device Bookmarks:** Save and reopen analyzed reports locally in the browser (`localStorage`).
- **Persistent Cloud Storage:** Saves analyzed reports per authenticated user in **Supabase PostgreSQL** (`public.reports`).
- **Authentication:** Secured with **Clerk** JWT verification on protected API endpoints.

## Tech Stack
- **Frontend:** React, Vite, React Router, Clerk (`@clerk/react`)
- **Backend:** Python, Flask, Gunicorn, Google GenAI (`google-genai`), PyMuPDF, Pytesseract, Clerk Backend API
- **Database:** Supabase (PostgreSQL)
- **Hosting:** Vercel (Frontend) & Render (Backend)

## Project Structure
```text
capstone/
├── backend/
│   ├── app.py                  # Flask API (/upload, /ask, /reports)
│   ├── auth.py                 # Clerk JWT authentication decorator
│   ├── gemini_ocr_service.py   # Gemini multimodal PDF extraction + fallback
│   ├── pdf_service.py          # PyMuPDF / Tesseract local extraction
│   ├── biomarker_service.py    # Biomarker parsing
│   ├── analysis_service.py     # Clinical analysis & triage
│   ├── imaging_service.py      # Imaging report analysis
│   ├── translation_service.py  # Language normalization
│   ├── supabase_service.py     # Supabase client & report CRUD
│   ├── supabase_schema.sql     # PostgreSQL schema for public.reports
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main UI, bookmarks, language switching, AI chat
│   │   └── translations.js     # UI translations
│   ├── vercel.json             # SPA rewrite rules for Vercel
│   └── package.json
└── render.yaml                 # Render deployment blueprint
```

## Local Setup

### 1. Backend
```powershell
cd backend
pip install -r requirements.txt
python app.py
```
Configure `backend/.env` (see `backend/.env.example`):
- `GEMINI_API_KEY`
- `CLERK_SECRET_KEY`
- `CLERK_JWT_KEY`
- `CLERK_AUTHORIZED_PARTIES=http://localhost:5173`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

### 2. Frontend
```powershell
cd frontend
npm install
npm run dev
```
Configure `frontend/.env.local`:
- `VITE_CLERK_PUBLISHABLE_KEY`
- `VITE_API_URL=http://127.0.0.1:5000`
