# 🌍 Worldocs

**Worldocs** is a web-based document translation platform that converts PDF and DOCX files into multiple languages while preserving the original layout, formatting, and typography. It supports a wide range of Indic scripts and global languages with intelligent font rendering and HarfBuzz text shaping.

---

## ✨ Features

- 📄 **PDF & DOCX Translation** — Upload PDF or DOCX documents and receive a fully translated output.
- 🌐 **20+ Language Support** — Includes Hindi, Marathi, Bengali, Tamil, Telugu, Kannada, Malayalam, Gujarati, Punjabi, Arabic, Russian, Chinese, Japanese, Korean, and more.
- 🔤 **Script-Aware Font Rendering** — Automatically selects the correct Noto Sans font per Unicode block (Devanagari, Bengali, Tamil, etc.) using HarfBuzz text shaping via `fpdf2`.
- 🖼️ **OCR for Image-Based Text** — Extracts and translates text embedded in charts and images using PyMuPDF vector extraction and Tesseract OCR fallback.
- 📊 **Multi-Column Layout Detection** — Detects and preserves 2-column document structures.
- ☁️ **Cloud Storage** — Translated files are stored on AWS S3 and served via pre-signed URLs.
- 📧 **Email Delivery** — Send translated PDFs directly to any email address.
- 🔐 **JWT Authentication** — Secure user registration, login, and session management.
- 🔑 **Password Recovery** — Forgot password via 6-digit OTP sent to email (expires in 10 minutes).
- 🕐 **Session Idle Timeout** — Frontend enforces a 30-minute inactivity timeout.
- 🛡️ **Rate Limiting** — API endpoints are protected with `slowapi` to prevent abuse.
- 📋 **Translation History** — Each user has a dashboard showing past translation tasks.
- 🛠️ **Admin Panel** — View platform-wide stats and user data via a secured admin interface.
- 📶 **Real-Time Progress** — WebSocket endpoint streams live translation progress.

---

## 🏗️ Tech Stack

### Backend
| Component | Technology |
|---|---|
| Web Framework | FastAPI |
| Auth | JWT (`PyJWT`) + `passlib[bcrypt]` |
| Database | SQLAlchemy + PostgreSQL (`psycopg2`) |
| PDF Parsing | `pdfplumber`, `PyMuPDF (fitz)` |
| PDF Generation | `fpdf2` + `uharfbuzz` + `fonttools` |
| Translation | `deep-translator` (Google Translate) |
| DOCX Support | `python-docx` |
| OCR | `pytesseract` + `Pillow` |
| Storage | AWS S3 (`boto3`) |
| Email | `aiosmtplib` + `fastapi-mail` |
| Rate Limiting | `slowapi` |
| ASGI Server | `uvicorn` |

### Frontend
| Component | Technology |
|---|---|
| UI Pages | Vanilla HTML, CSS, JavaScript |
| Fonts | Noto Sans (Latin & all Indic scripts) |
| Styling | Custom CSS (`style.css`) |
| Config | `config.js` — dynamic API URL selection |

---

## 📁 Project Structure

```
Worldocs/
├── app.py                        # Main FastAPI application & translation logic
├── auth.py                       # JWT authentication helpers
├── models.py                     # SQLAlchemy ORM models (User, TranslationTask)
├── database.py                   # DB engine + session factory
├── email_utils.py                # Email sending utilities (OTP, PDF delivery)
├── config.js                     # Frontend API URL configuration
├── style.css                     # Global stylesheet
│
├── index.html                    # Landing / upload page
├── dashboard.html                # User dashboard (history, translation UI)
├── login.html                    # Login & registration page
├── reset-password.html           # Password reset via OTP
├── admin.html                    # Admin statistics panel
│
├── NotoSansDevanagari-Regular.ttf  # Hindi / Marathi
├── NotoSansBengali-Regular.ttf     # Bengali
├── NotoSansGujarati-Regular.ttf    # Gujarati
├── NotoSansGurmukhi-Regular.ttf    # Punjabi
├── NotoSansTamil-Regular.ttf       # Tamil
├── NotoSansTelugu-Regular.ttf      # Telugu
├── NotoSansKannada-Regular.ttf     # Kannada
├── NotoSansMalayalam-Regular.ttf   # Malayalam
├── NotoSansArabic-Regular.ttf      # Arabic / Urdu
├── NotoSans-Regular.ttf            # Latin / Cyrillic / Generic Unicode
│
├── download_fonts.sh             # Script to download Noto font files
├── requirements.txt              # Python dependencies
├── render.yaml                   # Render.com deployment config
├── Procfile                      # Process file (alternative deployment)
└── .env                          # Environment variables (not committed)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL database
- AWS S3 bucket
- Gmail account (for email delivery via SMTP)
- Tesseract OCR installed on the system

### 1. Clone the Repository

```bash
git clone https://github.com/jayesh5103/Worldocs.git
cd Worldocs
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Noto Fonts

```bash
bash download_fonts.sh
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
# JWT
SECRET_KEY=your_secret_key_here

# Database
DATABASE_URL=postgresql://user:password@host:5432/worldocs

# AWS S3
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=eu-north-1
S3_BUCKET=pdf-translator-storage

# Email (Gmail SMTP)
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

# Admin
ADMIN_SECRET=your_admin_secret

# CORS (comma-separated origins)
ALLOWED_ORIGIN=https://yourdomain.com
```

### 6. Run the Backend

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 7. Open the Frontend

Open `index.html` in your browser, or serve all HTML files via a static file server (e.g., GitHub Pages, Nginx, or Live Server in VS Code).

---

## ⚙️ Configuration

Edit `config.js` to point the frontend to your backend:

```js
const CONFIG = {
    API_BASE_URL: "https://worldocs.onrender.com",  // ← your Render URL
    ...
};
```

The config automatically resolves to `localhost:8000` when running locally.

---

## 🌐 API Reference

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/register` | Register a new user | No |
| `POST` | `/login` | Login and receive JWT token | No |
| `POST` | `/forgot-password` | Send OTP for password reset | No |
| `POST` | `/reset-password` | Reset password using OTP | No |
| `POST` | `/forgot-username` | Email username reminder | No |
| `POST` | `/translate` | Upload PDF/DOCX and start translation | Yes |
| `GET` | `/history` | Fetch user's translation history | Yes |
| `POST` | `/send-pdf` | Email a translated PDF | Yes |
| `WS` | `/progress/{task_id}` | Real-time translation progress | Yes |
| `GET` | `/admin/stats` | Platform statistics | Admin |
| `GET` | `/admin/users` | List all users with task counts | Admin |

---

## 🌍 Supported Languages

| Language | Code | Script |
|---|---|---|
| Hindi | `hi` | Devanagari |
| Marathi | `mr` | Devanagari |
| Bengali | `bn` | Bengali |
| Gujarati | `gu` | Gujarati |
| Punjabi | `pa` | Gurmukhi |
| Tamil | `ta` | Tamil |
| Telugu | `te` | Telugu |
| Kannada | `kn` | Kannada |
| Malayalam | `ml` | Malayalam |
| Arabic | `ar` | Arabic |
| Urdu | `ur` | Arabic |
| Russian | `ru` | Cyrillic |
| Chinese (Simplified) | `zh-CN` | CJK |
| Japanese | `ja` | CJK |
| Korean | `ko` | Hangul |
| French | `fr` | Latin |
| German | `de` | Latin |
| Spanish | `es` | Latin |
| Portuguese | `pt` | Latin |

---

## ☁️ Deployment (Render.com)

This project includes a `render.yaml` for one-click deployment on [Render](https://render.com):

1. Push the repository to GitHub.
2. Connect it to Render and select **"Use render.yaml"**.
3. Set the following environment variables in the Render dashboard:
   - `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_FROM`
   - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
   - `ALLOWED_ORIGIN`
   - `ADMIN_SECRET`
4. Render will automatically provision a free PostgreSQL database (`worldocs-db`).

---

## 🔒 Security

- Passwords are hashed with **bcrypt** via `passlib`.
- API authentication uses **JWT Bearer tokens** (2-hour expiry).
- Frontend enforces a **30-minute idle session timeout**.
- OTP for password reset expires in **10 minutes**.
- Rate limiting applied to login (`10/min`), forgot-password (`5/min`), and other sensitive endpoints.
- Admin endpoints require a secret header (`X-Admin-Secret`).
- CORS is configurable via the `ALLOWED_ORIGIN` environment variable.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Jayesh** — [@jayesh5103](https://github.com/jayesh5103)

---

> Built as an MCA project to make document translation accessible across languages and scripts.
