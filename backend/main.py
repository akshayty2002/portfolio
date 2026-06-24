from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid, jwt, datetime, json, os, base64, httpx

app = FastAPI(title="Akshay Tyagi Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── GitHub DB config (set these as env vars on Render) ────────────────────────
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO  = os.getenv("GITHUB_REPO", "")   # e.g. akshaytyagi0007/portfolio-db
GITHUB_FILE  = os.getenv("GITHUB_FILE", "db.json")
GITHUB_API   = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"

def github_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

def load_from_github() -> dict:
    """Pull db.json from GitHub and return parsed dict."""
    try:
        r = httpx.get(GITHUB_API, headers=github_headers(), timeout=10)
        r.raise_for_status()
        data = r.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        return json.loads(content), data["sha"]
    except Exception as e:
        print(f"[warn] Could not load from GitHub: {e}")
        return None, None

def save_to_github(data: dict, sha: str):
    """Push updated db.json back to GitHub."""
    try:
        content = base64.b64encode(
            json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        ).decode("utf-8")
        payload = {
            "message": "chore: update portfolio db",
            "content": content,
            "sha": sha
        }
        r = httpx.put(GITHUB_API, headers=github_headers(), json=payload, timeout=10)
        r.raise_for_status()
        # update sha for next write
        return r.json()["content"]["sha"]
    except Exception as e:
        print(f"[warn] Could not save to GitHub: {e}")
        return sha

# ── Auth config (set SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD on Render) ────
SECRET_KEY     = os.getenv("SECRET_KEY",     "change-this-secret")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "akshay")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin@2026")
security = HTTPBearer()

def create_token():
    payload = {
        "sub": ADMIN_USERNAME,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ── In-memory db (default fallback if GitHub unreachable) ─────────────────────
db = {
    "profile": {
        "name": "Akshay Tyagi",
        "title": "Junior Python Developer",
        "email": "akshayvatstyagi0007@gmail.com",
        "phone": "+91-8130204102",
        "location": "Ghaziabad, India",
        "github": "https://github.com/akshaytyagi0007",
        "objective": (
            "Motivated Computer Science graduate with 1.5+ years of professional experience "
            "as a Junior Python Developer at Accenture. Skilled in Python, REST API development, "
            "data analysis, and backend development. Seeking a role to further apply and grow my "
            "expertise in building scalable, real-world solutions."
        ),
    },
    "skills": {
        "Languages": ["Python", "SQL", "Bash"],
        "Libraries & Frameworks": ["NumPy", "Pandas", "Matplotlib", "Seaborn", "Plotly", "FastAPI", "Requests", "BeautifulSoup"],
        "Tools": ["Git", "GitHub", "VS Code", "Jupyter Notebook", "Postman"],
        "Databases": ["SQLite", "PostgreSQL"],
        "Core Concepts": ["REST APIs", "Data Wrangling", "EDA", "Data Visualisation", "JWT Authentication"],
    },
    "certifications": [
        {"id": "c1", "title": "FastAPI – The Complete Course 2026 (Beginner + Advanced)", "platform": "Udemy", "instructors": "Eric Roby, Chad Darby", "date": "June 2026", "url": "https://www.udemy.com/certificate/fastapi-complete-course"},
        {"id": "c2", "title": "Python Data Analysis: NumPy & Pandas Masterclass", "platform": "Udemy", "instructors": "Maven Analytics, Chris Bruehl", "date": "June 2026", "url": "https://www.udemy.com/certificate/numpy-pandas-masterclass"},
    ],
    "projects": [
        {"id": "p1", "title": "CLI ATM Simulator", "tech": ["Python"], "github": "https://github.com/akshaytyagi0007/python-atm-simulator", "description": "Command-line ATM simulation with account creation, PIN auth, deposits, withdrawals, and mini-statement generation.", "highlights": ["Session management and input validation with lockout logic", "JSON file storage for persistent account data across runs"], "public": True},
        {"id": "p2", "title": "Number Guessing Game", "tech": ["Python"], "github": "https://github.com/akshaytyagi0007/number-guessing-game", "description": "Interactive CLI number guessing game with difficulty levels and score tracking.", "highlights": ["Multiple difficulty levels with dynamic range", "Score tracking and replay functionality"], "public": True},
        {"id": "p3", "title": "URL Shortener", "tech": ["Python"], "github": "https://github.com/akshaytyagi0007/url-shortner", "description": "Python-based URL shortener that converts long URLs into short, shareable links.", "highlights": ["Custom alias support for shortened URLs", "Persistent storage of URL mappings"], "public": True},
        {"id": "p4", "title": "Neural Network from Scratch", "tech": ["Python", "NumPy"], "github": "https://github.com/akshaytyagi0007/neural-net-numpy", "description": "Fully-connected feedforward neural network using only NumPy – no ML frameworks.", "highlights": ["Forward propagation, backpropagation, and gradient descent from scratch", "94%+ accuracy on MNIST with a 2-hidden-layer architecture"], "public": False},
        {"id": "p5", "title": "Titanic Survival – EDA", "tech": ["Python", "Pandas", "Seaborn", "Matplotlib"], "github": "https://github.com/akshaytyagi0007/titanic-eda", "description": "Exploratory Data Analysis on the Kaggle Titanic dataset uncovering survival patterns.", "highlights": ["Missing value treatment, outlier detection, and feature correlation analysis", "5+ visualisations: female survival ~74% vs male ~19%; 1st class ~63% survival"], "public": True},
        {"id": "p6", "title": "Animated GDP Time-Series", "tech": ["Python", "Matplotlib", "Pandas"], "github": "https://github.com/akshaytyagi0007/animated-timeseries", "description": "Animated bar chart race visualising GDP growth across countries from 1960 to 2020.", "highlights": ["Matplotlib FuncAnimation for smooth frame-by-frame transitions", "Exported as MP4 and GIF for GitHub and LinkedIn"], "public": False},
        {"id": "p7", "title": "Secure Auth API – FastAPI", "tech": ["Python", "FastAPI", "JWT", "SQLite", "Pydantic"], "github": "https://github.com/akshaytyagi0007/auth-api-fastapi", "description": "Production-ready REST API with JWT-based auth, bcrypt password hashing, and Swagger docs.", "highlights": ["Password hashing (bcrypt), token expiry, and refresh token logic", "Auto-generated Swagger UI via FastAPI's OpenAPI integration"], "public": False},
    ],
    "contact": {
        "fixed": {
            "email": "akshayvatstyagi0007@gmail.com",
            "phone": "+91-8130204102",
            "location": "Ghaziabad, India",
        },
        "links": [
            {"id": "l1", "label": "GitHub",   "url": "https://github.com/akshaytyagi0007", "icon": "github"},
            {"id": "l2", "label": "LinkedIn", "url": "", "icon": "linkedin"},
        ]
    },
    "education": [
        {"id": "edu1", "degree": "B.Tech – Computer Science & Engineering", "institution": "Dr. A.P.J. Abdul Kalam Technical University (AKTU)", "year": "2019 – 2023", "percentage": "73%"},
        {"id": "edu2", "degree": "Intermediate (PCM)", "institution": "Kendriya Vidyalaya, Ghaziabad", "year": "2019", "percentage": "75%"},
    ]
}

# sha of the current db.json on GitHub (needed for updates)
_gh_sha = None

@app.on_event("startup")
async def startup():
    """Load latest db from GitHub on startup."""
    global _gh_sha
    if GITHUB_TOKEN and GITHUB_REPO:
        data, sha = load_from_github()
        if data:
            db.update(data)
            _gh_sha = sha
            print("[info] db loaded from GitHub")
        else:
            print("[warn] using default in-memory db")
    else:
        print("[info] no GitHub env vars set – using in-memory db only")

def persist():
    """Save current db to GitHub. Call after every write."""
    global _gh_sha
    if GITHUB_TOKEN and GITHUB_REPO:
        _gh_sha = save_to_github(db, _gh_sha)

# ── Pydantic models ───────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str

class CertificationModel(BaseModel):
    title: str
    platform: str
    instructors: str
    date: str
    url: str

class ProjectModel(BaseModel):
    title: str
    tech: List[str]
    github: str
    description: str
    highlights: List[str]
    public: bool

class SkillsModel(BaseModel):
    skills: Dict[str, List[str]]

class ContactFixedModel(BaseModel):
    email: str
    phone: str
    location: str

class ContactLinkModel(BaseModel):
    label: str
    url: str
    icon: str

class ProfileModel(BaseModel):
    name: str
    title: str
    email: str
    phone: str
    location: str
    github: str
    objective: str

class EducationModel(BaseModel):
    degree: str
    institution: str
    year: str
    percentage: str

# ── Public routes ─────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Akshay Tyagi Portfolio API"}

@app.post("/api/auth/login")
def login(body: LoginRequest):
    if body.username != ADMIN_USERNAME or body.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": create_token(), "message": "Login successful"}

@app.get("/api/all")
def get_all():
    return {
        **db["profile"],
        "skills":         db["skills"],
        "certifications": db["certifications"],
        "projects":       [p for p in db["projects"] if p["public"]],
        "contact":        db["contact"],
        "education":      db["education"],
    }

@app.get("/api/profile")
def get_profile():
    return db["profile"]

@app.get("/api/skills")
def get_skills():
    return db["skills"]

@app.get("/api/projects")
def get_projects():
    return db["projects"]

@app.get("/api/certifications")
def get_certifications():
    return db["certifications"]

@app.get("/api/contact")
def get_contact():
    return db["contact"]

@app.get("/api/education")
def get_education():
    return db["education"]

# ── Admin: Profile ────────────────────────────────────────────────────────────

@app.put("/api/admin/profile", dependencies=[Depends(verify_token)])
def update_profile(body: ProfileModel):
    db["profile"].update(body.model_dump())
    persist()
    return {"message": "Profile updated"}

# ── Admin: Skills ─────────────────────────────────────────────────────────────

@app.put("/api/admin/skills", dependencies=[Depends(verify_token)])
def update_skills(body: SkillsModel):
    db["skills"] = body.skills
    persist()
    return {"message": "Skills updated"}

@app.post("/api/admin/skills/category", dependencies=[Depends(verify_token)])
def add_skill_category(body: dict):
    name = body.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Category name required")
    if name in db["skills"]:
        raise HTTPException(status_code=400, detail="Category already exists")
    db["skills"][name] = []
    persist()
    return {"message": f"Category '{name}' added"}

@app.delete("/api/admin/skills/category/{name}", dependencies=[Depends(verify_token)])
def delete_skill_category(name: str):
    if name not in db["skills"]:
        raise HTTPException(status_code=404, detail="Category not found")
    del db["skills"][name]
    persist()
    return {"message": f"Category '{name}' deleted"}

# ── Admin: Certifications ─────────────────────────────────────────────────────

@app.post("/api/admin/certifications", dependencies=[Depends(verify_token)])
def add_certification(body: CertificationModel):
    cert = {"id": str(uuid.uuid4())[:8], **body.model_dump()}
    db["certifications"].append(cert)
    persist()
    return cert

@app.put("/api/admin/certifications/{cert_id}", dependencies=[Depends(verify_token)])
def update_certification(cert_id: str, body: CertificationModel):
    for i, c in enumerate(db["certifications"]):
        if c["id"] == cert_id:
            db["certifications"][i] = {"id": cert_id, **body.model_dump()}
            persist()
            return db["certifications"][i]
    raise HTTPException(status_code=404, detail="Certification not found")

@app.delete("/api/admin/certifications/{cert_id}", dependencies=[Depends(verify_token)])
def delete_certification(cert_id: str):
    before = len(db["certifications"])
    db["certifications"] = [c for c in db["certifications"] if c["id"] != cert_id]
    if len(db["certifications"]) == before:
        raise HTTPException(status_code=404, detail="Certification not found")
    persist()
    return {"message": "Deleted"}

# ── Admin: Projects ───────────────────────────────────────────────────────────

@app.post("/api/admin/projects", dependencies=[Depends(verify_token)])
def add_project(body: ProjectModel):
    project = {"id": str(uuid.uuid4())[:8], **body.model_dump()}
    db["projects"].append(project)
    persist()
    return project

@app.put("/api/admin/projects/{proj_id}", dependencies=[Depends(verify_token)])
def update_project(proj_id: str, body: ProjectModel):
    for i, p in enumerate(db["projects"]):
        if p["id"] == proj_id:
            db["projects"][i] = {"id": proj_id, **body.model_dump()}
            persist()
            return db["projects"][i]
    raise HTTPException(status_code=404, detail="Project not found")

@app.delete("/api/admin/projects/{proj_id}", dependencies=[Depends(verify_token)])
def delete_project(proj_id: str):
    before = len(db["projects"])
    db["projects"] = [p for p in db["projects"] if p["id"] != proj_id]
    if len(db["projects"]) == before:
        raise HTTPException(status_code=404, detail="Project not found")
    persist()
    return {"message": "Deleted"}

# ── Admin: Contact ────────────────────────────────────────────────────────────

@app.put("/api/admin/contact/fixed", dependencies=[Depends(verify_token)])
def update_contact_fixed(body: ContactFixedModel):
    db["contact"]["fixed"].update(body.model_dump())
    persist()
    return {"message": "Contact info updated"}

@app.post("/api/admin/contact/links", dependencies=[Depends(verify_token)])
def add_contact_link(body: ContactLinkModel):
    link = {"id": str(uuid.uuid4())[:8], **body.model_dump()}
    db["contact"]["links"].append(link)
    persist()
    return link

@app.put("/api/admin/contact/links/{link_id}", dependencies=[Depends(verify_token)])
def update_contact_link(link_id: str, body: ContactLinkModel):
    for i, l in enumerate(db["contact"]["links"]):
        if l["id"] == link_id:
            db["contact"]["links"][i] = {"id": link_id, **body.model_dump()}
            persist()
            return db["contact"]["links"][i]
    raise HTTPException(status_code=404, detail="Link not found")

@app.delete("/api/admin/contact/links/{link_id}", dependencies=[Depends(verify_token)])
def delete_contact_link(link_id: str):
    before = len(db["contact"]["links"])
    db["contact"]["links"] = [l for l in db["contact"]["links"] if l["id"] != link_id]
    if len(db["contact"]["links"]) == before:
        raise HTTPException(status_code=404, detail="Link not found")
    persist()
    return {"message": "Deleted"}

# ── Admin: Education ──────────────────────────────────────────────────────────

@app.post("/api/admin/education", dependencies=[Depends(verify_token)])
def add_education(body: EducationModel):
    edu = {"id": str(uuid.uuid4())[:8], **body.model_dump()}
    db["education"].append(edu)
    persist()
    return edu

@app.put("/api/admin/education/{edu_id}", dependencies=[Depends(verify_token)])
def update_education(edu_id: str, body: EducationModel):
    for i, e in enumerate(db["education"]):
        if e["id"] == edu_id:
            db["education"][i] = {"id": edu_id, **body.model_dump()}
            persist()
            return db["education"][i]
    raise HTTPException(status_code=404, detail="Education not found")

@app.delete("/api/admin/education/{edu_id}", dependencies=[Depends(verify_token)])
def delete_education(edu_id: str):
    before = len(db["education"])
    db["education"] = [e for e in db["education"] if e["id"] != edu_id]
    if len(db["education"]) == before:
        raise HTTPException(status_code=404, detail="Education not found")
    persist()
    return {"message": "Deleted"}
