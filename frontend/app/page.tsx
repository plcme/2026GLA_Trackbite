"use client";

import { useState } from "react";
import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

type ConnectionState = "idle" | "loading" | "success" | "error";

export default function Home() {
  const [prompt, setPrompt] = useState("Say hello from Gemini and tell me what TrackBite can do for me.");
  const [state, setState] = useState<ConnectionState>("idle");
  const [geminiResponse, setGeminiResponse] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  async function handleTest() {
    setState("loading");
    setGeminiResponse("");
    setErrorMessage("");

    try {
      const { data } = await axios.post<{ response: string }>(
        `${API_URL}/gemini-test`,
        { prompt }
      );
      setGeminiResponse(data.response);
      setState("success");
    } catch (err: unknown) {
      const msg =
        axios.isAxiosError(err)
          ? (err.response?.data?.detail ?? err.message)
          : "Unexpected error";
      setErrorMessage(String(msg));
      setState("error");
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950 flex items-center justify-center p-6">
      <div className="w-full max-w-2xl space-y-6">

        {/* Header */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-3">
            <span className="text-4xl">🥦</span>
            <h1 className="text-4xl font-bold text-white tracking-tight">TrackBite</h1>
          </div>
          <p className="text-slate-400 text-sm">AI-powered food tracking · Powered by Gemini</p>
        </div>

        {/* Connection card */}
        <div className="bg-slate-800/60 backdrop-blur border border-slate-700 rounded-2xl p-6 space-y-4">

          <label className="block text-sm font-medium text-slate-300">
            Test Prompt
          </label>
          <textarea
            className="w-full rounded-xl bg-slate-900 border border-slate-600 text-slate-100 placeholder-slate-500
                       px-4 py-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-emerald-500
                       transition"
            rows={3}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />

          <button
            onClick={handleTest}
            disabled={state === "loading" || !prompt.trim()}
            className="w-full py-3 rounded-xl font-semibold text-sm transition
                       bg-emerald-500 hover:bg-emerald-400 text-white
                       disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {state === "loading" ? "Connecting to Gemini..." : "Test Connection"}
          </button>

          {/* Status */}
          {state === "loading" && (
            <div className="flex items-center gap-2 text-slate-400 text-sm">
              <span className="animate-spin inline-block w-4 h-4 border-2 border-slate-400 border-t-emerald-400 rounded-full" />
              Calling Gemini via Vertex AI...
            </div>
          )}

          {state === "success" && (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <span className="text-emerald-400 text-xl">✓</span>
                <span className="text-emerald-400 font-semibold">Gemini Connected</span>
              </div>
              <div className="bg-slate-900 border border-slate-700 rounded-xl p-4 text-slate-200 text-sm leading-relaxed whitespace-pre-wrap">
                {geminiResponse}
              </div>
            </div>
          )}

          {state === "error" && (
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-red-400 text-xl">✗</span>
                <span className="text-red-400 font-semibold">Connection Failed</span>
              </div>
              <div className="bg-red-950/40 border border-red-800 rounded-xl p-3 text-red-300 text-xs font-mono">
                {errorMessage}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <p className="text-center text-slate-600 text-xs">
          Backend: <span className="font-mono">{API_URL}</span>
        </p>
      </div>
    </main>
  );
}
