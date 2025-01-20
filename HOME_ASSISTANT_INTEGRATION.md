# Home Assistant API Integration

This document outlines the integration with Home Assistant for smart home control.

## Key Features

1. **Device Control**
   - Light control
   - Thermostat management
   - Security system integration
   - Media control

2. **Automation Management**
   - Trigger automation routines
   - Modify automation settings
   - Monitor automation status

3. **State Monitoring**
   - Real-time device status
   - Energy usage tracking
   - Environment monitoring

## API Endpoints and Examples

### 1. Device Control
```javascript
// Turn on living room light
await fetch('http://homeassistant.local:8123/api/services/light/turn_on', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.HOME_ASSISTANT_TOKEN}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    entity_id: 'light.living_room'
  })
});
```

### 2. State Monitoring
```javascript
// Get thermostat status
const response = await fetch('http://homeassistant.local:8123/api/states/climate.living_room', {
  headers: {
    'Authorization': `Bearer ${process.env.HOME_ASSISTANT_TOKEN}`
  }
});
const data = await response.json();
console.log(`Current temperature: ${data.state}`);
```

### 3. Automation Trigger
```javascript
// Trigger good morning routine
await fetch('http://homeassistant.local:8123/api/services/automation/trigger', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.HOME_ASSISTANT_TOKEN}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    entity_id: 'automation.good_morning'
  })
});
```

### 4. Event Streaming
```javascript
const ws = new WebSocket('ws://homeassistant.local:8123/api/websocket');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.event?.event_type === 'state_changed') {
    console.log('State changed:', data.event.data);
  }
};
```

## Authentication

1. **Long-Lived Access Token**
   - Generate token in Home Assistant
   - Store securely in environment variables
   - Use for API authentication

2. **Example Request**
```javascript
const response = await fetch('http://homeassistant.local:8123/api/states', {
  headers: {
    'Authorization': `Bearer ${process.env.HOME_ASSISTANT_TOKEN}`,
    'Content-Type': 'application/json'
  }
});
```

## Error Handling and Recovery

### 1. Authentication Errors (401)
```javascript
if (response.status === 401) {
  // Refresh token logic
  const newToken = await refreshToken();
  // Update environment variable
  process.env.HOME_ASSISTANT_TOKEN = newToken;
  // Retry request with new token
  return await makeRequestWithRetry(request);
}
```

### 2. Entity Not Found (404)
```javascript
if (response.status === 404) {
  // Validate entity exists
  const entities = await getAllEntities();
  if (!entities.includes(requestedEntity)) {
    throw new Error(`Entity ${requestedEntity} does not exist`);
  }
  // Check entity naming convention
  if (!isValidEntityName(requestedEntity)) {
    throw new Error(`Invalid entity name format: ${requestedEntity}`);
  }
}
```

### 3. Server Errors (500)
```javascript
const MAX_RETRIES = 3;
const BASE_DELAY = 1000; // 1 second

async function makeRequestWithRetry(request, retries = 0) {
  try {
    const response = await fetch(request);
    if (response.status === 500 && retries < MAX_RETRIES) {
      const delay = BASE_DELAY * Math.pow(2, retries);
      await new Promise(resolve => setTimeout(resolve, delay));
      return makeRequestWithRetry(request, retries + 1);
    }
    return response;
  } catch (error) {
    if (retries < MAX_RETRIES) {
      const delay = BASE_DELAY * Math.pow(2, retries);
      await new Promise(resolve => setTimeout(resolve, delay));
      return makeRequestWithRetry(request, retries + 1);
    }
    throw error;
  }
}
```

### 4. Service Unavailable (503)
```javascript
if (response.status === 503) {
  // Notify user
  sendNotification('Home Assistant service is currently unavailable');
  
  // Check service status
  const status = await checkServiceStatus();
  if (status === 'maintenance') {
    // Handle maintenance mode
    scheduleRetryAfterMaintenance();
  } else {
    // Handle temporary outage
    scheduleRetryWithBackoff();
  }
}
```

## Next Steps

1. Generate long-lived access token
2. Implement device control endpoints
3. Add state monitoring
4. Create integration tests
