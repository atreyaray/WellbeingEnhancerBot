from dotenv import load_dotenv
load_dotenv()
import os
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_URI = os.getenv("DATABASE_URI")
