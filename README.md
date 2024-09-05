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
## Technology Stack and Communication Patterns
### Weather Alert Service
**Technologies:** Utilizes gRPC for efficient communication with the notification service, databases for persistent storage, and caching mechanisms to enhance access to frequently used data.\

**Communication:** Implements gRPC for fast, reliable, and secure inter-service communication.
### User Alert Service
**Technologies:** WebSockets for real-time alert notifications to clients, a relational database to manage user information and preferences.

**Communication:** Uses gRPC for server-to-server communication and WebSockets for real-time client updates.
### Gateway
1.  Directs requests for data processing and alert notifications to the respective services.
2. Distributes incoming requests evenly across services to optimize performance and reduce the risk of overloading any single component.
3. Stores frequently accessed data like weather conditions to speed up response times for common queries.

## Data Management
Uses a database for storing raw and processed weather data, and user data.

## Deployment and Scaling
Both services are containerized using Docker, allowing for consistency across development, testing, and production environments. 

Includes load balancing within each service to distribute requests evenly across instances, enhancing reliability and responsiveness.

Continuous monitoring of both services' performance and health via endpoints, with automated scaling to maintain optimal performance levels.