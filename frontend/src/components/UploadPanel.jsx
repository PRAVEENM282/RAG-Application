import React, { useState } from 'react';
import axios from 'axios';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';

const UploadPanel = () => {
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState(null); // success | error
    const [message, setMessage] = useState("");

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        setUploading(true);
        setStatus(null);
        
        try {
            const res = await axios.post('http://localhost:8000/api/v1/ingest', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setStatus("success");
            setMessage(`Ingested: ${file.name}`);
        } catch (err) {
            console.error(err);
            setStatus("error");
            setMessage("Upload failed");
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="card mb-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Upload size={20} />
                Ingest Documents
            </h3>
            
            <div className="relative group cursor-pointer border-2 border-dashed border-slate-600 rounded-lg p-8 text-center hover:border-blue-500 transition-colors">
                <input 
                    type="file" 
                    onChange={handleFileUpload}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    disabled={uploading}
                />
                <div className="flex flex-col items-center gap-2 text-slate-400 group-hover:text-blue-400">
                    <FileText size={32} />
                    <span className="text-sm">
                        {uploading ? "Uploading..." : "Drop PDF or Text files here"}
                    </span>
                </div>
            </div>

            {status && (
                <div className={`mt-4 flex items-center gap-2 text-sm p-3 rounded-md ${
                    status === 'success' ? 'bg-green-900/30 text-green-400' : 'bg-red-900/30 text-red-400'
                }`}>
                    {status === 'success' ? <CheckCircle size={16} /> : <AlertCircle size={16} />}
                    {message}
                </div>
            )}
        </div>
    );
};

export default UploadPanel;
