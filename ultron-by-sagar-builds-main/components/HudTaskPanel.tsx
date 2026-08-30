"use client";

import React, { useState } from "react";
import { ExecutionPlan } from "@/lib/jarvisSocket";

interface Props {
  plan: ExecutionPlan | null;
  tools: any[];
  memories: any[];
}

export default function HudTaskPanel({ plan, tools, memories }: Props) {
  const [tab, setTab] = useState<"tasks" | "tools" | "memory">("tasks");

  return (
    <div className="hud-panel hud-right-panel">
      <div className="tab-header">
        <button
          className={`tab-btn ${tab === "tasks" ? "active" : ""}`}
          onClick={() => setTab("tasks")}
        >
          TASKS {plan ? "●" : ""}
        </button>
        <button
          className={`tab-btn ${tab === "tools" ? "active" : ""}`}
          onClick={() => setTab("tools")}
        >
          TOOLS ({tools.length})
        </button>
        <button
          className={`tab-btn ${tab === "memory" ? "active" : ""}`}
          onClick={() => setTab("memory")}
        >
          MEMORY
        </button>
      </div>

      <div className="tab-content">
        {tab === "tasks" && (
          <div className="tasks-container">
            {plan ? (
              <div className="active-plan">
                <div className="plan-goal">
                  <span className="goal-label">CURRENT GOAL:</span>
                  <p>{plan.goal}</p>
                </div>
                <div className="plan-steps">
                  {plan.steps.map((s, idx) => (
                    <div key={s.id} className={`step-item ${s.status}`}>
                      <div className="step-icon">
                        {s.status === "completed" ? "✓" : s.status === "in_progress" ? "◐" : "○"}
                      </div>
                      <div className="step-details">
                        <div className="step-title">{s.title}</div>
                        <div className="step-tool">{s.tool_name}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="empty-state">
                <div className="empty-icon">◎</div>
                <div>SYSTEM READY</div>
                <div className="sub">Awaiting multi-step instruction</div>
              </div>
            )}
          </div>
        )}

        {tab === "tools" && (
          <div className="tools-list">
            {tools.map((t) => (
              <div key={t.name} className="tool-card">
                <div className="tool-name">{t.name}</div>
                <div className="tool-desc">{t.description}</div>
              </div>
            ))}
          </div>
        )}

        {tab === "memory" && (
          <div className="memory-list">
            {memories.length > 0 ? (
              memories.map((m, idx) => (
                <div key={m.id || idx} className="memory-card">
                  <div className="memory-num">#{idx + 1}</div>
                  <div className="memory-text">{m.text || m}</div>
                </div>
              ))
            ) : (
              <div className="empty-state">
                <div>NO SAVED MEMORIES</div>
                <div className="sub">Say &quot;Remember [detail]&quot; to store</div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
