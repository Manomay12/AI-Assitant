"use client";

import React from "react";
import { SystemStatus } from "@/lib/jarvisSocket";

interface Props {
  status: SystemStatus;
  permissions: Record<string, string>;
  online: boolean;
  theme: string;
}

export default function HudStatusPanel({ status, permissions, online, theme }: Props) {
  return (
    <div className="hud-panel hud-left-panel">
      <div className="panel-header">
        <span className="panel-tag">SYSTEM TELEMETRY</span>
        <span className={`status-pill ${online ? "online" : "offline"}`}>
          {online ? "CONNECTED" : "STANDBY"}
        </span>
      </div>

      <div className="telemetry-grid">
        <div className="telemetry-card">
          <div className="telemetry-label">CPU CORE</div>
          <div className="telemetry-value">{status.cpu_percent.toFixed(1)}%</div>
          <div className="gauge-bar">
            <div className="gauge-fill" style={{ width: `${Math.min(status.cpu_percent, 100)}%` }} />
          </div>
        </div>

        <div className="telemetry-card">
          <div className="telemetry-label">MEMORY RAM</div>
          <div className="telemetry-value">{status.ram_percent.toFixed(1)}%</div>
          <div className="gauge-bar">
            <div className="gauge-fill" style={{ width: `${Math.min(status.ram_percent, 100)}%` }} />
          </div>
        </div>
      </div>

      <div className="status-rows">
        <div className="status-row">
          <span>AI PROVIDER</span>
          <span className="highlight-val">{status.ai_provider?.toUpperCase() || "NVIDIA NIM"}</span>
        </div>
        <div className="status-row">
          <span>ACTIVE TOOLS</span>
          <span className="highlight-val">{status.active_tools_count || 12} REGISTERED</span>
        </div>
        <div className="status-row">
          <span>POWER / BATTERY</span>
          <span className="highlight-val">{status.battery || "AC POWER"}</span>
        </div>
      </div>

      <div className="panel-divider" />

      <div className="panel-header">
        <span className="panel-tag">SECURITY & PERMISSIONS</span>
      </div>

      <div className="permissions-list">
        {Object.entries(permissions || {}).slice(0, 5).map(([scope, level]) => (
          <div key={scope} className="permission-item">
            <span className="perm-scope">{scope.replace(":", " → ")}</span>
            <span className={`perm-badge ${level}`}>{level.toUpperCase()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
