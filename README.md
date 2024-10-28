# PAD - Severe Weather Alert Service


## Application Suitability
### Complex Data Handling
Handle and process large volumes of diverse meteorological data efficiently and accurate alert generation.
### Independence and Scalability
Each service is designed to operate independently and is scalable to handle variations in data volume and user load, especially during severe weather events.
## Service Boundaries
### Weather Alert Service
Responsible for ingesting weather data, processing it to detect severe conditions, and generating relevant alerts.

Operates independently with its own database and caching mechanisms to ensure performance and reliability.
### User Alert Service
Manages user data and preferences, receives alerts from the processing service, and delivers these alerts to users via various channels. 

Manages its own user database and handles communication back to the data processing service for feedback on delivery success.

![image](https://github.com/user-attachments/assets/4482fbda-f803-4671-9840-956924c38381)

The actor, which could be an end-user or another service, interacts with the system by making HTTP/1.1 requests to the Gateway.

The Gateway serves as entry point and communicates with back-end services through gRPC calls. It's also responsible for interacting with the Service Discovery component to locate services within the architecture.

Service Discovery is responsible for maintaining a registry of services (like User Alert Service and Weather Data Service) and their instances. It helps the Gateway locate these services dynamically, aiding in the resilience and scalability of the system.

These two services handle specific business logic. The User Alert Service manages user data and alert preferences and relies on MongoDB for data storage. The Weather Data Service processes and stores weather data using MySQL.

Redis is utilized as a shared cache, likely to store frequently accessed data like session information, cached weather data, or user preferences. Both services can quickly access this shared cache to improve performance and reduce database load.

MongoDB and MySQL are used for persisting different types of data. MongoDB, being a NoSQL database, is likely used here for its flexibility in handling unstructured data, such as user profiles or alert settings. MySQL, a relational database, is suitable for structured data like weather records which require complex queries and transactional integrity.
## Technology Stack and Communication Patterns
### Weather Alert Service
**Technologies:** Utilizes gRPC for efficient communication with the notification service, databases for persistent storage, and caching mechanisms to enhance access to frequently used data. 

**Communication:** Implements gRPC for fast, reliable, and secure inter-service communication.
### User Alert Service
**Technologies:** WebSockets for real-time alert notifications to clients, a relational database to manage user information and preferences.

Both microservices use Python (Django), and NodeJs for Gateway.

**Communication:** Uses gRPC for server-to-server communication and WebSockets for real-time client updates.
### Gateway
1.  Directs requests for data processing and alert notifications to the respective services.
2. Distributes incoming requests evenly across services to optimize performance and reduce the risk of overloading any single component.
3. Stores frequently accessed data like weather conditions to speed up response times for common queries.

## Data Management
Uses a database for storing raw and processed weather data, and user data. Mongo DB for User Alert Service, storing user data, and preferences. MySQL for Weather Data Service, store and process weather data.

## Deployment and Scaling
Both services are containerized using Docker, allowing for consistency across development, testing, and production environments. 

Includes load balancing within each service to distribute requests evenly across instances, enhancing reliability and responsiveness.

Continuous monitoring of both services' performance and health via endpoints, with automated scaling to maintain optimal performance levels.

# API Documentation

# Get Weather Prediction (Direct)

**Endpoint**: `GET /api/v1/weather-prediction/:location`

- **Description**: Direct retrieval of weather prediction for a specified location.
- **URL**: `http://localhost:8001/api/v1/weather-prediction/New york`
- **Method**: GET

**Response**:
- Status 200: Weather prediction data for the specified location.
# Gateway Health

**Endpoint**: `GET /api/v1/health`

- **Description**: Checks the health status of the gateway.
- **URL**: `http://localhost:3000/api/v1/health`
- **Method**: GET

**Response**:
- Status 200: Gateway service is healthy.


# Service List

**Endpoint**: `GET /services`

- **Description**: Retrieves a list of registered services.
- **URL**: `http://localhost:5000/services`
- **Method**: GET

**Response**:
- Status 200: List of registered services.

# Register Service Discovery

**Endpoint**: `POST /register`

- **Description**: Registers a service with the Service Discovery service.
- **URL**: `http://localhost:5000/register`
- **Method**: POST

**Request Body (JSON)**:
```json
{
    "name": "service_name",
    "ip": "123",
    "port": "123"
}
```


# Generate Report

**Endpoint**: `GET /api/v1/generate-report/:location`

- **Description**: Generates a weather report for a specified location.
- **URL**: `http://localhost:8001/api/v1/generate-report/Houston`
- **Method**: GET

**Response**:
- Status 200: Generated report data.

# Gateway UAS - Get Prediction with Load Balancing

**Endpoint**: `GET /api/v1/weather-prediction/:location`

- **Description**: Retrieves weather prediction for a specified location via the gateway with load balancing.
- **URL**: `http://localhost:3000/api/v1/weather-prediction/Los Angeles`
- **Method**: GET

**Response**:
- Status 200: Weather prediction data for the specified location.

---

# CRUD WDS Prediction

**Endpoint**: `GET /api/v1/weather-prediction/:location`

- **Description**: CRUD operations for weather predictions in WDS.
- **URL**: `http://localhost:8000/api/v1/weather-prediction/`
- **Method**: GET/POST/UPDATE/DELETE

**Response**:
- Status 200: Weather prediction data.

# CRUD WDS Weather Data

**Endpoint**: `GET /api/v1/weather-data/`

- **Description**: CRUD operations for weather data in WDS.
- **URL**: `http://localhost:8000/api/v1/weather-data/`
- **Method**: GET/POST/UPDATE/DELETE

**Request Body (JSON)**:
```json
{
    "id": 1,
    "location": "New York",
    "temperature": 11.5,
    "wind_speed": 0.79,
    "precipitation": 40.55,
    "timestamp": "2024-09-22T15:37:42.554245Z"
}
```

# Gateway UAS - Get Current Weather (GRPC)

**Endpoint**: `GET /api/v1/current-weather/:location`

- **Description**: Retrieves the current weather for a specified location through the gateway.
- **URL**: `http://localhost:3000/api/v1/current-weather/houston`
- **Method**: GET

**Response**:
- Status 200: Current weather data for the specified location.

# Health WDS

**Endpoint**: `GET /api/v1/health`

- **Description**: Checks the health status of the Weather Data Service (WDS).
- **URL**: `http://localhost:8000/api/v1/health`
- **Method**: GET

**Response**:
- Status 200: Service is healthy.

# Health UAS

**Endpoint**: `GET /api/v1/health`

- **Description**: Checks the health status of the User Alert Service (UAS).
- **URL**: `http://localhost:8001/api/v1/health`
- **Method**: GET

**Response**:
- Status 200: Service is healthy.

## Deployment and Testing

### Prerequisites
- **Docker**: Ensure Docker is installed to run the services in isolated containers.
- **Docker Compose**: Used to define and run multi-container applications.

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/malmilo6/PAD.git
   cd pad-project
   
2. **Build and up the image**
To be able to access to get data, ensure to run GRPC on WDS after running the container, following the command inside the WDS container

   ```bash
   docker-compose build
   docker-compose up
   python manage.py run_grpc_server

   
3. **Testing**
Enter docker container (wds or uas) entering following commands, and then run pytest

   ```bash
   docker-compose build
   docker exec -it wds (or uas)
   pytest
