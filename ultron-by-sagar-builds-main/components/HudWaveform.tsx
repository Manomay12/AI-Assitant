"use client";

import React, { useEffect, useRef } from "react";

interface Props {
  isActive: boolean;
  theme: string;
}

export default function HudWaveform({ isActive, theme }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;
    let phase = 0;

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const width = canvas.width;
      const height = canvas.height;
      const centerY = height / 2;

      ctx.lineWidth = 2;
      ctx.strokeStyle =
        theme === "ultron_gold"
          ? "rgba(255, 170, 48, 0.85)"
          : theme === "cyber_crimson"
          ? "rgba(255, 60, 60, 0.85)"
          : "rgba(0, 240, 255, 0.85)";

      ctx.beginPath();
      const bars = 36;
      const step = width / bars;

      for (let i = 0; i < bars; i++) {
        const x = i * step;
        const distFromCenter = Math.abs(i - bars / 2) / (bars / 2);
        const ampFactor = 1 - distFromCenter * 0.6;
        const amplitude = isActive
          ? Math.sin(phase + i * 0.4) * 20 * ampFactor + Math.sin(phase * 1.5 + i * 0.8) * 10
          : Math.sin(phase + i * 0.2) * 4 * ampFactor;

        ctx.moveTo(x, centerY - amplitude);
        ctx.lineTo(x, centerY + amplitude);
      }
      ctx.stroke();

      phase += isActive ? 0.15 : 0.04;
      animId = requestAnimationFrame(render);
    };

    render();
    return () => cancelAnimationFrame(animId);
  }, [isActive, theme]);

  return <canvas ref={canvasRef} width={400} height={60} className="hud-waveform" />;
}
