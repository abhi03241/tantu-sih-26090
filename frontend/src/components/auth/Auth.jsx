import React, { useState } from 'react';
import {
  Store,
  ShoppingBag,
  ArrowRight,
  Eye,
  EyeOff,
  Volume2,
  Mic,
  TrendingUp,
  Users
} from 'lucide-react';

import { loginUser, registerUser } from '../../services/authService';
import { LANGUAGES } from '../../constants/languages';
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
      <div className="auth-shell">

        {/* Brand bar */}
        <header className="auth-brandbar">
          <span className="auth-wordmark">
            ShilpVani
            <span className="auth-wordmark-dot" aria-hidden="true" />
          </span>
          <span className="auth-wordmark-hi">शिल्पवाणी</span>
        </header>

        {/* Heading */}
        <section className="auth-hero">
          <span className="auth-eyebrow">
            {mode === 'login' ? 'Welcome back' : 'Join the marketplace'}
          </span>
          <h1 className="auth-title">
            {mode === 'login'
              ? 'Login to ShilpVani'
              : 'Create your account'}
          </h1>
          <p className="auth-lead">
            Connecting India&apos;s artisans with buyers through voice
            intelligence.
          </p>
        </section>

        {/* Role selection */}
        <div
          className="auth-role-selection"
          role="group"
          aria-label="Choose account type"
        >
          <button
            type="button"
            className={`auth-role ${role === 'artisan' ? 'active' : ''}`}
            onClick={() => selectRole('artisan')}
            aria-pressed={role === 'artisan'}
          >
            <span className="auth-role-text">
              <strong>कारीगर / Artisan</strong>
              <small>Voice first · Sell crafts</small>
            </span>
            <Store size={20} />
          </button>

          <button
            type="button"
            className={`auth-role ${role === 'buyer' ? 'active' : ''}`}
            onClick={() => selectRole('buyer')}
            aria-pressed={role === 'buyer'}
          >
            <span className="auth-role-text">
              <strong>खरीदार / Buyer</strong>
              <small>Direct sourcing · B2B</small>
            </span>
            <ShoppingBag size={20} />
          </button>
        </div>

        {/* Voice help card (existing "Listen to instructions" feature) */}
        <button
          type="button"
          className="auth-voice"
          onClick={handleVoiceHelp}
        >
          <span className="auth-voice-icon">
            <Volume2 size={18} />
          </span>
          <span className="auth-voice-text">
            <strong>सुनकर समझें</strong>
            <small>Listen to instructions</small>
          </span>
        </button>

        {/* Form card */}
        <div className="auth-card">
          <div className="auth-tabs" role="tablist">
            <button
              type="button"
              role="tab"
              aria-selected={mode === 'login'}
              className={mode === 'login' ? 'active' : ''}
              onClick={() => changeMode('login')}
            >
              Login
            </button>

            <button
              type="button"
              role="tab"
              aria-selected={mode === 'signup'}
              className={mode === 'signup' ? 'active' : ''}
              onClick={() => changeMode('signup')}
            >
              Sign Up
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {mode === 'signup' && (
              <div className="auth-field">
                <label htmlFor="auth-name">Full Name</label>
                <input
                  id="auth-name"
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
              <label htmlFor="auth-phone">मोबाइल नंबर / Mobile Number</label>

              <div className="auth-phone-input">
                <span>+91</span>
                <input
                  id="auth-phone"
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
              <label htmlFor="auth-password">Password</label>

              <div className="auth-password-input">
                <input
                  id="auth-password"
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
                <label htmlFor="auth-confirm">Confirm Password</label>

                <input
                  id="auth-confirm"
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
        </div>

        {/* Supported languages */}
        <section className="auth-panel">
          <div className="auth-panel-head">
            <span className="auth-eyebrow">
              {LANGUAGES.length} regional languages
            </span>
            <span className="auth-panel-note">Voice cataloguing</span>
          </div>
          <div className="auth-chips">
            {LANGUAGES.map((lang) => (
              <span key={lang.code} className="auth-chip">
                {lang.name}
              </span>
            ))}
          </div>
        </section>

        {/* What the platform offers */}
        <section className="auth-features">
          <div className="auth-feature">
            <Mic size={18} />
            <strong>Voice first</strong>
            <small>Describe crafts by speaking</small>
          </div>
          <div className="auth-feature">
            <TrendingUp size={18} />
            <strong>Smart pricing</strong>
            <small>AI price guidance</small>
          </div>
          <div className="auth-feature">
            <Users size={18} />
            <strong>Direct buyers</strong>
            <small>Bulk order requests</small>
          </div>
        </section>

        <footer className="auth-footer">
          <p>Made for India&apos;s artisans</p>
        </footer>
      </div>
    </div>
  );
}