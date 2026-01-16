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
- **语音模型**: Qwen3-Omni-30B-A3B-Instruct

## 功能特性

- ✅ 实时语音流处理
- ✅ 端到端语音模型调用
- ✅ 语音活动检测(VAD)
- ✅ 打断处理机制
- ✅ 多路并发支持
- ✅ 对话历史管理
- ✅ 日志记录
- ✅ TTS语音合成

## 项目结构

```
ai-phone-assistant/
├── app/                    # 核心应用代码
│   ├── __init__.py
│   ├── main.py             # FastAPI应用入口
│   ├── config.py           # 配置管理
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py       # HTTP API路由
│   │   └── websocket.py    # WebSocket端点
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── call_manager.py     # 呼叫管理
│   │   ├── audio_processor.py  # 音频处理
│   │   ├── model_client.py     # 远程模型客户端
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
├── tools/                  # 开发工具脚本
├── tests/                  # 测试用例
├── database/               # 数据库文件
├── logs/                   # 日志目录
├── recordings/             # 录音文件存储
├── text_to_audio.py        # 文本转音频工具
├── .env                    # 环境变量配置
├── .env.example
├── requirements.txt
└── README.md
```

## 环境要求

- Python 3.10+
- Conda (用于环境管理)

## 安装步骤

### 1. 创建Conda环境

```bash
conda create -n ljm_asr python=3.10 -y
```

### 2. 激活环境

```bash
conda activate ljm_asr
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

复制 `.env.example` 为 `.env` 并配置以下变量：

```bash
# 远程模型服务 (OpenAI兼容API)
REMOTE_MODEL_SERVICE_URL=http://10.246.32.45:8091
REMOTE_MODEL_SERVICE_API_KEY=                    # 可为空
REMOTE_MODEL_SERVICE_TIMEOUT=30

# 阿里云配置
ALIYUN_ACCESS_KEY_ID=your-access-key-id
ALIYUN_ACCESS_KEY_SECRET=your-access-key-secret
ALIYUN_CALL_CENTER_INSTANCE_ID=your-instance-id

# 其他配置见.env文件
```

## 运行服务

```bash
# 取消代理环境变量
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export no_proxy="10.246.32.45,localhost,127.0.0.1"

# 启动服务
cd /cpfs/user/zhaochenxu1/users/liujinming/git_program/ai-phone-assistant
PYTHONPATH=/cpfs/user/zhaochenxu1/users/liujinming/git_program/ai-phone-assistant \
  conda run -n ljm_asr python app/main.py

# 或使用uvicorn
PYTHONPATH=/cpfs/user/zhaochenxu1/users/liujinming/git_program/ai-phone-assistant \
  conda run -n ljm_asr uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

服务启动后访问：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## 工具脚本

### 文本转音频

```bash
cd /cpfs/user/zhaochenxu1/users/liujinming/git_program/ai-phone-assistant
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export no_proxy="10.246.32.45"
conda run -n ljm_asr python text_to_audio.py "你的问题"

# 输出: /cpfs/user/zhaochenxu1/users/liujinming/git_program/mp3/response.wav
```

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

## 支持的模型

| 模型 | 说明 |
|------|------|
| Qwen3-Omni-30B-A3B-Instruct | 语音/文本多模态模型 |
| API格式 | OpenAI兼容 |
| TTS格式 | 支持wav |

## 注意事项

### 代理配置

访问模型服务 `http://10.246.32.45:8091` 时需要取消代理：
```bash
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export no_proxy="10.246.32.45,localhost,127.0.0.1"
```

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
- 验证代理配置是否已取消
- 查看日志文件获取详细错误信息

## 许可证

MIT License
