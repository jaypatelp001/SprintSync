/**
 * Login / Register Component
 */
import { useState } from 'react';
import { api } from '../api';

export default function Login({ onLogin }) {
    const [isRegister, setIsRegister] = useState(false);
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            let data;
            if (isRegister) {
                data = await api.register(username, email, password);
            } else {
                data = await api.login(username, password);
            }
            onLogin(data.user, data.access_token);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <h1>⚡ SprintSync</h1>
                    <p className="subtitle">AI-Powered Project Tracking</p>
                </div>

                <form onSubmit={handleSubmit} className="login-form">
                    <h2>{isRegister ? 'Create Account' : 'Welcome Back'}</h2>

                    {error && <div className="error-banner">{error}</div>}

                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            id="username"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter your username"
                            required
                            autoFocus
                        />
                    </div>

                    {isRegister && (
                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <input
                                id="email"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Enter your email"
                                required
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            required
                        />
                    </div>

                    <button type="submit" className="btn-primary" disabled={loading}>
                        {loading ? 'Please wait...' : (isRegister ? 'Sign Up' : 'Sign In')}
                    </button>

                    <p className="toggle-mode">
                        {isRegister ? 'Already have an account?' : "Don't have an account?"}
                        <button
                            type="button"
                            className="btn-link"
                            onClick={() => { setIsRegister(!isRegister); setError(''); }}
                        >
                            {isRegister ? 'Sign In' : 'Sign Up'}
                        </button>
                    </p>

                    {!isRegister && (
                        <div className="demo-credentials">
                            <p><strong>Demo:</strong> admin / admin123</p>
                        </div>
                    )}
                </form>
            </div>
        </div>
    );
}
