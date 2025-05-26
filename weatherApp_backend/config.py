import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'db', 'weather.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
