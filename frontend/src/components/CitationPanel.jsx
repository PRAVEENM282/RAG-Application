import React from 'react';
import { BookOpen } from 'lucide-react';

const CitationPanel = ({ citations }) => {
    if (!citations || citations.length === 0) return null;

    return (
        <div className="card h-full overflow-y-auto">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2 sticky top-0 bg-inherit py-2 border-b border-slate-700">
                <BookOpen size={20} />
                Sources
            </h3>
            <div className="space-y-4">
                {citations.map((cite, idx) => (
                    <div key={idx} className="p-3 rounded bg-slate-800/50 border border-slate-700 hover:border-slate-600 transition-colors">
                        <div className="flex justify-between items-start mb-2">
                            <span className="text-xs font-medium px-2 py-1 bg-blue-900/50 text-blue-300 rounded">
                                {cite.source}
                            </span>
                            <span className="text-xs text-slate-500">
                                p. {cite.page}
                            </span>
                        </div>
                        <p className="text-sm text-slate-400 line-clamp-3 italic">
                            "{cite.text}"
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CitationPanel;
