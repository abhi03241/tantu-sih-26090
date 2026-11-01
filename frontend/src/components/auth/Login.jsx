
import React, { useState } from 'react';
import {
  Store,
  ShoppingBag,
  ArrowRight,
  Volume2,
  CheckCircle
} from 'lucide-react';

import { useApp } from '../../context/AppContext';
import ShilpVaniLogo from '../common/ShilpVaniLogo';
import './Login.css';

export default function Login() {
  const { role, switchRole, t, speakText } = useApp();

  const [selectedRole, setSelectedRole] = useState(
    role || 'artisan'
  );

  const handleContinue = () => {
    // Demo entry only. Real authentication is not connected yet.
    switchRole(selectedRole);
  };

  const handleListen = () => {
    speakText(
      `${t('appTitle')}. ${t('tagline')}. ` +
      `${t('artisanRole')}. ${t('buyerRole')}.`
    );
  };

  return (
    <div className="login-screen">

      <div className="login-card">

        {/* Logo and Branding */}
        <div className="login-brand">
          <div className="login-logo">
            <ShilpVaniLogo size={52} />
          </div>

          <h1>ShilpVani</h1>
          <p className="login-hindi">शिल्पवाणी</p>

          <p className="login-tagline">
            {t('tagline')}
          </p>
        </div>

        {/* Welcome */}
        <div className="login-heading">
          <h2>Welcome!</h2>
          <p>
            Choose how you want to use ShilpVani.
          </p>
        </div>

        {/* Role Selection */}
        <div className="login-role-section">

          <button
            type="button"
            className={`login-role-card ${
              selectedRole === 'artisan' ? 'selected' : ''
            }`}
            onClick={() => setSelectedRole('artisan')}
            aria-pressed={selectedRole === 'artisan'}
          >
            <div className="login-role-icon artisan-icon">
              <Store size={27} />
            </div>

            <div className="login-role-info">
              <h3>{t('artisanRole')}</h3>
              <p>Create and sell your handmade crafts</p>
            </div>

            {selectedRole === 'artisan' && (
              <CheckCircle
                className="login-check"
                size={22}
              />
            )}
          </button>

          <button
            type="button"
            className={`login-role-card ${
              selectedRole === 'buyer' ? 'selected' : ''
            }`}
            onClick={() => setSelectedRole('buyer')}
            aria-pressed={selectedRole === 'buyer'}
          >
            <div className="login-role-icon buyer-icon">
              <ShoppingBag size={27} />
            </div>

            <div className="login-role-info">
              <h3>{t('buyerRole')}</h3>
              <p>Explore and purchase handmade crafts</p>
            </div>

            {selectedRole === 'buyer' && (
              <CheckCircle
                className="login-check"
                size={22}
              />
            )}
          </button>

        </div>

        {/* Continue Button */}
        <button
          type="button"
          className="login-continue-btn"
          onClick={handleContinue}
        >
          <span>{t('continueBtn')}</span>
          <ArrowRight size={20} />
        </button>

        {/* Voice Assistance */}
        <button
          type="button"
          className="login-voice-btn"
          onClick={handleListen}
        >
          <Volume2 size={19} />
          Listen to instructions
        </button>

        <div className="login-footer">
          <p>
            Made with ❤️ for India's artisans
          </p>
          <small>
            Demo access · OTP authentication is not
            connected yet.
          </small>
        </div>

      </div>
    </div>
  );
}
