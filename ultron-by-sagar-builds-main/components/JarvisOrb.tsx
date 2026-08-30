"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { createOrbScene, type OrbSceneApi } from "@/lib/orbScene";
import { HandTracker, type TrackerStatus } from "@/lib/handTracker";
import {
  JarvisSocketClient,
  type ChatMessage,
  type ExecutionPlan,
  type PermissionRequest,
  type SystemStatus,
} from "@/lib/jarvisSocket";
import HudStatusPanel from "./HudStatusPanel";
import HudTaskPanel from "./HudTaskPanel";
import HudWaveform from "./HudWaveform";
import HudInputBar from "./HudInputBar";
import PermissionModal from "./PermissionModal";

type CameraState = "off" | "starting" | "on" | "error";
type HudMode = "full" | "voice" | "text" | "focus";
type ThemeMode = "jarvis_cyan" | "ultron_gold" | "cyber_crimson";

const MODE_LABEL: Record<TrackerStatus["mode"], string> = {
  idle: "STANDBY",
  spin: "SPIN",
  zoom: "ZOOM",
};

export default function JarvisOrb() {
  const containerRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const overlayRef = useRef<HTMLCanvasElement>(null);
  const sceneRef = useRef<OrbSceneApi | null>(null);
  const trackerRef = useRef<HandTracker | null>(null);
  const socketRef = useRef<JarvisSocketClient | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);
  const alwaysListenRef = useRef<boolean>(false);

  const [camera, setCamera] = useState<CameraState>("off");
  const [status, setStatus] = useState<TrackerStatus>({ hands: 0, mode: "idle" });
  const [error, setError] = useState<string | null>(null);

  // Backend Integration State
  const [online, setOnline] = useState<boolean>(false);
  const [hudMode, setHudMode] = useState<HudMode>("full");
  const [theme, setTheme] = useState<ThemeMode>("ultron_gold");
  const [isListening, setIsListening] = useState<boolean>(false);
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);
  const [alwaysListen, setAlwaysListen] = useState<boolean>(false);

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "init",
      role: "assistant",
      text: "JARVIS 5.0 online. Real-time browser automation & AI Agent systems active. Ready for your command.",
      timestamp: "SYSTEM READY",
    },
  ]);

  const [activePlan, setActivePlan] = useState<ExecutionPlan | null>(null);
  const [permissionReq, setPermissionReq] = useState<PermissionRequest | null>(null);
  const [tools, setTools] = useState<any[]>([]);
  const [memories, setMemories] = useState<any[]>([]);
  const [permissions, setPermissions] = useState<Record<string, string>>({
    "app:launch": "always_allow",
    "browser:control": "always_allow",
    "screen:read": "always_allow",
    "internet:research": "always_allow",
    "comm:send": "always_allow",
  });

  const [telemetry, setTelemetry] = useState<SystemStatus>({
    cpu_percent: 14.5,
    ram_percent: 41.0,
    disk_percent: 54.0,
    battery: "AC Power",
    ai_provider: "NVIDIA NIM",
    active_tools_count: 12,
    online: false,
  });

  // Browser Speech Synthesis Function
  const speakInBrowser = useCallback((text: string) => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
    try {
      window.speechSynthesis.cancel();
      const cleanText = text.replace(/[*#]/g, "").trim();
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.rate = 1.05;
      utterance.pitch = 0.95;

      const voices = window.speechSynthesis.getVoices();
      const aiVoice = voices.find(
        (v) =>
          v.name.includes("David") ||
          v.name.includes("Google UK English Male") ||
          v.name.includes("Natural") ||
          (v.lang.startsWith("en") && v.name.includes("Male"))
      );
      if (aiVoice) utterance.voice = aiVoice;

      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);

      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn("SpeechSynthesis error:", e);
      setIsSpeaking(false);
    }
  }, []);

  // Safe deduplicating message adder
  const appendMessage = useCallback((msg: ChatMessage) => {
    setMessages((prev) => {
      // Deduplicate consecutive identical messages
      if (prev.length > 0) {
        const last = prev[prev.length - 1];
        if (last.role === msg.role && last.text === msg.text) {
          return prev;
        }
      }
      return [...prev, msg];
    });
  }, []);

  // Initialize Three.js 3D Orb Scene & WebSocket Client
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const scene = createOrbScene(container);
    sceneRef.current = scene;

    const socket = new JarvisSocketClient();
    socket.onStatusChange = (isOnline) => {
      setOnline(isOnline);
      setTelemetry((prev) => ({ ...prev, online: isOnline }));
    };

    socket.onMessageReceived = (msg) => {
      appendMessage(msg);
      if (msg.role === "assistant") {
        speakInBrowser(msg.text);
      }
    };

    socket.onPlanUpdate = (plan) => {
      setActivePlan(plan);
    };

    socket.onPermissionRequest = (req) => {
      setPermissionReq(req);
    };

    socket.onInitState = (data) => {
      if (data.tools) setTools(data.tools);
      if (data.memories) setMemories(data.memories);
      if (data.permissions) setPermissions(data.permissions);
    };

    socket.connect();
    socketRef.current = socket;

    return () => {
      trackerRef.current?.stop();
      trackerRef.current = null;
      scene.dispose();
      sceneRef.current = null;
      socket.disconnect();
      socketRef.current = null;
    };
  }, [speakInBrowser, appendMessage]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Dispatch message to agent with single user bubble
  const handleUserMessage = useCallback(
    async (text: string) => {
      const cleanText = text.trim();
      if (!cleanText) return;

      appendMessage({
        id: `u_${Date.now()}`,
        role: "user",
        text: cleanText,
        timestamp: new Date().toLocaleTimeString(),
      });

      const fallbackResponse = await socketRef.current?.sendMessage(cleanText);

      if (fallbackResponse === null && !socketRef.current?.isConnected()) {
        const offlineMsg =
          "⚠️ JARVIS Backend is currently offline. Please run 'python -m jarvis.main --mode server' in terminal.";
        appendMessage({
          id: `a_${Date.now()}`,
          role: "assistant",
          text: offlineMsg,
          timestamp: new Date().toLocaleTimeString(),
        });
        speakInBrowser(offlineMsg);
      }
    },
    [appendMessage, speakInBrowser]
  );

  // Web Speech Recognition Setup (Continuous & Always-Listening)
  const startSpeechRecognition = useCallback(() => {
    if (typeof window === "undefined") return;
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition is not supported in this browser. Please use Chrome or Edge.");
      return;
    }

    try {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }

      const recognition = new SpeechRecognition();
      recognition.lang = "en-IN";
      recognition.continuous = true;
      recognition.interimResults = false;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event: any) => {
        const results = event.results;
        if (results && results.length > 0) {
          const lastResult = results[results.length - 1];
          if (lastResult.isFinal) {
            const transcript = lastResult[0].transcript;
            if (transcript && transcript.trim()) {
              handleUserMessage(transcript);
            }
          }
        }
      };

      recognition.onerror = (event: any) => {
        if (event.error !== "no-speech") {
          console.warn("Speech recognition notice:", event.error);
        }
      };

      recognition.onend = () => {
        // Auto-reconnect if always-listening is enabled
        if (alwaysListenRef.current) {
          setTimeout(() => {
            if (alwaysListenRef.current) {
              try {
                recognition.start();
              } catch (e) {}
            }
          }, 300);
        } else {
          setIsListening(false);
        }
      };

      recognitionRef.current = recognition;
      recognition.start();
      setIsListening(true);
    } catch (e) {
      console.error("Speech recognition error:", e);
      setIsListening(false);
    }
  }, [handleUserMessage]);

  const toggleMic = useCallback(() => {
    if (isListening) {
      alwaysListenRef.current = false;
      setAlwaysListen(false);
      recognitionRef.current?.stop();
      setIsListening(false);
    } else {
      alwaysListenRef.current = true;
      setAlwaysListen(true);
      startSpeechRecognition();
    }
  }, [isListening, startSpeechRecognition]);

  const stopGestures = useCallback(() => {
    trackerRef.current?.stop();
    trackerRef.current = null;
    setCamera("off");
    setStatus({ hands: 0, mode: "idle" });
  }, []);

  const startGestures = useCallback(async () => {
    const video = videoRef.current;
    const overlay = overlayRef.current;
    if (!video || !overlay || trackerRef.current) return;

    setCamera("starting");
    setError(null);

    const tracker = new HandTracker(video, overlay, {
      onRotate: (dt, dp) => sceneRef.current?.rotateBy(dt, dp),
      onZoom: (factor) => sceneRef.current?.zoomBy(factor),
      onStatus: (st) => {
        setStatus(st);
        socketRef.current?.sendGesture(st.mode, st.hands);
      },
    });
    trackerRef.current = tracker;

    try {
      await tracker.start();
      setCamera("on");
    } catch (err) {
      trackerRef.current = null;
      tracker.stop();
      setCamera("error");
      setError(
        err instanceof DOMException && err.name === "NotAllowedError"
          ? "CAMERA ACCESS DENIED"
          : "TRACKING INIT FAILED"
      );
    }
  }, []);

  const toggleGestures = useCallback(() => {
    if (trackerRef.current) stopGestures();
    else void startGestures();
  }, [startGestures, stopGestures]);

  const handlePermissionDecision = (requestId: string, decision: string) => {
    socketRef.current?.respondPermission(requestId, decision);
    setPermissionReq(null);
  };

  const cameraOn = camera === "on";

  return (
    <div className={`jarvis-theme-root theme-${theme}`}>
      {/* 3D Three.js Holographic Orb */}
      <div ref={containerRef} className="orb-root" />

      {/* Cyber Overlays */}
      <div className="overlay-vignette" />
      <div className="overlay-grain" />
      <div className="overlay-scanlines" />

      {/* Header HUD Bar */}
      <div className="hud hud-title-bar">
        <div className="title-block">
          <div className="main-logo">J A R V I S</div>
          <div className="sub-logo">
            ULTRON HOLOGRAPHIC HUD v5.0 · {online ? "ONLINE" : "STANDBY"} {alwaysListen && "· 🟢 ALWAYS LISTENING"}
          </div>
        </div>

        <div className="mode-selector">
          <button
            className={`mode-btn ${hudMode === "full" ? "active" : ""}`}
            onClick={() => setHudMode("full")}
          >
            FULL HUD
          </button>
          <button
            className={`mode-btn ${hudMode === "voice" ? "active" : ""}`}
            onClick={() => {
              setHudMode("voice");
              if (!isListening) toggleMic();
            }}
          >
            VOICE MODE
          </button>
          <button
            className={`mode-btn ${hudMode === "focus" ? "active" : ""}`}
            onClick={() => setHudMode("focus")}
          >
            FOCUS
          </button>
        </div>

        <div className="theme-selector">
          <button
            className={`theme-dot cyan ${theme === "jarvis_cyan" ? "active" : ""}`}
            title="JARVIS Cyan"
            onClick={() => setTheme("jarvis_cyan")}
          />
          <button
            className={`theme-dot gold ${theme === "ultron_gold" ? "active" : ""}`}
            title="ULTRON Gold"
            onClick={() => setTheme("ultron_gold")}
          />
          <button
            className={`theme-dot crimson ${theme === "cyber_crimson" ? "active" : ""}`}
            title="Cyber Crimson"
            onClick={() => setTheme("cyber_crimson")}
          />
        </div>
      </div>

      {/* Left Status & Telemetry Panel */}
      {hudMode === "full" && (
        <HudStatusPanel
          status={telemetry}
          permissions={permissions}
          online={online}
          theme={theme}
        />
      )}

      {/* Right Task & Tools Panel */}
      {hudMode === "full" && (
        <HudTaskPanel plan={activePlan} tools={tools} memories={memories} />
      )}

      {/* Center Chat Transcript */}
      <div className={`hud-center-chat ${hudMode}`}>
        <div className="chat-messages">
          {messages.slice(-6).map((m) => (
            <div key={m.id} className={`chat-bubble ${m.role}`}>
              <div className="chat-meta">
                <span className="role-tag">{m.role.toUpperCase()}</span>
                <span className="time-tag">{m.timestamp}</span>
              </div>
              <div className="chat-text">{m.text}</div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        {/* Audio Reactive Waveform */}
        <div className="waveform-wrapper">
          <HudWaveform isActive={isListening || isSpeaking} theme={theme} />
        </div>
      </div>

      {/* Bottom Command & Interaction Deck (Zero-Lag Memoized Component) */}
      <HudInputBar
        onSendMessage={handleUserMessage}
        isListening={isListening}
        onToggleMic={toggleMic}
      />

      {/* MediaPipe Camera Gesture HUD Preview */}
      <div className="hud hud-controls">
        <div className={`camera-panel${cameraOn ? " visible" : ""}`}>
          <video ref={videoRef} muted playsInline className="camera-video" />
          <canvas ref={overlayRef} width={208} height={156} className="camera-overlay" />
          <div className="camera-status">
            {status.hands > 0
              ? `${status.hands} HAND${status.hands > 1 ? "S" : ""} · ${MODE_LABEL[status.mode]}`
              : "SHOW HANDS"}
          </div>
        </div>

        {error && <div className="hud-error">{error}</div>}

        <div className="hud-row">
          <button
            type="button"
            className="hud-btn"
            aria-pressed={cameraOn}
            onClick={toggleGestures}
            disabled={camera === "starting"}
          >
            {camera === "starting" ? "INITIALIZING…" : cameraOn ? "GESTURES ON" : "GESTURES OFF"}
          </button>
        </div>
      </div>

      {/* Interactive Permission Modal */}
      {permissionReq && (
        <PermissionModal request={permissionReq} onDecision={handlePermissionDecision} />
      )}
    </div>
  );
}
