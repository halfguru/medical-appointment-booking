# medical-appointment-booking
Medical appointment booking REST API

- A patient can search for the different providers of the clinic 
- A patient can look for the availabilities of a specific provider within a defined time interval (for instance, the availabilities of Dr. A between May 8th, 2019 and May 12th, 2019) 
- A patient can book an appointment with a provider by selecting one of their availabilities 

## Running Locally
You can run the Python application directly on your local operating system (this requires Python 3)
```
$ pip install -r requirements.txt
$ python ./app/app.py
```

## Running with Docker

You can build the application as a Docker image and run it:
```
$ docker build -t appointment-rest .
$ docker run -d -p 8080:8080 appointment-rest
```

## Documentation
You can consult the REST commands autogenerated documentation with Swagger UI at ``http://localhost:8080/ui``

## REST API endpoints

Here are some examples for the REST commands:

GET /providers
```
# Curl
curl -X GET --header 'Accept: application/json' 'http://localhost:8080/providers'
# Request URL
http://localhost:8080/providers
```

GET /providers/{first_name}_{last_name}
```
# Curl
curl -X GET --header 'Accept: application/json' 'http://localhost:8080/providers/John_Doe'
# Request URL
http://localhost:8080/providers/John_Doe
```

GET /availabilities
```
# Curl
curl -X GET --header 'Accept: application/json' 'http://localhost:8080/availabilities?provider_first_name=John&provider_last_name=Doe&start_time=2022-06-02&end_time=2022-06-03'
# Request URL
http://localhost:8080/availabilities?provider_first_name=John&provider_last_name=Doe&start_time=2022-06-02&end_time=2022-06-03
```

PUT /appointments
```
# Curl
curl -X PUT --header 'Content-Type: application/json' --header 'Accept: application/json' 'http://localhost:8080/appointments?patient_first_name=Simon&patient_last_name=Ho&provider_first_name=John&provider_last_name=Doe&start_time=2022-06-02%2014%3A00%3A00&end_time=2022-06-03%2014%3A15%3A00'
# Request URL
http://localhost:8080/appointments?patient_first_name=Simon&patient_last_name=Ho&provider_first_name=John&provider_last_name=Doe&start_time=2022-06-02%2014%3A00%3A00&end_time=2022-06-03%2014%3A15%3A00
```

## Database
The medical appointments are stored in a SQLite database. It's currently filled by default with a clinic, providers, patients and appointments for testing. It can be deleted to start from scratch or edited to manually add clinics, patients and providers.

## Stacks used
* [Python 3.9.5](https://www.python.org/downloads/release/python-395/) - Programming language
* [flask](https://github.com/pallets/flask) - Server framework
* [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - Database
* [connexion](https://github.com/spec-first/connexion) - OpenAPI specification framework
* [docker](https://www.docker.com/products/docker-desktop/) - Container
