from flask import Flask, request, jsonify
import requests
from datetime import datetime
from models import db, WeatherData
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

@app.route("/")
def home():
    return {"message": "Weather API running"}

# /weather to search for temp
@app.route("/weather")
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return {"error": "Please provide 'lat' and 'lon' query parameters"}, 400

    # Fetch weather from OpenWeatherMap API
    api_key = app.config["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    res = requests.get(url)
    if res.status_code != 200:
        return {"error": "Failed to fetch weather"}, 500

    data = res.json()
    temp = data["main"]["temp"]
    location_str = f"{lat},{lon}"
    date_str = datetime.utcnow().strftime("%Y-%m-%d")

    # Store data in database
    record = WeatherData(location=location_str, date=date_str, temperature=temp)
    db.session.add(record)
    db.session.commit()

    return {
        "location": location_str,
        "date": date_str,
        "temperature": temp
    }
# /export/json 
@app.route("/export/json")
def export_json():
    records = WeatherData.query.all()
    result = [
        {"location": r.location, "date": r.date, "temperature": r.temperature}
        for r in records
    ]
    return jsonify(result)
#/view
@app.route("/view")
def view_records():
    records = WeatherData.query.all()
    return jsonify([
        {"id": r.id, "location": r.location, "date": r.date, "temperature": r.temperature}
        for r in records
    ])
#/update/#?location=#,#&date=####-##-##&temp=#
@app.route("/update/<int:id>")
def update_record(id):
    record = WeatherData.query.get(id)
    if not record:
        return {"error": "Record not found"}, 404

    location = request.args.get("location")
    date = request.args.get("date")
    temp = request.args.get("temp")

    if location:
        parts = location.split(",")
        if len(parts) != 2:
            return {"error": "Location must be in 'lat,lon' format"}, 400
        try:
            lat = float(parts[0])
            lon = float(parts[1])
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                return {"error": "Latitude must be between -90 and 90 and longitude between -180 and 180"}, 400
        except ValueError:
            return {"error": "Latitude and longitude must be numbers"}, 400
        record.location = location

    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return {"error": "Date must be in YYYY-MM-DD format"}, 400
        record.date = date

    if temp:
        try:
            temp_val = float(temp)
        except ValueError:
            return {"error": "Temperature must be a number"}, 400
        record.temperature = temp_val

    db.session.commit()
    return {"message": f"Record {id} updated successfully"}

#/delete/#
@app.route("/delete/<int:id>")
def delete_record(id):
    record = WeatherData.query.get(id)
    if not record:
        return {"error": "Record not found"}, 404

    db.session.delete(record)
    db.session.commit()

    return {"message": f"Record {id} deleted successfully"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
