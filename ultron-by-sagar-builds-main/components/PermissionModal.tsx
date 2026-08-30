"use client";

import React from "react";
import { PermissionRequest } from "@/lib/jarvisSocket";

interface Props {
  request: PermissionRequest;
  onDecision: (requestId: string, decision: string) => void;
}

export default function PermissionModal({ request, onDecision }: Props) {
  return (
    <div className="permission-modal-overlay">
      <div className="permission-modal">
        <div className="modal-header">
          <div className="security-shield">⚠</div>
          <div className="modal-title">SECURITY ACCESS REQUIRED</div>
        </div>

        <div className="modal-body">
          <div className="scope-tag">SCOPE: {request.scope.toUpperCase()}</div>
          <p className="action-text">
            JARVIS requests permission to execute:
            <br />
            <strong>&quot;{request.action}&quot;</strong>
          </p>
          {request.target && <div className="target-badge">TARGET: {request.target}</div>}
        </div>

        <div className="modal-actions">
          <button
            className="hud-action-btn btn-allow-once"
            onClick={() => onDecision(request.request_id, "allow_once")}
          >
            ALLOW ONCE
          </button>
          <button
            className="hud-action-btn btn-allow-session"
            onClick={() => onDecision(request.request_id, "allow_session")}
          >
            ALLOW SESSION
          </button>
          <button
            className="hud-action-btn btn-always-allow"
            onClick={() => onDecision(request.request_id, "always_allow")}
          >
            ALWAYS ALLOW
          </button>
          <button
            className="hud-action-btn btn-deny"
            onClick={() => onDecision(request.request_id, "deny")}
          >
            DENY
          </button>
        </div>
      </div>
    </div>
  );
}
