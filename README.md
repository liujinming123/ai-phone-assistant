# AI Phone Assistant

基于端到端语音模型的AI电话助理服务，支持实时语音对话、智能打断、多路并发。

## 技术栈

- **Web框架**: FastAPI + Uvicorn
- **实时通信**: WebSocket
- **音频处理**: NumPy + SciPy + PyDub
- **语音检测**: VAD (语音活动检测)
- **HTTP客户端**: HTTPx + aiohttp
- **日志**: Loguru
- **阿里云SDK**: alibabacloud-tea-openapi

## 功能特性

- ✅ 实时语音流处理
- ✅ 端到端语音模型调用
- ✅ 语音活动检测(VAD)
- ✅ 打断处理机制
- ✅ 多路并发支持
- ✅ 对话历史管理
- ✅ 日志记录

## 项目结构

```
AI_phone/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py        # HTTP API路由
│   │   └── websocket.py     # WebSocket端点
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── call_manager.py     # 呼叫管理
│   │   ├── audio_processor.py  # 音频处理
│   │   ├── model_client.py      # 远程模型客户端
│   │   ├── session_manager.py  # 会话管理
│   │   ├── vad_service.py      # VAD检测
│   │   └── logger_service.py   # 日志服务
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── conversation.py     # 对话模型
│   │   └── call.py             # 呼叫模型
│   │
│   └── utils/
│       └── __init__.py
│
├── logs/                    # 日志目录
├── recordings/              # 录音文件存储
├── database/                # 数据库文件
├── .env                     # 环境变量配置
├── requirements.txt          # Python依赖
└── README.md
```

## 环境要求

- Python 3.10+
- Conda (用于环境管理)

## 安装步骤

### 1. 创建Conda环境

```bash
~/miniconda3/Scripts/conda.exe create -n AI_phone python=3.10 -y
```

### 2. 激活环境

```bash
conda activate AI_phone
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

复制 `.env.example` 为 `.env` 并配置以下变量：

```bash
# 远程模型服务
MODEL_SERVICE_URL=http://your-model-service-url
MODEL_SERVICE_API_KEY=your-api-key

# 阿里云配置
ALIYUN_ACCESS_KEY_ID=your-access-key-id
ALIYUN_ACCESS_KEY_SECRET=your-access-key-secret
ALIYUN_CALL_CENTER_INSTANCE_ID=your-instance-id

# 其他配置见.env文件
```

## 运行服务

```bash
# 开发模式
python app/main.py

# 或使用uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

服务启动后访问：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## API接口

### HTTP API

#### 发起呼叫
```http
POST /api/call/initiate
Content-Type: application/json

{
  "phone_number": "13800138000",
  "prompt": "你是AI客服，请友善地与用户对话"
}
```

#### 查询呼叫状态
```http
GET /api/call/{call_id}
```

#### 结束呼叫
```http
POST /api/call/{call_id}/terminate
```

#### 获取对话记录
```http
GET /api/call/{call_id}/conversation
```

### WebSocket

#### 音频流端点
```
ws://localhost:8000/ws/call/{call_id}
```

消息格式：
- 客户端 → 服务端：二进制音频数据（PCM 8kHz）
- 服务端 → 客户端：二进制音频数据（PCM 16kHz，AI语音）
- 控制消息：JSON格式

## 注意事项

### PyAudio安装

在Windows上，PyAudio可能需要预编译的wheel文件：

1. 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. 下载对应Python 3.10和64位系统的whl文件
3. 安装：
```bash
pip install PyAudio-0.2.14-cp310-cp310-win_amd64.whl
```

### FFmpeg

pydub需要FFmpeg来处理音频文件：
- 下载：https://ffmpeg.org/download.html
- 解压并添加到系统PATH

### 阿里云SDK

确保Access Key有调用云呼叫中心的权限。

## 性能优化建议

1. **并发处理**: 使用asyncio进行异步处理
2. **音频缓冲**: 合理设置缓冲区大小
3. **VAD参数**: 根据实际使用调整
4. **连接池**: HTTP请求使用连接池

## 故障排查

### 依赖安装失败
- 检查Python版本是否为3.10+
- 确保conda环境已激活
- 尝试升级pip：`pip install --upgrade pip`

### 音频处理错误
- 检查音频格式和采样率
- 确认FFmpeg已正确安装

### API调用失败
- 检查.env配置是否正确
- 验证API Key是否有效
- 查看日志文件获取详细错误信息

## 许可证

MIT License
