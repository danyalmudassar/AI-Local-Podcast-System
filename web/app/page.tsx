'use client';

import React, { useState } from 'react';
import { Play, Loader2, Wand2, Mic2, Pause, Volume2, Save } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Home() {
    const [topic, setTopic] = useState('');
    const [length, setLength] = useState('short');
    const [isGenerating, setIsGenerating] = useState(false);
    const [status, setStatus] = useState(''); // e.g., "Researching", "Writing Script", "Recording"
    const [audioUrl, setAudioUrl] = useState<string | null>(null);
    const [scriptInput, setScriptInput] = useState('');
    const [mode, setMode] = useState<'agent' | 'manual'>('agent');
    const [hostName, setHostName] = useState('Anny');
    const [guestName, setGuestName] = useState('Dany Bhatti');
    const [models, setModels] = useState<string[]>([]);
    const [selectedModel, setSelectedModel] = useState('qwen2.5:0.5b');

    const API_URL = 'http://localhost:8000';

    // Fetch models on mount
    React.useEffect(() => {
        fetch(`${API_URL}/api/models`)
            .then(res => res.json())
            .then(data => {
                if (data.models && data.models.length > 0) {
                    setModels(data.models);
                    setSelectedModel(data.models[0]);
                }
            })
            .catch(err => console.error("Failed to fetch models", err));
    }, []);

    const handleGenerate = async () => {
        if (!topic && mode === 'agent') return;
        if (!scriptInput && mode === 'manual') return;

        setIsGenerating(true);
        setAudioUrl(null);
        setStatus('Initializing Agent...');

        try {
            let endpoint = mode === 'agent' ? '/api/generate' : '/api/manual';
            let body;

            if (mode === 'agent') {
                body = JSON.stringify({
                    topic,
                    length,
                    host_name: hostName,
                    guest_name: guestName,
                    model: selectedModel
                });
            } else {
                body = JSON.stringify({ script: scriptInput });
            }

            const res = await fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: body,
            });

            if (!res.ok) throw new Error('Generation start failed');

            const data = await res.json();

            // Handle Manual Mode (Sync)
            if (mode === 'manual') {
                setAudioUrl(`${API_URL}/api/audio/${data.filename}`);
                setStatus('Complete!');
                setIsGenerating(false);
                return;
            }

            // Handle Agent Mode (Async Polling)
            const jobId = data.jobId;
            setStatus('Request Queued...');

            const pollInterval = setInterval(async () => {
                try {
                    const statusRes = await fetch(`${API_URL}/api/status/${jobId}`);
                    const statusData = await statusRes.json();

                    if (statusData.status === 'completed') {
                        clearInterval(pollInterval);
                        setAudioUrl(`${API_URL}/api/audio/${statusData.filename}`);
                        setStatus('Complete!');
                        setIsGenerating(false);
                    } else if (statusData.status === 'failed') {
                        clearInterval(pollInterval);
                        setStatus(`Error: ${statusData.message}`);
                        setIsGenerating(false);
                    } else {
                        // Still processing
                        setStatus(`Processing: ${statusData.message || 'Working...'}`);
                    }
                } catch (e) {
                    console.error("Polling error", e);
                    clearInterval(pollInterval);
                    setStatus('Polling failed');
                    setIsGenerating(false);
                }
            }, 2000);

        } catch (e) {
            console.error(e);
            setStatus('Error occurred starting generation.');
            setIsGenerating(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 text-white font-sans selection:bg-purple-500/30">
            <div className="fixed inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none"></div>

            {/* Background Gradient Orbs */}
            <div className="fixed top-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px] pointer-events-none" />
            <div className="fixed bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px] pointer-events-none" />

            <main className="relative z-10 container mx-auto px-6 py-12 max-w-4xl">
                <header className="mb-12 text-center">
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-purple-300 mb-6"
                    >
                        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                        System Online v2.0
                    </motion.div>
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="text-5xl md:text-7xl font-bold tracking-tight bg-gradient-to-b from-white to-white/50 bg-clip-text text-transparent mb-4"
                    >
                        AI Podcast Agent
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.2 }}
                        className="text-lg text-slate-400 max-w-xl mx-auto"
                    >
                        Turn any topic into a professional, multi-speaker podcast episode instantly. Powered by local LLMs and neural speech synthesis.
                    </motion.p>
                </header>

                {/* Control Panel */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.3 }}
                    className="group relative bg-slate-900/50 backdrop-blur-xl border border-white/10 rounded-3xl p-1 shadow-2xl"
                >
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-1000" />

                    <div className="relative bg-slate-950/80 rounded-2xl p-6 md:p-8">
                        {/* Mode Switcher */}
                        <div className="flex gap-4 mb-8">
                            <button
                                onClick={() => setMode('agent')}
                                className={`flex-1 py-3 px-4 rounded-xl text-sm font-medium transition-all duration-300 flex items-center justify-center gap-2
                        ${mode === 'agent'
                                        ? 'bg-purple-600/20 text-purple-300 border border-purple-500/30 shadow-[0_0_20px_-5px_rgba(147,51,234,0.3)]'
                                        : 'bg-slate-900 text-slate-500 border border-transparent hover:bg-slate-900/80 hover:text-slate-400'}`}
                            >
                                <Wand2 className="w-4 h-4" />
                                Agent Mode
                            </button>
                            <button
                                onClick={() => setMode('manual')}
                                className={`flex-1 py-3 px-4 rounded-xl text-sm font-medium transition-all duration-300 flex items-center justify-center gap-2
                        ${mode === 'manual'
                                        ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30 shadow-[0_0_20px_-5px_rgba(37,99,235,0.3)]'
                                        : 'bg-slate-900 text-slate-500 border border-transparent hover:bg-slate-900/80 hover:text-slate-400'}`}
                            >
                                <Mic2 className="w-4 h-4" />
                                Script Mode
                            </button>
                        </div>

                        {/* Input Area */}
                        <div className="space-y-6">
                            <AnimatePresence mode="wait">
                                {mode === 'agent' ? (
                                    <motion.div
                                        key="agent-inputs"
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: 20 }}
                                        className="space-y-6"
                                    >
                                        <div>
                                            <label className="block text-sm font-medium text-slate-400 mb-2 ml-1">Topic</label>
                                            <input
                                                type="text"
                                                placeholder="e.g., The Future of Space Colonization"
                                                value={topic}
                                                onChange={(e) => setTopic(e.target.value)}
                                                className="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-4 text-lg focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all placeholder:text-slate-700"
                                            />
                                        </div>
                                        <div className="grid grid-cols-2 gap-4">
                                            <div>
                                                <label className="block text-sm font-medium text-slate-400 mb-2 ml-1">Host Name</label>
                                                <input
                                                    type="text"
                                                    value={hostName}
                                                    onChange={(e) => setHostName(e.target.value)}
                                                    className="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all text-white"
                                                />
                                            </div>
                                            <div>
                                                <label className="block text-sm font-medium text-slate-400 mb-2 ml-1">Guest Name</label>
                                                <input
                                                    type="text"
                                                    value={guestName}
                                                    onChange={(e) => setGuestName(e.target.value)}
                                                    className="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all text-white"
                                                />
                                            </div>
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-slate-400 mb-2 ml-1">AI Model</label>
                                            <select
                                                value={selectedModel}
                                                onChange={(e) => setSelectedModel(e.target.value)}
                                                className="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all text-white appearance-none"
                                            >
                                                {models.map(m => (
                                                    <option key={m} value={m}>{m}</option>
                                                ))}
                                            </select>
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-slate-400 mb-2 ml-1">Length</label>
                                            <div className="grid grid-cols-3 gap-3">
                                                {['short', 'medium', 'long'].map((l) => (
                                                    <button
                                                        key={l}
                                                        onClick={() => setLength(l)}
                                                        className={`py-2 px-4 rounded-lg text-sm font-medium capitalize border transition-all
                                                ${length === l
                                                                ? 'bg-white/10 border-white/20 text-white'
                                                                : 'bg-transparent border-white/5 text-slate-500 hover:bg-white/5'}`}
                                                    >
                                                        {l}
                                                    </button>
                                                ))}
                                            </div>
                                        </div>
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        key="manual-inputs"
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: 20 }}
                                    >
                                        <label className="block text-sm font-medium text-slate-400 mb-2 ml-1">Script</label>
                                        <textarea
                                            placeholder="Host: Hello world!&#10;Guest: Hi there."
                                            value={scriptInput}
                                            onChange={(e) => setScriptInput(e.target.value)}
                                            className="w-full h-40 bg-slate-900 border border-white/10 rounded-xl px-4 py-4 text-base focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all placeholder:text-slate-700 resize-none font-mono"
                                        />
                                    </motion.div>
                                )}
                            </AnimatePresence>

                            {/* Generate Button */}
                            <button
                                onClick={handleGenerate}
                                disabled={isGenerating}
                                className="w-full relative overflow-hidden group bg-white text-black font-bold text-lg py-4 rounded-xl transition-all hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 disabled:pointer-events-none"
                            >
                                <div className="absolute inset-0 bg-gradient-to-r from-purple-400 via-blue-400 to-purple-400 opacity-0 group-hover:opacity-20 transition-opacity duration-300" />
                                <span className="flex items-center justify-center gap-2">
                                    {isGenerating ? (
                                        <>
                                            <Loader2 className="w-5 h-5 animate-spin" />
                                            {status}
                                        </>
                                    ) : (
                                        <>
                                            <Play className="w-5 h-5 fill-current" />
                                            Generate Episode
                                        </>
                                    )}
                                </span>
                            </button>
                        </div>
                    </div>
                </motion.div>

                {/* Audio Player */}
                <AnimatePresence>
                    {audioUrl && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 20 }}
                            className="mt-8 p-1 rounded-3xl bg-gradient-to-br from-green-500/20 to-blue-500/20 backdrop-blur-md border border-white/10"
                        >
                            <div className="bg-slate-950/80 rounded-2xl p-6 flex items-center gap-6">
                                <div className="w-12 h-12 rounded-full bg-green-500 flex items-center justify-center text-slate-950">
                                    <Volume2 className="w-6 h-6" />
                                </div>
                                <div className="flex-1">
                                    <h3 className="text-lg font-semibold text-white mb-1">Generated Podcast</h3>
                                    <p className="text-sm text-green-400">Ready to play</p>
                                </div>
                                <audio controls src={audioUrl} className="w-full max-w-md h-10 accent-green-500" />
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>
        </div>
    );
}
