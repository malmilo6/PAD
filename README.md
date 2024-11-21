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

<img width="604" alt="image" src="https://github.com/user-attachments/assets/48860e16-4b68-42a2-a712-cab895cea2b6">

	1.	The actor represents an end-user or another service making HTTP/1.1 requests to interact with the system.
	2.	Gateway: Serving as the system’s entry point, the Gateway receives HTTP requests from the actor and forwards them to back-end services via gRPC calls. It is responsible for interacting with the Service Discovery component to dynamically locate and route requests to appropriate services, ensuring flexibility and resilience as services scale or move.
	3.	Service Discovery: This component maintains a registry of services, such as the User Alert Service and Weather Data Service, and their instances. By helping the Gateway dynamically locate services, it enhances system scalability and fault tolerance, supporting a microservices architecture.
	4.	Redis Cluster/Ring (Shared Cache): Redis acts as a shared caching layer across the system. Frequently accessed data, such as session information, cached weather data, or user preferences, is stored here to improve performance and reduce the load on databases. Both the User Alert Service and Weather Data Service can access this shared cache to retrieve data efficiently.
	5.	User Alert Service: This service manages user-specific data and alert preferences. It relies on MongoDB (UAS DB) for storing user information, preferences, and alerts. MongoDB’s flexibility with unstructured data makes it suitable for handling diverse user profiles and alert settings. Additionally, the ETL Service pulls data from this service for analytical processing and storage in the Data Warehouse.
	6.	Weather Data Service: This service is dedicated to processing and storing weather-related information. It uses MySQL (WDS DB), a relational database, to store structured weather data that requires complex queries and transactional integrity. The Weather Data Service can also access the Redis cache for frequently requested weather information. As with the User Alert Service, data flows from this service to the ETL Service for warehousing.
	7.	ETL Service: The Extract, Transform, Load (ETL) Service gathers data from both the User Alert Service and Weather Data Service, processes it as needed, and loads it into the Data Warehouse. This warehouse serves as the central repository for aggregated and historical data, supporting analytics and reporting.
	8.	Data Warehouse: Acting as a consolidated data store, the Data Warehouse integrates data from multiple services for analytical purposes. This storage layer is optimized for complex queries and analysis, making it a valuable resource for generating insights from the system’s data.
	9.	Prometheus: Prometheus is employed for monitoring and collecting metrics across various services in the system. It gathers real-time data on service performance, health, and resource usage, enabling proactive system management.
	10.	Grafana: Connected to Prometheus, Grafana provides a visualization interface for the collected metrics. Through dashboards and visualizations, stakeholders can monitor system health, performance trends, and key metrics, supporting informed decision-making.

 The system architecture presented is designed to handle user interactions, manage data efficiently, and optimize performance through caching, monitoring, and service discovery. The Actor, which could represent an end-user or another service, initiates communication by making HTTP/1.1 requests to the Gateway. The Gateway functions as the system’s entry point, receiving these requests and forwarding them to various back-end services via gRPC calls. Additionally, the Gateway interacts with the Service Discovery component, which maintains a registry of services like the User Alert Service and Weather Data Service, allowing the Gateway to dynamically locate and route requests to these services, enhancing the resilience and scalability of the system. The Redis Cluster/Ring operates as a shared cache across the system, storing frequently accessed data such as session information, cached weather data, and user preferences to reduce the load on primary databases and improve performance. Both the User Alert Service, which manages user data and alert preferences, and the Weather Data Service, which processes weather data, can quickly access Redis for this purpose. For persistent storage, the User Alert Service relies on MongoDB for handling user information and alert settings, leveraging MongoDB’s flexibility for unstructured data. In contrast, the Weather Data Service uses MySQL, a relational database suited for structured weather records requiring complex queries and transactional integrity. Data from both services flows into an ETL Service, which extracts, transforms, and loads it into a central Data Warehouse. This warehouse consolidates data for analytics, supporting historical analysis and reporting. To monitor and visualize the system’s health and performance, Prometheus collects real-time metrics from each component, which are then visualized in Grafana through dashboards, providing insights into system trends and enabling proactive management. Overall, this modular architecture is optimized for scalability, performance, and observability, with each service operating independently to facilitate efficient data processing and responsive user interactions.

Communication and Data Flow:

	•	HTTP: Used by the actor to communicate with the Gateway.
	•	gRPC: Facilitates fast, low-latency communication between internal services (Gateway, User Alert Service, Weather Data Service, and ETL Service).
	•	Redis Cache: Both the User Alert Service and Weather Data Service can access Redis for frequently accessed data.
	•	Database Connections: MongoDB and MySQL serve as primary data stores for the User Alert Service and Weather Data Service, respectively.
	•	ETL to Data Warehouse: ETL processes data from User Alert and Weather Data services, transforming it as needed before storing it in the Data Warehouse.
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
   
3. **Set up DB Replication**
In master
```
CREATE USER 'replica_user'@'%' IDENTIFIED BY 'replica_password';
GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'%';
FLUSH PRIVILEGES;

SHOW MASTER STATUS;
```

In each slave
```
STOP SLAVE;

CHANGE MASTER TO
    MASTER_HOST='db_wds',
    MASTER_USER='replica_user',
    MASTER_PASSWORD='replica_password',
    MASTER_LOG_FILE='mysql-bin.000007', (check in SHOW MASTER)
    MASTER_LOG_POS=81859,
    GET_MASTER_PUBLIC_KEY=1;

START SLAVE;

SHOW SLAVE STATUS\G
```
In case of error
```
STOP SLAVE;
RESET SLAVE;
START SLAVE;
```
**Manual Failover**

Stop slave process
```
STOP SLAVE;
RESET SLAVE ALL;
```
Set RW status
```
SET GLOBAL read_only = OFF;
```
Now proceed with the steps defined in Setup DB replication.

4. **Testing**
Enter docker container (wds or uas) entering following commands, and then run pytest

   ```bash
   docker-compose build
   docker exec -it wds (or uas)
   pytest
