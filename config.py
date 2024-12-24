import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# MongoDB settings
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://hrutikadsuryawanshi2002:rutika@cluster0.tzlwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "p6Kx9XkLJhI3TyNZzlx5M3lG7PqJo1nOjxR3d5LQ0xk")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
