# OpenClaw Virtual World - PRD

## 概述

构建一个 Flutter 安卓 App，用户可以在其中与 AI 角色（小爱）实时对话和互动。
AI 通过 OpenClaw 控制虚拟角色的状态，预生成 2D 立绘作为角色表现层，Sprite 切换表现不同状态。

## 核心目标

- 用户在手机上与 AI 角色面对面交流
- 2D 房间背景 + 角色立绘叠加显示
- AI 返回状态码 → 切换角色立绘（表情、动作）
- 对话走 OpenClaw，复用现有的 memory/persona/tool 体系

## 架构

```
┌──────────────┐              ┌──────────────┐              ┌──────────────┐
│  Flutter App  │◄───HTTP/WS──►│ World Server  │◄───WS────────│  OpenClaw     │
│  (安卓/iOS)   │              │ (公网 VPS)    │  (主动连入)   │  (内网)       │
│              │              │              │              │              │
│ - 2D 场景渲染 │              │ - 世界状态管理 │              │ - AI 对话     │
│ - 立绘切换    │              │ - 消息转发    │              │ - 状态控制    │
│ - 聊天 UI    │              │ - 用户认证    │              │ - Tool 调用   │
│ - 用户输入    │              │ - 状态持久化  │              │ - Memory     │
└──────────────┘              └──────────────┘              └──────────────┘
```

### 架构要点

- World Server 部署在公网 VPS，同时服务 Flutter App 和 OpenClaw
- OpenClaw 在内网运行，主动 WebSocket 连接到 World Server（不暴露公网端口）
- Flutter App 通过 HTTP/WebSocket 连接 World Server
- World Server 是消息中枢 + 世界状态管理器

## 数据流

### 用户发消息

```
用户输入 "你今天心情怎么样？"
  → Flutter App 调用 OpenClaw Gateway API (POST /v1/chat)
  → OpenClaw 处理，AI 回复文字 + 状态更新
  → Flutter App 收到响应：
     - 文字消息（显示在聊天框）
     - 状态更新（切换角色立绘）
  → 渲染
```

## 角色状态系统

### 状态 Schema

```json
{
  "mood": "happy|sad|excited|thinking|shy|angry|sleepy|playful",
  "action": "standing|sitting|lying|waving|drinking|reading|typing",
  "expression": "smile|laugh|pout|wink|blush|surprised|neutral",
  "scene": "bedroom|living_room|kitchen|balcony",
  "time_of_day": "morning|afternoon|evening|night"
}
```

### 立绘命名规则

```
{action}_{expression}.png

示例：
standing_smile.png
sitting_laugh.png
reading_neutral.png
```

### 图片制作流程

#### 方式 A：静态立绘
1. AI 生成角色立绘（白色/纯色背景，全身，居中）
2. 抠图去背景（保留透明通道 PNG）
3. 裁剪到统一尺寸
4. 按状态命名，放入 assets/sprites/character/

#### 方式 B：帧动画（推荐）
1. ComfyUI 生成角色短视频（如"微笑"、"挥手"、"打字"）
2. 从视频抽帧（8-12 fps）
3. 每帧去背景（rembg 等工具）
4. 输出 PNG 序列
5. App 里循环播放帧序列，实现自然动画效果

帧动画比静态切换自然很多，且不需要 Spine/Live2D 的骨骼绑定。

### Phase 1 起步图片（~15 张）

- standing_smile, standing_neutral, standing_laugh
- sitting_smile, sitting_neutral
- typing_focused
- reading_neutral
- waving_smile
- drinking_smile
- lying_sleepy
- standing_shy, standing_angry, standing_sad, standing_surprised

## 场景系统（2D 背景）

每个房间一张背景图，角色立绘叠在上方。

| 场景 | 文件名 | 描述 |
|------|--------|------|
| 客厅 | bg_living_room.png | 沙发、电视、书桌 |
| 卧室 | bg_bedroom.png | 床、衣柜、梳妆台 |
| 厨房 | bg_kitchen.png | 灶台、冰箱 |
| 阳台 | bg_balcony.png | 花架、远景 |

### 时间/光照

通过叠加半透明色层：
- 早晨：暖黄 10%
- 下午：无叠加
- 傍晚：橙色 15%
- 夜晚：深蓝 30%

## 技术选型

### Flutter App
- Dart / Flutter
- 图片叠加：Stack + Image widget
- 聊天 UI：ListView + TextField
- 网络：http / web_socket_channel
- 状态管理：Provider 或 Riverpod

### OpenClaw 侧
- Gateway REST API（POST /v1/chat）
- AI 输出状态码驱动立绘切换

### 通信协议

#### App → OpenClaw (HTTP)

```http
POST /v1/chat
Authorization: Bearer <gateway-token>
Content-Type: application/json

{
  "sessionKey": "xiaoai-room-1",
  "message": "你今天心情怎么样？",
  "context": {
    "currentState": { "action": "standing", "expression": "smile", "scene": "living_room" }
  }
}
```

#### OpenClaw → App (响应)

```json
{
  "reply": "心情超好的～ 坐在窗边晒太阳特别舒服 ☀️",
  "stateUpdate": {
    "action": "sitting",
    "expression": "smile",
    "scene": "living_room"
  }
}
```

## 开发阶段

### Phase 1: 验证 & 原型
- [x] 设计状态 schema
- [ ] AI 生成第一批角色立绘（~15 张）
- [ ] 抠图处理
- [ ] Flutter 项目搭建
- [ ] 2D 场景：背景 + 角色立绘 + 聊天框
- [ ] 立绘切换控制器
- [ ] 对接 OpenClaw Gateway API
- [ ] 打包 APK 测试

### Phase 2: 丰富内容
- [ ] 更多场景背景
- [ ] 更多角色状态立绘
- [ ] 时间/光照系统
- [ ] 背景音乐/环境音
- [ ] AI 主动推送（WebSocket 长连接）

### Phase 3: 高级功能
- [ ] 语音对话（TTS 接入）
- [ ] Spine/Live2D 升级角色动画
- [ ] AI 记忆可视化
- [ ] iOS 版本

## 文件结构

```
xiaoai_app/
├── docs/
│   ├── PRD.md
│   └── world-design.md
├── lib/
│   ├── main.dart
│   ├── models/
│   │   └── character_state.dart
│   ├── services/
│   │   └── openclaw_service.dart
│   ├── widgets/
│   │   ├── scene_view.dart          # 背景 + 角色立绘
│   │   ├── character_sprite.dart    # 立绘切换
│   │   └── chat_panel.dart          # 聊天界面
│   └── screens/
│       └── home_screen.dart
├── assets/
│   ├── sprites/
│   │   └── character/               # 角色立绘（抠图后 PNG）
│   └── backgrounds/                  # 场景背景
├── pubspec.yaml
└── android/
```
