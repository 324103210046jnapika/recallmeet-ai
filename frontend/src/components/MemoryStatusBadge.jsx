import React from "react";
import {
  Database,
  ShieldAlert,
  AlertTriangle,
} from "lucide-react";

export default function MemoryStatusBadge({
  provider,
  connected,
  className = "",
}) {
  if (
    provider === "hindsight" &&
    connected === true
  ) {
    return (
      <div
        className={`inline-flex items-center gap-2 rounded-full border border-emerald-500/25 bg-emerald-500/10 px-3 py-1.5 text-xs font-semibold text-emerald-400 ${className}`}
      >
        <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />

        <Database className="h-3.5 w-3.5" />

        <span>HINDSIGHT ACTIVE</span>
      </div>
    );
  }

  if (provider === "local_fallback") {
    return (
      <div
        className={`inline-flex items-center gap-2 rounded-full border border-amber-500/25 bg-amber-500/10 px-3 py-1.5 text-xs font-semibold text-amber-400 ${className}`}
      >
        <AlertTriangle className="h-3.5 w-3.5" />

        <span>DEVELOPMENT MEMORY</span>
      </div>
    );
  }

  return (
    <div
      className={`inline-flex items-center gap-2 rounded-full border border-rose-500/20 bg-rose-500/10 px-3 py-1.5 text-xs font-semibold text-rose-400 ${className}`}
    >
      <ShieldAlert className="h-3.5 w-3.5" />

      <span>MEMORY DISABLED</span>
    </div>
  );
}