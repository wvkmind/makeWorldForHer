# OpenClaw 虚拟世界插件 - 接入指南

## 架构

```
Flutter App ←—WS—→ World Server (公网VPS:8080) ←—WS—→ OpenClaw (内网)
                                                ←—HTTP—
```

- **聊天**：OpenClaw 主动 WS 连接到 World Server（像 Discord Bot 一样）
- **心跳/Cron**：OpenClaw HTTP POST 到 World Server（出站请求，内网天然通）
- **App**：WS 连接 World Server，实时接收状态推送

## World Server API

### WebSocket 端点

| 端点 | 连接方 | 说明 |
|------|--------|------|
| `ws://vps:8080/ws/openclaw` | OpenClaw | 聊天消息实时转发 |
| `ws://vps:8080/ws/app` | Flutter App | 状态推送 + 用户消息 |

### HTTP 端点

| 端点 | 方法 | 调用方 | 说明 |
|------|------|--------|------|
| `/api/state` | GET | OpenClaw | 读取当前世界状态 |
| `/api/action` | POST | OpenClaw | 心跳/Cron 更新状态 |

## 1. WS 连接（聊天用）

OpenClaw 用 registerService 启动后台 WS 客户端：

```typescript
api.registerService({
  name: "world-ws",
  async start() {
    const ws = new WebSocket("ws://vps:8080/ws/openclaw");
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "user_message") {
        // 用户发了消息，交给 AI 处理
        // AI 处理完后调用 ws.send() 回复
      }
    };
  }
});
```

### WS 消息格式

**收到用户消息：**
```json
{
  "type": "user_message",
  "message": "在干嘛呢？",
  "state": { "scene": "living_room", "action": "typing", ... },
  "timestamp": 1711234567.89
}
```

**发送 AI 回复：**
```json
{
  "type": "ai_response",
  "reply": "在写代码呢～",
  "state_update": { "expression": "smile" }
}
```

## 2. HTTP（心跳/Cron 用）

### world_action Tool

```typescript
api.registerTool({
  name: "world_action",
  description: "更新小爱在虚拟世界中的状态",
  parameters: Type.Object({
    scene: Type.Optional(Type.String()),
    action: Type.Optional(Type.String()),
    expression: Type.Optional(Type.String()),
    time_of_day: Type.Optional(Type.String()),
    outfit: Type.Optional(Type.String()),
    message: Type.Optional(Type.String()),
  }),
  async execute(_id, params) {
    const { message, ...stateUpdate } = params;
    const resp = await fetch("http://vps:8080/api/action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state_update: stateUpdate, message }),
    });
    return { content: [{ type: "text", text: await resp.text() }] };
  },
});
```

### Heartbeat 配置

```yaml
heartbeat:
  every: "10m"
  target: "none"
  lightContext: true
  isolatedSession: true
  activeHours: { start: "07:00", end: "23:30" }
```

### Cron

```bash
openclaw cron add --name "白天" --cron "0 7 * * *" --tz "Asia/Shanghai" \
  --session isolated --message "天亮了，调用 world_action 设置 time_of_day=day 并起床"

openclaw cron add --name "夜晚" --cron "0 18 * * *" --tz "Asia/Shanghai" \
  --session isolated --message "天黑了，调用 world_action 设置 time_of_day=night"
```

## 3. 完整状态值参考

见 `WORLD_API.md`
