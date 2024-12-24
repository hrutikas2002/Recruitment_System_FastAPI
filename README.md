Project Setup:
1. Create a virtual environment and install the dependencies:

python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt

2. Set up the database:

Run migrations or create the necessary tables in the database as per your ORM configuration.

3. Run the API server:
uvicorn main:app --reload

The application will be available at http://127.0.0.1:8000.

Environment Variables
The project requires a .env file to configure sensitive information and environment-specific variables. Below is an example of the required environment variables:

Example .env file:
ini
Copy code
MONGO_URI=your_mongo_database_uri
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

Description of Variables:
MONGO_URI: The URI for connecting to your MongoDB database. Replace this with your MongoDB connection string.
SECRET_KEY: A secret key used to encode JWT tokens. Ensure this key is kept secure.
ALGORITHM: The algorithm used for JWT token encryption (e.g., HS256).
ACCESS_TOKEN_EXPIRE_MINUTES: The expiration time (in minutes) for the JWT access token.
