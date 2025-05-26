from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50))  # Store "lat,lon" as string
    date = db.Column(db.String(20))      # date string, e.g. "2025-05-25"
    temperature = db.Column(db.Float)    # temperature in Celsius
