# Ambrosio API Reference

This document provides detailed information about Ambrosio's API endpoints and interfaces.

## Core API Endpoints

### 1. Voice Interface API

#### Start Voice Session
- **Endpoint**: `/api/voice/start`
- **Method**: POST
- **Request**:
  ```json
  {
    "session_id": "string",
    "language": "pt-PT"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "websocket_url": "wss://your-server/ws/voice"
  }
  ```

#### Stop Voice Session
- **Endpoint**: `/api/voice/stop`
- **Method**: POST
- **Request**:
  ```json
  {
    "session_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success"
  }
  ```

### 2. Home Assistant Control API

#### Get Devices
- **Endpoint**: `/api/home-assistant/devices`
- **Method**: GET
- **Response**:
  ```json
  {
    "devices": [
      {
        "id": "string",
        "name": "string",
        "type": "light|switch|sensor",
        "state": "on|off",
        "room": "string"
      }
    ]
  }
  ```

#### Control Device
- **Endpoint**: `/api/home-assistant/control`
- **Method**: POST
- **Request**:
  ```json
  {
    "device_id": "string",
    "action": "turn_on|turn_off|toggle",
    "parameters": {}
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "new_state": "on|off"
  }
  ```

## WebSocket Interfaces

### Voice Stream
- **URL**: `wss://your-server/ws/voice`
- **Protocol**:
  - Client sends audio frames
  - Server responds with:
    ```json
    {
      "text": "recognized text",
      "intent": "device_control|query|other",
      "response": "text response"
    }
    ```

## Error Responses

All endpoints return standardized error responses:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

## Rate Limiting

- 100 requests/minute per IP
- 10 concurrent WebSocket connections per user

## Authentication

All endpoints require authentication via API key:

```bash
Authorization: Bearer YOUR_API_KEY
```

## Versioning

API version is included in the URL:

```
/api/v1/...
```

## Testing Endpoints

### Health Check
- **Endpoint**: `/api/health`
- **Method**: GET
- **Response**:
  ```json
  {
    "status": "ok",
    "services": {
      "voice": "up",
      "home_assistant": "up"
    }
  }
  ```

### Echo Test
- **Endpoint**: `/api/echo`
- **Method**: POST
- **Request**:
  ```json
  {
    "message": "string"
  }
  ```
- **Response**:
  ```json
  {
    "echo": "string"
  }
