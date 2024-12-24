from app.models import Candidate, Admin, Job
from bson.objectid import ObjectId
from app.database import db
from app.schemas import JobUpdate
async def create_candidate(candidate: Candidate):
    await db.candidates.insert_one(candidate.dict())

async def get_user_by_email(db, email: str):
    return await db.candidates.find_one({"email": email}) or await db.admins.find_one({"email": email})

async def create_job(job: Job):
    await db.jobs.insert_one(job.dict())

async def update_job(job_id: str, job: JobUpdate):
    await db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": job.dict(exclude_unset=True)})

async def get_all_jobs():
    return await db.jobs.find().to_list(100)

async def get_all_candidates():
    return await db.candidates.find().to_list(100)

async def update_candidate_resume(email: str, resume_url: str):
    return await db.candidates.update_one(
        {"email": email},
        {"$set": {"resume_url": resume_url}}
    )
