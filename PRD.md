# OpenClaw Virtual World - PRD

## 概述

构建一个 Unity 虚拟世界，用户可以在其中与 AI 角色（小爱）实时对话和互动。
AI 通过 OpenClaw 控制虚拟角色的状态和行为，预生成图片作为角色表现层。

## 核心目标

- 用户在 Unity 3D 场景中与 AI 角色面对面交流
- AI 角色有丰富的状态表现（表情、动作、场景、服装）
- 对话走 OpenClaw，复用现有的 memory/persona/tool 体系
- 低成本：预生成图片，AI 只输出状态码，不实时生成图

## 架构

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────┐
│  Unity 客户端 │◄──WS──►│  Mirror 服务器     │◄──HTTP──►│  OpenClaw    │
│  (手机/PC)   │         │  (Linux VPS)      │         │  Gateway API │
│             │         │                  │         │             │
│ - 3D 场景渲染 │         │ - 房间管理        │         │ - AI 对话    │
│ - 角色图片显示 │         │ - 消息路由        │         │ - 状态控制   │
│ - 聊天 UI    │         │ - 状态同步        │         │ - Tool 调用  │
│ - 用户输入    │         │ - OpenClaw 适配层  │         │ - Memory    │
└─────────────┘         └──────────────────┘         └─────────────┘
```

## 数据流

### 用户发消息

```
Unity 用户输入 "你今天心情怎么样？"
  → Mirror Server 收到
  → Mirror Server 调用 OpenClaw Gateway API (POST /v1/chat)
  → OpenClaw 处理，AI 回复文字 + 状态更新
  → Mirror Server 收到响应
  → Mirror Server 广播给 Unity：
     - 文字消息（显示在聊天框）
     - 状态更新（切换角色图片/动画）
  → Unity 渲染
```

### AI 主动推送（心跳/场景变化）

```
OpenClaw 心跳触发
  → AI 决定更新状态（比如"我去倒杯水"）
  → 通过 Gateway API 或 Webhook 推送到 Mirror Server
  → Mirror Server 广播状态更新
  → Unity 角色切换到"倒水"图片/动画
```

## 角色状态系统

### 状态 Schema

```json
{
  "mood": "happy|sad|excited|thinking|shy|angry|sleepy|playful",
  "action": "standing|sitting|lying|walking|waving|drinking|reading|typing",
  "scene": "bedroom|living_room|cafe|park|office|kitchen",
  "outfit": "casual|pajama|dress|sportswear|formal",
  "accessory": "none|glasses|headphones|hat|cat_ears",
  "expression": "smile|laugh|pout|wink|blush|surprised|neutral",
  "time_of_day": "morning|afternoon|evening|night"
}
```

### 图片命名规则

```
{scene}_{action}_{mood}_{outfit}_{expression}.png

示例：
bedroom_sitting_happy_casual_smile.png
cafe_standing_excited_dress_laugh.png
kitchen_drinking_sleepy_pajama_neutral.png
```

### 图片数量估算

| 维度 | 取值数 |
|------|-------|
| scene | 6 |
| action | 8 |
| mood | 8 |
| outfit | 5 |
| expression | 7 |
| **全组合** | **13,440** |

实际不需要全组合，按常见场景生成 **200-500 张** 就够用了。
优先级：bedroom + 常见动作 + 常见心情 = ~50 张起步。

## 技术选型

### 角色创建
- **腾讯 Hunyuan3D 系列** — 从概念图到游戏角色一条龙
- 天然游戏风格友好，输出质量适合 Unity 直接用
- VRM 格式导出，配合 UniVRM 导入 Unity

### Mirror Server (C#)
- 运行在 Linux VPS 上
- 处理房间/玩家管理
- 作为 OpenClaw 的"适配层"，调用 Gateway REST API
- 维护每个房间的世界状态

### Unity Client (C#)
- 运行在手机/PC
- Mirror 网络同步
- 角色用 2D Sprite（预生成图片）或 Spine 动画
- 聊天 UI（输入框 + 消息列表）
- 3D 场景渲染

### OpenClaw 侧
- **不需要写新 channel plugin**
- Mirror Server 通过 Gateway REST API 交互
- 或者用 WebSocket 长连做实时推送
- AI 的 tool 能直接改 `workspace/world-state.json`

### 通信协议

#### Mirror → OpenClaw (HTTP)

```http
POST /v1/chat
Authorization: Bearer <gateway-token>
Content-Type: application/json

{
  "sessionKey": "virtual-world-room-1",
  "message": "你今天心情怎么样？",
  "context": {
    "userId": "wvkmind",
    "roomId": "room-1",
    "currentState": { "mood": "happy", "action": "sitting", ... }
  }
}
```

#### OpenClaw → Mirror (响应)

```json
{
  "reply": "心情超好的～ 今天天气不错，坐在窗边晒太阳特别舒服 ☀️",
  "stateUpdate": {
    "mood": "happy",
    "action": "sitting",
    "scene": "bedroom",
    "expression": "smile"
  },
  "image": "bedroom_sitting_happy_casual_smile.png"
}
```

## 开发阶段

### Phase 1: 验证 & 原型
- [ ] 设计状态 schema（本文档已完成）
- [ ] 用 AI 生成第一批图片（50 张起步）
- [ ] 写最简 HTTP 代理：Mirror Server → OpenClaw
- [ ] Unity 最简场景：显示图片 + 聊天框
- [ ] 验证端到端对话流程

### Phase 2: 世界丰富
- [ ] 更多场景（cafe, park, office）
- [ ] 更多服装/配饰
- [ ] 动画（Spine 或逐帧）
- [ ] AI 主动行为（心跳触发场景变化）
- [ ] 背景音乐/环境音

### Phase 3: 高级功能
- [ ] 多人同房间
- [ ] 用户自定义场景
- [ ] AI 记忆可视化（回忆气泡等）
- [ ] 语音对话（MiMo TTS 接入）
- [ ] 视频通话模式

## 文件结构

```
openclaw-virtual-world/
├── PRD.md                    # 本文档
├── server/                   # Mirror 服务器端
│   ├── OpenClawBridge.cs     # OpenClaw API 适配层
│   ├── WorldState.cs         # 世界状态管理
│   └── RoomManager.cs        # 房间管理
├── client/                   # Unity 客户端
│   ├── ChatUI.cs             # 聊天界面
│   ├── AvatarRenderer.cs     # 角色渲染
│   └── NetworkManager.cs     # Mirror 网络管理
├── assets/                   # 预生成图片
│   ├── bedroom/
│   ├── cafe/
│   └── ...
└── scripts/                  # 辅助脚本
    └── generate_avatars.py   # 批量生成角色图片
```

## 备注

- Mirror Server 调 OpenClaw 的方式跟 Discord Bot 调 API 本质上一样
- 区别在于 Discord 是 OpenClaw 内置 channel，Mirror 需要自己写适配层
- OpenClaw 的 `sessions_send` / Gateway REST API 都可以用来交互
- 未来如果做得好，可以把 Mirror 适配层封装成 OpenClaw 的 channel plugin
