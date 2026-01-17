import React, { useState } from 'react';
import axios from 'axios';
import { Lock, UserPlus } from 'lucide-react';

const Login = ({ onLogin }) => {
    const [isRegisterMode, setIsRegisterMode] = useState(false);
    const [username, setUsername] = useState('admin');
    const [password, setPassword] = useState('admin');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccess('');

        if (isRegisterMode) {
            // Registration flow
            try {
                await axios.post('http://localhost:8000/api/v1/auth/register', {
                    username,
                    password
                });
                setSuccess('Registration successful! You can now login.');
                setIsRegisterMode(false);
                setPassword('');
            } catch (err) {
                console.error(err);
                setError(err.response?.data?.detail || 'Registration failed');
            } finally {
                setLoading(false);
            }
        } else {
            // Login flow
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            try {
                const res = await axios.post('http://localhost:8000/api/v1/auth/token', formData);
                const token = res.data.access_token;
                localStorage.setItem('token', token);
                onLogin(token);
            } catch (err) {
                console.error(err);
                setError('Invalid credentials');
            } finally {
                setLoading(false);
            }
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-slate-950 p-4">
            <div className="w-full max-w-md space-y-8 rounded-2xl bg-slate-900 p-8 shadow-2xl border border-slate-800">
                <div className="flex flex-col items-center">
                    <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-600">
                        {isRegisterMode ? <UserPlus className="h-6 w-6 text-white" /> : <Lock className="h-6 w-6 text-white" />}
                    </div>
                    <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-white">
                        {isRegisterMode ? 'Create Account' : 'Authenticated Access'}
                    </h2>
                    <p className="mt-2 text-center text-sm text-slate-400">
                        RAG Enterprise System
                    </p>
                </div>

                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    <div className="space-y-4 rounded-md shadow-sm">
                        <div>
                            <input
                                type="text"
                                required
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="relative block w-full rounded-lg border-slate-700 bg-slate-800 text-white p-3 placeholder-slate-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 sm:text-sm"
                                placeholder="Username"
                            />
                        </div>
                        <div>
                            <input
                                type="password"
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="relative block w-full rounded-lg border-slate-700 bg-slate-800 text-white p-3 placeholder-slate-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 sm:text-sm"
                                placeholder="Password"
                            />
                        </div>
                    </div>

                    {error && (
                        <div className="text-red-500 text-sm text-center bg-red-900/20 p-2 rounded">
                            {error}
                        </div>
                    )}

                    {success && (
                        <div className="text-green-500 text-sm text-center bg-green-900/20 p-2 rounded">
                            {success}
                        </div>
                    )}

                    <div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="group relative flex w-full justify-center rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold text-white hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-70 transition-all"
                        >
                            {loading ? (isRegisterMode ? 'Creating account...' : 'Signing in...') : (isRegisterMode ? 'Register' : 'Sign in')}
                        </button>
                    </div>
                </form>
                
                <div className="text-center">
                    <button
                        onClick={() => {
                            setIsRegisterMode(!isRegisterMode);
                            setError('');
                            setSuccess('');
                        }}
                        className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
                    >
                        {isRegisterMode ? 'Already have an account? Sign in' : "Don't have an account? Register"}
                    </button>
                </div>

                {!isRegisterMode && (
                    <div className="text-center text-xs text-slate-500">
                        Default credentials: admin / admin
                    </div>
                )}
            </div>
        </div>
    );
};

export default Login;
