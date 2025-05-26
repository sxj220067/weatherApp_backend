git clone the file

open terminal

cd to the file given

pip install -r requirements.txt

export OPENWEATHER_API_KEY="your_api_key"

python3 create_db.py

python3 mainapp.py

API Endpoints
GET/ 
response {"message": "weather API running"}

GET /weather?lat=51&lon=-0.45
response 
{
  "location": "51,52",
  date: "2025-05-26",
  "temperature": somenumber
}

GET /export/json
response
[
{
  "location": "51,52",
  date: "2025-05-26",
  "temperature": somenumber
}
]
PUT /update/<id>?location=<new>&date =<new>&temp=<new>
reponse will update the already stored data

Delete /delete/<id>
response will delete the <id> data
