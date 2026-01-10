# AI Phone Assistant - Quick Start Guide

## 1. Activate Conda Environment

```bash
conda activate AI_phone
```

## 2. Configure Environment Variables

Edit `C:/code/AI_phone/.env` and update:

```bash
# Remote Model Service
REMOTE_MODEL_SERVICE_URL=http://your-model-service-url
REMOTE_MODEL_SERVICE_API_KEY=your-api-key

# Alibaba Cloud
ALIYUN_ACCESS_KEY_ID=your-access-key-id
ALIYUN_ACCESS_KEY_SECRET=your-access-key-secret
ALIYUN_CALL_CENTER_INSTANCE_ID=your-instance-id
```

## 3. Start the Service

### Development Mode
```bash
cd C:/code/AI_phone
python app/main.py
```

### Or use Uvicorn
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 4. Verify Service is Running

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 5. Test with API

### Initiate a Call
```bash
curl -X POST "http://localhost:8000/api/call/initiate" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "13800138000",
    "prompt": "Hello, this is AI assistant"
  }'
```

### Check Call Status
```bash
curl http://localhost:8000/api/call/call_123
```

### Get Conversation
```bash
curl http://localhost:8000/api/call/call_123/conversation
```

## 6. Test WebSocket

Use a WebSocket client to connect to:
```
ws://localhost:8000/ws/call/call_123
```

Send audio data as binary (PCM 8kHz).

## 7. View Logs

Check logs in `C:/code/AI_phone/logs/` directory.

## Troubleshooting

### Port Already in Use
```bash
# Kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Log Errors
Check the log files in the `logs/` directory for detailed error messages.

## Service API Reference

### HTTP Endpoints

- `POST /api/call/initiate` - Initiate a phone call
- `GET /api/call/{call_id}` - Get call status
- `POST /api/call/{call_id}/terminate` - Terminate a call
- `GET /api/call/{call_id}/conversation` - Get conversation history

### WebSocket Endpoints

- `WS /ws/call/{call_id}` - Audio stream connection

## Configuration Reference

| Variable | Description | Default |
|----------|-------------|---------|
| HOST | Server host | 0.0.0.0 |
| PORT | Server port | 8000 |
| REMOTE_MODEL_SERVICE_URL | Model service URL | - |
| REMOTE_MODEL_SERVICE_API_KEY | Model service API key | - |
| AUDIO_SAMPLE_RATE | Audio sample rate (Hz) | 16000 |
| SILENCE_DURATION | Silence duration (ms) | 800 |
| LOG_LEVEL | Logging level | INFO |
