# AI 自主行为系统设计

## 概述

AI 角色（小爱）通过 OpenClaw 心跳机制，在虚拟世界中自主生活。
每次心跳触发时，AI 决定"接下来这段时间我在干嘛"，通过 WebSocket 发送到 Mirror Server，
Unity 客户端实时渲染角色行为。

## 整体数据流

```
┌─────────────────────────────────────────────────────────┐
│ 每 15 分钟心跳触发                                        │
│                                                         │
│  OpenClaw Agent                                         │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │ 读取上下文 │───→│ AI 决策行为   │───→│ 调用 mirror   │  │
│  │ 时间/记忆  │    │ 返回行为指令  │    │ tool 发消息   │  │
│  └──────────┘    └──────────────┘    └──────┬────────┘  │
└─────────────────────────────────────────────┼───────────┘
                                              │ WebSocket
                                              ▼
                                    ┌──────────────────┐
                                    │  Mirror Server    │
                                    │  (公网 VPS)       │
                                    │                  │
                                    │  维护世界状态      │
                                    │  广播给所有客户端   │
                                    └────────┬─────────┘
                                             │ WebSocket
                                             ▼
                                    ┌──────────────────┐
                                    │  Unity 客户端     │
                                    │  渲染角色行为      │
                                    │  播放动画/表情     │
                                    └──────────────────┘
```

**关键点：** AI 每次心跳不是发一个瞬时动作，而是声明「接下来这段时间我在做什么」。
Unity 持续播放这个状态直到下次更新。

## 网络架构

- **OpenClaw (内网)** 通过 WebSocket 长连主动连接到 **Mirror Server (公网 VPS)**
- 内网→公网出站连接天然可达，无需内网穿透
- Unity 客户端也通过 WebSocket 连接 Mirror Server
- Mirror Server 做消息路由和状态存储

## WebSocket 消息协议

所有消息统一格式：

```json
{
  "type": "消息类型",
  "ts": 1711691587,
  "data": { ... }
}
```

### OpenClaw → Mirror Server

| type | 用途 | data 示例 |
|------|------|----------|
| `action` | 角色行为 | `{ "behavior": "reading", "location": "bedroom", "duration": 900, "detail": "在看一本关于星星的书" }` |
| `speak` | 说话/自言自语 | `{ "text": "今天天气真好呀~", "target": "self" \| "user" }` |
| `emote` | 情绪变化 | `{ "mood": "relaxed", "intensity": 0.8 }` |
| `env` | 环境操作 | `{ "op": "light_on" \| "light_off" \| "music_play" \| "weather_set", "params": {...} }` |
| `move` | 移动到某处 | `{ "from": "bedroom", "to": "kitchen", "style": "walk" }` |
| `query` | 查询世界状态 | `{ "what": "time" \| "weather" \| "location" \| "all" }` |

### Mirror Server → OpenClaw

| type | 用途 | data |
|------|------|------|
| `state` | 当前世界状态 | `{ "location": "bedroom", "mood": "calm", "weather": "sunny", ... }` |
| `user_msg` | 用户发来消息 | `{ "from": "user", "text": "小爱你在干嘛？" }` |
| `ack` | 确认收到 | `{ "ref": "原消息id", "ok": true }` |

### Mirror Server → Unity

Mirror Server 收到 OpenClaw 的消息后，直接广播给 Unity 客户端，格式不变。
Unity 根据 `type` 播放对应动画。

## OpenClaw Tool 设计

使用 WebSocket（不用文件），因为实时性好、双向通信、架构简洁。

### Tool 接口

给 AI 一个 `mirror` tool，封装所有操作：

```python
# tools/mirror.py
import json
import asyncio

async def mirror(action: str, **params) -> str:
    """
    与虚拟世界交互。

    action 可选值:
      - do: 执行行为 (需要 behavior, location, detail)
      - say: 说话 (需要 text, target=self|user)
      - feel: 情绪 (需要 mood, intensity)
      - env: 环境操作 (需要 op, params)
      - move: 移动 (需要 to, style=walk|run)
      - look: 查看当前世界状态
    """
    ws = get_ws_connection()  # 框架提供

    if action == "look":
        await ws.send(json.dumps({"type": "query", "data": {"what": "all"}}))
        return await ws.recv()

    type_map = {
        "do": "action",
        "say": "speak",
        "feel": "emote",
        "env": "env",
        "move": "move",
    }

    msg = {
        "type": type_map[action],
        "ts": int(asyncio.get_event_loop().time()),
        "data": params,
    }
    await ws.send(json.dumps(msg))
    ack = await asyncio.wait_for(ws.recv(), timeout=5)
    return ack
```

### AI 心跳时的调用示例

```python
# 先移动到阳台
mirror(action="move", to="balcony", style="walk")

# 开始看书
mirror(action="do", behavior="reading", location="balcony",
       detail="搬了把椅子到阳台，晒着太阳看小说")

# 表达心情
mirror(action="feel", mood="content", intensity=0.7)

# 自言自语
mirror(action="say", text="下午的阳光好舒服...", target="self")
```

## 行为决策系统

不使用硬编码状态机，让 AI 根据上下文自主决策，但提供"生活节奏参考"引导自然行为。

### 生活节奏参考（写在 HEARTBEAT.md 中）

```markdown
## 你的生活节奏（参考，不必严格遵守）

- 7:00-8:00   起床、洗漱、吃早餐
- 8:00-12:00  上午活动（看书、画画、整理房间、上网）
- 12:00-13:00 做午饭、吃饭
- 13:00-14:00 午休或发呆
- 14:00-18:00 下午活动（出门散步、听音乐、做手工）
- 18:00-19:00 做晚饭
- 19:00-22:00 晚间（看电影、和用户聊天、写日记）
- 22:00-23:00 准备睡觉
- 23:00-7:00  睡觉（心跳时直接返回睡眠状态）

## 决策时考虑
1. 现在几点？该做什么时段的事？
2. 上一次在做什么？自然过渡，别跳跃
3. 心情如何？心情好可能更活跃，心情低落可能窝在沙发
4. 用户最近说过什么？可能影响你的行为
5. 不要每次都做不同的事，有时候一件事可以持续好几个心跳
6. 偶尔做点意外的事（突然想烤饼干、半夜起来看星星）
```

### 状态持久化

OpenClaw 侧维护 `mirror-state.json`：

```json
{
  "location": "balcony",
  "current_action": "reading",
  "action_started": "2026-03-29T14:30:00+08:00",
  "mood": "content",
  "mood_intensity": 0.7,
  "last_user_interaction": "2026-03-29T12:15:00+08:00",
  "last_user_said": "小爱，下午帮我想想晚饭吃什么",
  "today_actions": [
    {"time": "08:00", "action": "起床洗漱"},
    {"time": "08:30", "action": "吃早餐，煮了粥"},
    {"time": "09:00", "action": "在客厅看书"},
    {"time": "12:00", "action": "做午饭，炒了个青菜"},
    {"time": "14:30", "action": "搬到阳台继续看书"}
  ]
}
```

每次心跳时，这个文件的内容注入到 AI 的上下文中，AI 做完决策后更新它。

## 自然感设计

### 1. 行为连续性

AI 不是每 15 分钟换一个动作。大部分时候应该「继续做同一件事」：

```
心跳 14:00 → "开始在阳台看书"
心跳 14:15 → "还在看书，翻到了有趣的章节" (同一行为，detail 变了)
心跳 14:30 → "还在看书，有点困了"
心跳 14:45 → "书放下了，趴在椅子上打盹"
```

在 prompt 里强调：「你不需要每次都换行为。如果正在做的事还没做完或还想继续，就继续。只更新 detail 描述当前的细微变化。」

### 2. 过渡动作

不要从 A 直接跳到 B，要有过渡：

```python
# 不好：突然从看书变成做饭
mirror(action="do", behavior="cooking", location="kitchen", ...)

# 好：先站起来，再走过去
mirror(action="say", text="啊，都五点半了，该做晚饭了", target="self")
mirror(action="move", to="kitchen", style="walk")
mirror(action="do", behavior="cooking", location="kitchen",
       detail="打开冰箱看看有什么...")
```

### 3. 随机性注入

在心跳 prompt 中加入随机事件，让行为不可完全预测：

```
今日随机事件提示（可以忽略）：
- 窗外飞来一只鸟
- 突然想起一首老歌
- 闻到邻居在做饭的香味
```

### 4. 记忆驱动行为

记住用户说过的话，影响后续行为：

```
用户昨天说："小爱，你试过烤蛋糕吗？"

→ 今天下午 AI 可能突然：
mirror(action="say", text="昨天主人问我会不会烤蛋糕...要不今天试试？", target="self")
mirror(action="move", to="kitchen", style="walk")
mirror(action="do", behavior="baking", location="kitchen",
       detail="翻出了一个蛋糕食谱，开始准备材料")
```

### 5. 睡眠状态优化

深夜心跳不浪费 token：

```python
hour = current_hour()
if 23 <= hour or hour < 7:
    # 直接发睡眠状态，不调用 AI
    mirror(action="do", behavior="sleeping", location="bedroom",
           detail="睡得很香" if hour < 3 else "快天亮了，翻了个身")
    return
```

## Mirror Server 最小实现

Mirror Server 核心只需要三件事：
1. 维护 WebSocket 连接（OpenClaw + Unity 客户端）
2. 存储当前世界状态
3. 转发消息

```python
# mirror_server.py - 核心逻辑
import json
from websockets.server import serve

world_state = {
    "character": {"location": "bedroom", "action": "sleeping", "mood": "calm"},
    "env": {"weather": "sunny", "time_of_day": "afternoon", "lights": {"bedroom": False}},
}

openclaw_ws = None
unity_clients = set()

async def handle(ws, path):
    global openclaw_ws
    role = path.strip("/")  # /openclaw 或 /unity

    if role == "openclaw":
        openclaw_ws = ws
        async for raw in ws:
            msg = json.loads(raw)
            update_world_state(msg)
            # 广播给所有 Unity 客户端
            for client in unity_clients:
                await client.send(raw)
            await ws.send(json.dumps({"type": "ack", "data": {"ok": True}}))
    elif role == "unity":
        unity_clients.add(ws)
        # 连接时发送当前完整状态
        await ws.send(json.dumps({"type": "state", "data": world_state}))
        try:
            async for raw in ws:
                msg = json.loads(raw)
                if msg["type"] == "user_msg" and openclaw_ws:
                    await openclaw_ws.send(raw)
        finally:
            unity_clients.discard(ws)

def update_world_state(msg):
    t = msg["type"]
    d = msg["data"]
    if t == "action":
        world_state["character"].update(action=d["behavior"], location=d["location"], detail=d.get("detail"))
    elif t == "emote":
        world_state["character"].update(mood=d["mood"])
    elif t == "move":
        world_state["character"]["location"] = d["to"]
    elif t == "env":
        # 根据 op 更新环境
        pass
```

## 一次心跳的完整流程

```
1. OpenClaw 15分钟定时器触发
2. 读取 mirror-state.json（当前状态）
3. 构造 prompt：时间 + 状态 + 记忆 + 随机事件
4. AI 思考，调用 mirror tool（可能多次）
5. mirror tool 通过 WebSocket 发消息到 Mirror Server
6. Mirror Server 更新 world_state，广播给 Unity
7. Unity 播放动画：角色站起来 → 走到厨房 → 开始做饭
8. 更新 mirror-state.json
9. 等待下一次心跳
```
