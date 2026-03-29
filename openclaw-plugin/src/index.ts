/**
 * OpenClaw Virtual World Plugin
 * 
 * - registerService: WS client to World Server (chat relay, like Discord Bot)
 * - registerTool: world_action (HTTP, for heartbeat/cron state updates)
 * - registerTool: world_state (HTTP, read current state)
 */
import WebSocket from "ws";

const WORLD_SERVER_URL = process.env.WORLD_SERVER_URL || "http://localhost:8080";
const WORLD_WS_URL = process.env.WORLD_WS_URL || "ws://localhost:8080/ws/openclaw";

let ws: WebSocket | null = null;
let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

// Pending message handler - set by the plugin when AI processes a message
let pendingMessageHandler: ((message: string, state: any) => Promise<void>) | null = null;

export default {
  async onLoad(api: any) {
    // ============================================================
    // Service: WebSocket client to World Server (chat relay)
    // ============================================================
    api.registerService({
      name: "world-ws-client",

      async start() {
        connectWS(api);
      },

      async stop() {
        if (reconnectTimer) clearTimeout(reconnectTimer);
        if (ws) ws.close();
      },
    });

    // ============================================================
    // Tool: world_action (HTTP POST - for heartbeat/cron)
    // ============================================================
    api.registerTool({
      name: "world_action",
      description: `更新小爱在虚拟世界中的状态。心跳和定时任务时使用。
可用的值见 WORLD_API.md。关键规则：
- scene: living_room/bedroom/kitchen/bathroom/balcony
- action 必须和 scene 匹配
- action 必须和 time_of_day 匹配
- expression: smile/laugh/neutral/shy/sleepy/focused/excited/pout/sad/angry
- outfit: H01-H10(在家), O01-O10(外出)
- time_of_day: day/night (根据真实时间设置)`,
      parameters: {
        type: "object",
        properties: {
          scene: { type: "string", description: "房间" },
          action: { type: "string", description: "动作" },
          expression: { type: "string", description: "表情" },
          time_of_day: { type: "string", description: "day 或 night" },
          outfit: { type: "string", description: "服装ID" },
          message: { type: "string", description: "显示在聊天框的文字（可选）" },
        },
      },
      async execute(_id: string, params: any) {
        const { message, ...stateUpdate } = params;
        const body: any = { state_update: stateUpdate };
        if (message) body.message = message;

        try {
          const resp = await fetch(`${WORLD_SERVER_URL}/api/action`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
          });
          const result = await resp.json();
          return { content: [{ type: "text", text: JSON.stringify(result) }] };
        } catch (e: any) {
          return { content: [{ type: "text", text: `Error: ${e.message}` }] };
        }
      },
    });

    // ============================================================
    // Tool: world_state (HTTP GET - read current state)
    // ============================================================
    api.registerTool({
      name: "world_state",
      description: "获取小爱当前在虚拟世界中的状态（在哪个房间、做什么、穿什么、什么时间）",
      parameters: { type: "object", properties: {} },
      async execute() {
        try {
          const resp = await fetch(`${WORLD_SERVER_URL}/api/state`);
          const state = await resp.json();
          return { content: [{ type: "text", text: JSON.stringify(state) }] };
        } catch (e: any) {
          return { content: [{ type: "text", text: `Error: ${e.message}` }] };
        }
      },
    });
  },
};

// ============================================================
// WebSocket connection (Discord Bot pattern)
// ============================================================

function connectWS(api: any) {
  console.log(`[virtual-world] Connecting to ${WORLD_WS_URL}...`);

  ws = new WebSocket(WORLD_WS_URL);

  ws.on("open", () => {
    console.log("[virtual-world] Connected to World Server.");
  });

  ws.on("message", async (raw: Buffer) => {
    try {
      const data = JSON.parse(raw.toString());

      if (data.type === "user_message") {
        // User sent a message via App → process with AI
        const message = data.message || "";
        const worldState = data.state || {};

        console.log(`[virtual-world] User: ${message}`);

        // Send to OpenClaw's agent for processing
        // The agent will reply via the channel adapter
        try {
          const result = await api.sendMessage({
            channel: "virtual-world",
            message: message,
            context: {
              worldState: JSON.stringify(worldState),
              instruction: "用户通过虚拟世界App发来消息。回复后如需更新状态，请同时调用 world_action tool。",
            },
          });

          // Send AI reply back through WS
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
              type: "ai_response",
              reply: result.text || result.content || "",
              state_update: result.stateUpdate || null,
            }));
          }
        } catch (e: any) {
          console.error(`[virtual-world] AI error: ${e.message}`);
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
              type: "ai_response",
              reply: "啊...我刚走神了，你说什么？",
            }));
          }
        }
      } else if (data.type === "state_sync") {
        console.log(`[virtual-world] State synced: ${data.state?.scene}`);
      }
    } catch (e: any) {
      console.error(`[virtual-world] Parse error: ${e.message}`);
    }
  });

  ws.on("close", () => {
    console.log("[virtual-world] Disconnected. Reconnecting in 5s...");
    ws = null;
    reconnectTimer = setTimeout(() => connectWS(api), 5000);
  });

  ws.on("error", (err: Error) => {
    console.error(`[virtual-world] WS error: ${err.message}`);
    ws?.close();
  });
}
