import React, { useState, useEffect, useCallback } from 'react';
import { WebSocketService } from './services/websocket';
import ChatStream from './components/ChatStream';
import UploadPanel from './components/UploadPanel';
import CitationPanel from './components/CitationPanel';
import Login from './components/Login';
import { Send, Cpu, LogOut } from 'lucide-react';

function App() {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [citations, setCitations] = useState([]);
    const [isStreaming, setIsStreaming] = useState(false);
    const [wsService] = useState(() => new WebSocketService("ws://localhost:8000/ws/chat"));

    useEffect(() => {
        if (!token) return;

        wsService.connect(token, {
            onToken: (token) => {
                setMessages(prev => {
                    const newMsgs = [...prev];
                    const lastMsg = newMsgs[newMsgs.length - 1];
                    if (lastMsg && lastMsg.role === 'assistant') {
                        lastMsg.content += token;
                        return newMsgs;
                    } else {
                        return [...newMsgs, { role: 'assistant', content: token }];
                    }
                });
            },
            onCitation: (citation) => {
                setCitations(prev => [...prev, citation]);
            },
            onDone: () => {
                setIsStreaming(false);
            },
            onError: (err) => {
                console.error(err);
                setIsStreaming(false);
                setMessages(prev => [...prev, { role: 'assistant', content: `\n\n**Error:** ${err}` }]);
            }
        });
        
        return () => wsService.disconnect();
    }, [wsService, token]);

    const handleLogout = () => {
        setToken(null);
        localStorage.removeItem('token');
        wsService.disconnect();
    };

    if (!token) {
        return <Login onLogin={setToken} />;
    }


    const handleSubmit = (e) => {
        e.preventDefault();
        if (!input.trim() || isStreaming) return;

        // Reset citations for new query
        setCitations([]);
        
        // Add user message
        setMessages(prev => [...prev, { role: 'user', content: input }]);
        
        // Send to WS
        wsService.sendMessage(input);
        
        // Prepare UI
        setInput("");
        setIsStreaming(true);
        
        // Add placeholder for assistant response if not exists (optional, onToken handles it)
        setMessages(prev => [...prev, { role: 'assistant', content: "" }]);
    };

    return (
        <div className="flex h-screen overflow-hidden">
            {/* Sidebar */}
            <div className="w-80 bg-slate-900 border-r border-slate-800 p-6 flex flex-col">
                <div className="mb-8 flex flex-col gap-4">
                    <div className="flex items-center gap-3 text-blue-500">
                        <Cpu size={32} />
                        <h1 className="text-xl font-bold tracking-tight text-white">RAG Engine</h1>
                    </div>
                    <button onClick={handleLogout} className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors">
                        <LogOut size={16} />
                        Logout
                    </button>
                </div>

                <UploadPanel />
                
                <div className="flex-1 overflow-hidden mt-4">
                    <CitationPanel citations={citations} />
                </div>
            </div>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col min-w-0 bg-slate-950/50">
                <ChatStream messages={messages} isStreaming={isStreaming} />

                {/* Input Area */}
                <div className="p-6 border-t border-slate-800 bg-slate-900/50 backdrop-blur-sm">
                    <form onSubmit={handleSubmit} className="relative max-w-4xl mx-auto">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask me anything about your documents..."
                            className="w-full bg-slate-800 text-white placeholder-slate-400 rounded-xl pl-6 pr-14 py-4 focus:outline-none focus:ring-2 focus:ring-blue-500/50 border border-slate-700 shadow-xl"
                            disabled={isStreaming}
                        />
                        <button 
                            type="submit"
                            disabled={!input.trim() || isStreaming}
                            className="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                        >
                            <Send size={20} />
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default App;
