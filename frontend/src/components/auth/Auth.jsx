
import React, { useState } from 'react';
import {
  Store,
  ShoppingBag,
  ArrowRight,
  ArrowLeft,
  Eye,
  EyeOff,
  Volume2
} from 'lucide-react';

import { loginUser, registerUser } from '../../services/authService';
import './Auth.css';

export default function Auth({ onAuthSuccess }) {
  const [role, setRole] = useState('artisan');
  const [mode, setMode] = useState('login');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [form, setForm] = useState({
    name: '',
    phone: '',
    password: '',
    confirmPassword: ''
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const selectRole = (selectedRole) => {
    setRole(selectedRole);
    setError('');
  };

  const changeMode = (newMode) => {
    setMode(newMode);
    setError('');
    setForm({
      name: '',
      phone: '',
      password: '',
      confirmPassword: ''
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!/^[6-9]\d{9}$/.test(form.phone)) {
      setError('Enter a valid 10-digit Indian mobile number.');
      return;
    }

    if (form.password.length < 8) {
      setError('Password must contain at least 8 characters.');
      return;
    }

    if (mode === 'signup') {
      if (!form.name.trim()) {
        setError('Please enter your full name.');
        return;
      }

      if (form.password !== form.confirmPassword) {
        setError('Passwords do not match.');
        return;
      }
    }

    setLoading(true);

    try {
      let result;

      if (mode === 'signup') {
        result = await registerUser({
          full_name: form.name.trim(),
          phone: form.phone,
          password: form.password,
          role
        });
      } else {
        result = await loginUser({
          phone: form.phone,
          password: form.password,
          role
        });
      }

      const user = result.user || {
  role: result.role || role
};

// Check whether the selected role matches the account role
if (user.role !== role) {
  throw new Error('Your account belongs to a different role.');
}

// Store the token after role validation
if (result.access_token) {
  localStorage.setItem('access_token', result.access_token);
}

// Continue to the correct dashboard
onAuthSuccess(user);

    } catch (err) {
      setError(
        err.message || 'Something went wrong. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceHelp = () => {
    if ('speechSynthesis' in window) {
      const message = new SpeechSynthesisUtterance(
        'Welcome to ShilpVani. Select whether you are an artisan or a buyer. Then login or create a new account.'
      );

      message.lang = 'en-IN';
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(message);
    }
  };

  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="auth-brand">
          <div className="auth-logo">शि</div>
          <h1>ShilpVani</h1>
          <p>शिल्पवाणी</p>
          <span>
            Empowering artisans through technology
          </span>
        </div>

        <div className="auth-heading">
          <h2>
            {mode === 'login'
              ? 'Welcome Back!'
              : 'Create Your Account'}
          </h2>

          <p>
            {mode === 'login'
              ? 'Login to continue your journey.'
              : 'Join ShilpVani and get started.'}
          </p>
        </div>

        {/* Role Selection */}

        <div className="auth-role-selection">

          <button
            type="button"
            className={`auth-role ${
              role === 'artisan' ? 'active' : ''
            }`}
            onClick={() => selectRole('artisan')}
          >
            <Store size={23} />
            <span>Artisan</span>
          </button>

          <button
            type="button"
            className={`auth-role ${
              role === 'buyer' ? 'active' : ''
            }`}
            onClick={() => selectRole('buyer')}
          >
            <ShoppingBag size={23} />
            <span>Buyer</span>
          </button>

        </div>

        {/* Login / Signup Tabs */}

        <div className="auth-tabs">

          <button
            type="button"
            className={mode === 'login' ? 'active' : ''}
            onClick={() => changeMode('login')}
          >
            Login
          </button>

          <button
            type="button"
            className={mode === 'signup' ? 'active' : ''}
            onClick={() => changeMode('signup')}
          >
            Sign Up
          </button>

        </div>

        <form onSubmit={handleSubmit}>

          {mode === 'signup' && (
            <div className="auth-field">
              <label>Full Name</label>
              <input
                type="text"
                name="name"
                placeholder="Enter your full name"
                value={form.name}
                onChange={handleChange}
                autoComplete="name"
                required
              />
            </div>
          )}

          <div className="auth-field">
            <label>Mobile Number</label>

            <div className="auth-phone-input">
              <span>+91</span>
              <input
                type="tel"
                name="phone"
                placeholder="10-digit mobile number"
                value={form.phone}
                onChange={handleChange}
                maxLength={10}
                inputMode="numeric"
                autoComplete="tel-national"
                required
              />
            </div>
          </div>

          <div className="auth-field">
            <label>Password</label>

            <div className="auth-password-input">
              <input
                type={showPassword ? 'text' : 'password'}
                name="password"
                placeholder="Enter password"
                value={form.password}
                onChange={handleChange}
                autoComplete={
                  mode === 'login'
                    ? 'current-password'
                    : 'new-password'
                }
                required
              />

              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                aria-label="Toggle password visibility"
              >
                {showPassword
                  ? <EyeOff size={19} />
                  : <Eye size={19} />
                }
              </button>
            </div>
          </div>

          {mode === 'signup' && (
            <div className="auth-field">
              <label>Confirm Password</label>

              <input
                type="password"
                name="confirmPassword"
                placeholder="Re-enter your password"
                value={form.confirmPassword}
                onChange={handleChange}
                autoComplete="new-password"
                required
              />
            </div>
          )}

          {error && (
            <div className="auth-error" role="alert">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="auth-submit"
            disabled={loading}
          >
            {loading
              ? 'Please wait...'
              : mode === 'login'
                ? 'Login'
                : 'Create Account'
            }

            {!loading && <ArrowRight size={19} />}
          </button>

        </form>

        <button
          type="button"
          className="auth-voice"
          onClick={handleVoiceHelp}
        >
          <Volume2 size={18} />
          Listen to instructions
        </button>

        <div className="auth-footer">
          <p>Made with ❤️ for India's artisans</p>
        </div>

      </div>
    </div>
  );
}
