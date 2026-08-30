"use client";

import dynamic from "next/dynamic";

const JarvisOrb = dynamic(() => import("@/components/JarvisOrb"), {
  ssr: false,
  loading: () => (
    <div
      style={{
        display: "flex",
        height: "100vh",
        alignItems: "center",
        justifyContent: "center",
        background: "#020408",
        color: "#ffaa30",
        fontFamily: "'Orbitron', sans-serif",
        letterSpacing: "0.2em",
        fontSize: "14px",
      }}
    >
      INITIALIZING HOLOGRAPHIC CORE...
    </div>
  ),
});

export default function Home() {
  return <JarvisOrb />;
}
