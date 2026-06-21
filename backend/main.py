from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid, jwt, datetime, copy

app = FastAPI(title="Akshay Tyagi Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


SECRET_KEY = "akshay-portfolio-secret-2026"  
ADMIN_USERNAME = "akshay"
ADMIN_PASSWORD = "Tyagiboy@123"                 
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
            {"id": "l1", "label": "GitHub",   "url": "https://github.com/akshaytyagi0007", "icon": "github", "username": "akshaytyagi0007"},
            {"id": "l2", "label": "LinkedIn", "url": "", "icon": "linkedin", "username": ""},
        ]
    }
}


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
    username: Optional[str] = ""

class ProfileModel(BaseModel):
    name: str
    title: str
    email: str
    phone: str
    location: str
    github: str
    objective: str


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
    return {**db["profile"], "skills": db["skills"], "certifications": db["certifications"],
            "projects": [p for p in db["projects"] if p["public"]],
            "contact": db["contact"]}

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



@app.put("/api/admin/profile", dependencies=[Depends(verify_token)])
def update_profile(body: ProfileModel):
    db["profile"].update(body.dict())
    return {"message": "Profile updated"}


@app.put("/api/admin/skills", dependencies=[Depends(verify_token)])
def update_skills(body: SkillsModel):
    db["skills"] = body.skills
    return {"message": "Skills updated"}

@app.post("/api/admin/skills/category", dependencies=[Depends(verify_token)])
def add_skill_category(body: dict):
    name = body.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Category name required")
    if name in db["skills"]:
        raise HTTPException(status_code=400, detail="Category already exists")
    db["skills"][name] = []
    return {"message": f"Category '{name}' added"}

@app.delete("/api/admin/skills/category/{name}", dependencies=[Depends(verify_token)])
def delete_skill_category(name: str):
    if name not in db["skills"]:
        raise HTTPException(status_code=404, detail="Category not found")
    del db["skills"][name]
    return {"message": f"Category '{name}' deleted"}


@app.post("/api/admin/certifications", dependencies=[Depends(verify_token)])
def add_certification(body: CertificationModel):
    cert = {"id": str(uuid.uuid4())[:8], **body.dict()}
    db["certifications"].append(cert)
    return cert

@app.put("/api/admin/certifications/{cert_id}", dependencies=[Depends(verify_token)])
def update_certification(cert_id: str, body: CertificationModel):
    for i, c in enumerate(db["certifications"]):
        if c["id"] == cert_id:
            db["certifications"][i] = {"id": cert_id, **body.dict()}
            return db["certifications"][i]
    raise HTTPException(status_code=404, detail="Certification not found")

@app.delete("/api/admin/certifications/{cert_id}", dependencies=[Depends(verify_token)])
def delete_certification(cert_id: str):
    before = len(db["certifications"])
    db["certifications"] = [c for c in db["certifications"] if c["id"] != cert_id]
    if len(db["certifications"]) == before:
        raise HTTPException(status_code=404, detail="Certification not found")
    return {"message": "Deleted"}


@app.post("/api/admin/projects", dependencies=[Depends(verify_token)])
def add_project(body: ProjectModel):
    project = {"id": str(uuid.uuid4())[:8], **body.dict()}
    db["projects"].append(project)
    return project

@app.put("/api/admin/projects/{proj_id}", dependencies=[Depends(verify_token)])
def update_project(proj_id: str, body: ProjectModel):
    for i, p in enumerate(db["projects"]):
        if p["id"] == proj_id:
            db["projects"][i] = {"id": proj_id, **body.dict()}
            return db["projects"][i]
    raise HTTPException(status_code=404, detail="Project not found")

@app.delete("/api/admin/projects/{proj_id}", dependencies=[Depends(verify_token)])
def delete_project(proj_id: str):
    before = len(db["projects"])
    db["projects"] = [p for p in db["projects"] if p["id"] != proj_id]
    if len(db["projects"]) == before:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Deleted"}


@app.put("/api/admin/contact/fixed", dependencies=[Depends(verify_token)])
def update_contact_fixed(body: ContactFixedModel):
    db["contact"]["fixed"].update(body.dict())
    return {"message": "Contact info updated"}

@app.post("/api/admin/contact/links", dependencies=[Depends(verify_token)])
def add_contact_link(body: ContactLinkModel):
    link = {"id": str(uuid.uuid4())[:8], **body.dict()}
    db["contact"]["links"].append(link)
    return link

@app.put("/api/admin/contact/links/{link_id}", dependencies=[Depends(verify_token)])
def update_contact_link(link_id: str, body: ContactLinkModel):
    for i, l in enumerate(db["contact"]["links"]):
        if l["id"] == link_id:
            db["contact"]["links"][i] = {"id": link_id, **body.dict()}
            return db["contact"]["links"][i]
    raise HTTPException(status_code=404, detail="Link not found")

@app.delete("/api/admin/contact/links/{link_id}", dependencies=[Depends(verify_token)])
def delete_contact_link(link_id: str):
    before = len(db["contact"]["links"])
    db["contact"]["links"] = [l for l in db["contact"]["links"] if l["id"] != link_id]
    if len(db["contact"]["links"]) == before:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"message": "Deleted"}