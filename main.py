from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import CandidateCreate, CandidateLogin, JobCreate, JobUpdate, ResumeUpload
from app.crud import create_candidate, create_job, update_job, get_all_jobs, get_all_candidates, get_user_by_email
from app.auth import create_access_token, get_password_hash, verify_password, get_current_user
from datetime import timedelta
from app.database import db
from bson import ObjectId
import os


COLLECTION_NAME = "jobs"
collection = db[COLLECTION_NAME] 

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()

@app.get("/")
def welcome_message():
    return {"message": "Welcome to the Recruitment System API!"}

@app.post("/signup")
async def signup(candidate: CandidateCreate):
    candidate.password = get_password_hash(candidate.password)
    await create_candidate(candidate)
    return {"message": "User created successfully"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/jobs", dependencies=[Depends(get_current_user)])
async def post_job(job: JobCreate, current_user: dict = Depends(get_current_user)):
    await create_job(job)
    return {"message": "Job created successfully"}

@app.put("/jobs/{job_id}", dependencies=[Depends(get_current_user)])
async def update_job_endpoint(job_id: str, job: JobUpdate):
    await update_job(job_id, job)
    return {"message": "Job updated successfully"}

def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(doc) for doc in data]
    elif isinstance(data, dict):
        return {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in data.items()}
    return data

@app.get("/jobs")
async def get_jobs():
    jobs = await collection.find().to_list(length=100) 
    return convert_objectid_to_str(jobs)


@app.get("/candidates", dependencies=[Depends(get_current_user)])
async def get_candidates():
    candidates = await get_all_candidates()
    return candidates


from app.crud import update_candidate_resume
# File Upload: Upload Resume
@app.post("/upload-resume")
async def upload_resume(data: ResumeUpload, file: UploadFile = File(...)):
    """
    Endpoint for uploading resumes. Stores the resume URL in the database.
    """
    # Save the file to the local upload folder
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Generate the resume URL (local file path in this case)
    resume_url = f"{UPLOAD_FOLDER}/{file.filename}"

    # Update the candidate's resume_url in the database
    result = await db.candidates.update_one(
        {"email": data.email},  # Use the email from the request body
        {"$set": {"resume_url": resume_url}}  # Set the resume URL
    )

    # Check if the candidate was found and updated
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return {"message": "Resume uploaded successfully", "resume_url": resume_url}

# Helper: Convert ObjectId to String
def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(doc) for doc in data]
    elif isinstance(data, dict):
        return {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in data.items()}
    return data

@app.get("/view-resume/{candidate_email}", dependencies=[Depends(get_current_user)])
async def view_resume(candidate_email: str, current_user: dict = Depends(get_current_user)):
    """
    Endpoint for admins to view candidate resumes.
    """
    # Verify if the current user is an admin
    if "role" not in current_user or current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied. Admins only.")

    # Fetch the candidate's resume URL
    candidate = await db.candidates.find_one({"email": candidate_email})
    if not candidate or "resume_url" not in candidate:
        raise HTTPException(status_code=404, detail="Candidate or resume not found.")

    return {"candidate_email": candidate_email, "resume_url": candidate["resume_url"]}