from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Candidate schemas
class CandidateCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class CandidateLogin(BaseModel):
    email: EmailStr
    password: str

class CandidateResponse(BaseModel):
    email: EmailStr
    name: str
    resume_url: Optional[str] = None  # Added: Resume URL field to return candidate details with resume info

from pydantic import BaseModel, EmailStr

class ResumeUpload(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


# Job schemas
class JobCreate(BaseModel):
    title: str
    description: str
    department: str
    location: str
    employment_type: str
    salary_range: Optional[str] = None
    application_deadline: Optional[datetime] = None
    required_skills: List[str]
    additional_info: Optional[str] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    salary_range: Optional[str] = None
    application_deadline: Optional[datetime] = None
    required_skills: Optional[List[str]] = None
    additional_info: Optional[str] = None
    status: Optional[str] = None


# Admin and resume-specific schemas
class ResumeUploadResponse(BaseModel):
    message: str
    resume_url: str  # Added: Response schema for successful resume upload
