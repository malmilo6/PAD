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

## System Diagram
![Screenshot_1](https://github.com/user-attachments/assets/363b922f-46c1-402e-b03e-0436b3c6bcb5)

# API Documentation

## Weather Alert Service

### 1. Retrieve Weather Data
Retrieve all weather data entries for a specific location, or all entries if no location is specified.

- **URL**: `/weather/`
- **Method**: `GET`
- **URL Params**: 
  - Optional: `location=[string]`
- **Success Response**:
  - **Code**: 200
  - **Content**: Array of weather data objects
- **Error Response**:
  - **Code**: 404 NOT FOUND
  - **Content**: `{ error : "Data not found" }`

### 2. Get Future Weather Alerts
Get future weather alerts for a specified location.

- **URL**: `/weather/alerts/future/`
- **Method**: `GET`
- **Query Params**: 
  - Required: `location=[string]`
- **Success Response**:
  - **Code**: 200
  - **Content**: Array of future weather alert objects
- **Error Response**:
  - **Code**: 404 NOT FOUND
  - **Content**: `{ error : "Alerts not found for location" }`

### 3. Create Weather Data Entry
Create a new weather data entry.

- **URL**: `/weather/create/`
- **Method**: `POST`
- **Data Params**:
  ```json
  {
    "timestamp": "[datetime]",
    "location": "[string]",
    "temperature": "[float]",
    "humidity": "[float]",
    "wind_speed": "[float]",
    "weather_condition": "[string]"
  }
- **Success Response**:
  - **Code**: 201 CREATED
- **Error Response**:
  - **Code**: 404 NOT FOUND
  - **Content**: `{ error : "Invalid data" }`

#### 4. Delete Weather Data Entry
- **Endpoint**: `DELETE /weather/delete/{id}/`
- **Description**: Delete a specific weather data entry.
- **URL Params**:
  - `id` (required): The ID of the weather data entry to delete.
- **Success Response**:
  - **Code**: 204 NO CONTENT
- **Error Response**:
  - **Code**: 404 NOT FOUND
  - **Content**: `{ "error" : "Data not found" }`

#### 5. Retrieve Severe Weather Alert Prediction
- **Endpoint**: `GET /weather/predictions/`
- **Description**: Retrieve predictions for severe weather based on current data trends.
- **Success Response**:
  - **Code**: 200
  - **Content**: Array of prediction data
- **Error Response**:
  - **Code**: 404 NOT FOUND
  - **Content**: `{ "error" : "Predictions not available" }`

## User Alert Service

#### 1. Get Weather Report for Location
- **Endpoint**: `GET /profiles/weather-report/`
- **Description**: Get a detailed weather report for a specified location.
- **Query Params**:
  - `location` (required)
- **Success Response**:
  - **Code**: 200
  - **Content**: Weather report data
- **Error Response**:
  - **Code**: 404 NOT FOUND
  - **Content**: `{ "error" : "Location not found" }`

#### 2. Update User Alert Preferences
- **Endpoint**: `PATCH /profiles/update/{id}/`
- **Description**: Update the alert preferences associated with a user profile.
- **URL Params**:
  - `id` (required)
- **Data Params**:
  ```json
  {
    "alert_preferences": {
      "email": "boolean",
      "sms": "boolean",
      "push_notification": "boolean"
    }
  }
- **Success Response**:
  - **Code**: 200
  - **Content**: `{ "message": "Preferences updated successfully." }`
- **Error Response**:
  - **Code**: 404 BAD REQUEST
  - **Content**: `{ "error": "Invalid request" }`

#### 3. WS Communication
- **WS URL**: `ws://[host]/ws/alerts/`
- **Protocol**: WebSocket
- **Functionality**:
  - **Clients connect to receive real-time alerts.**
  - **Server sends alert messages when conditions meet user-specified preferences.**
