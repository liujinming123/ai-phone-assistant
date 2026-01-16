# AI Phone Assistant - Quick Start Guide

## 1. Activate Conda Environment

```bash
conda activate ljm_asr
```

## 2. Configure Environment Variables

Edit `/cpfs/user/zhaochenxu1/users/liujinming/git_program/ai-phone-assistant/.env`:

```bash
# Remote Model Service (OpenAI compatible API)
REMOTE_MODEL_SERVICE_URL=http://10.246.32.45:8091
REMOTE_MODEL_SERVICE_API_KEY=
REMOTE_MODEL_SERVICE_TIMEOUT=30

# Alibaba Cloud
ALIYUN_ACCESS_KEY_ID=your-access-key-id
ALIYUN_ACCESS_KEY_SECRET=your-access-key-secret
ALIYUN_CALL_CENTER_INSTANCE_ID=your-instance-id
```

## 3. Start the Service

### Remove Proxy Settings
```bash
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export no_proxy="10.246.32.45,localhost,127.0.0.1"
```

### Development Mode
```bash
cd /cpfs/user/zhaochenxu1/users/liujinming/git_program/ai-phone-assistant
PYTHONPATH=/cpfs/user/zhaochenxu1/users/liujinming/git_program/ai-phone-assistant \
  conda run -n ljm_asr python app/main.py
```

### Or use Uvicorn
```bash
cd /cpfs/user/zhaochenxu1/users/liujinming/git_program/ai-phone-assistant
PYTHONPATH=/cpfs/user/zhaochenxu1/users/liujinming/git_program/ai-phone-assistant \
  conda run -n ljm_asr uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
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

## 6. Test Model API

### Text Chat
```bash
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export no_proxy="10.246.32.45"

curl -X POST "http://10.246.32.45:8091/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "/vepfs/public/model-public/Qwen3-Omni-30B-A3B-Instruct",
    "messages": [
      {"role": "user", "content": "你好，请介绍一下自己"}
    ],
    "max_tokens": 100
  }'
```

### Text to Speech
```bash
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export no_proxy="10.246.32.45"

curl -X POST "http://10.246.32.45:8091/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "/vepfs/public/model-public/Qwen3-Omni-30B-A3B-Instruct",
    "input": "你好，我是AI助手",
    "voice": "alloy",
    "response_format": "wav"
  }' -o response.wav
```

## 7. Test Text to Audio Tool

```bash
cd /cpfs/user/zhaochenxu1/users/liujinming/git_program/ai-phone-assistant
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export no_proxy="10.246.32.45"

conda run -n ljm_asr python text_to_audio.py "请介绍一下你的功能"

# Output: /cpfs/user/zhaochenxu1/users/liujinming/git_program/mp3/response.wav
```

## 8. Test WebSocket

Use a WebSocket client to connect to:
```
ws://localhost:8000/ws/call/call_123
```

Send audio data as binary (PCM 8kHz).

## 9. View Logs

Check logs in `/cpfs/user/zhaochenxu1/users/liujinming/git_program/ai-phone-assistant/logs/` directory.

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

### Proxy Issues
```bash
# Make sure to unset proxy variables
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export no_proxy="10.246.32.45,localhost,127.0.0.1"
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
