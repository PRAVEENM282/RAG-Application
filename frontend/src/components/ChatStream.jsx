import React, { useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const ChatStream = ({ messages, isStreaming }) => {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    return (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg, idx) => (
                <div 
                    key={idx} 
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} message-enter`}
                >
                    <div 
                        className={`max-w-[80%] rounded-2xl px-6 py-4 ${
                            msg.role === 'user' 
                                ? 'bg-blue-600 text-white' 
                                : 'bg-slate-800 text-slate-100 border border-slate-700'
                        }`}
                        style={{
                            background: msg.role === 'user' ? 'var(--accent-primary)' : 'var(--bg-secondary)',
                        }}
                    >
                        <ReactMarkdown className="prose prose-invert max-w-none text-sm leading-relaxed">
                            {msg.content}
                        </ReactMarkdown>
                    </div>
                </div>
            ))}
            {isStreaming && (
                <div className="flex justify-start animate-pulse">
                     <div className="h-2 w-2 bg-blue-400 rounded-full mx-1"></div>
                     <div className="h-2 w-2 bg-blue-400 rounded-full mx-1 animation-delay-200"></div>
                     <div className="h-2 w-2 bg-blue-400 rounded-full mx-1 animation-delay-400"></div>
                </div>
            )}
            <div ref={bottomRef} />
        </div>
    );
}

export default ChatStream;
