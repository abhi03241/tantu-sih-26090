import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { LANGUAGES } from '../../constants/languages';
import ShilpVaniLogo from './ShilpVaniLogo';
import {
  Globe,
  Smartphone,
  Monitor,
  Volume2,
  LogOut
} from 'lucide-react';

export default function Header() {
  const {
    language,
    setLanguage,
    role,
    logout,
    deviceFrame,
    setDeviceFrame,
    speakText,
    ttsSpeaking,
    t,
    navigateTo
  } = useApp();

  const [langMenuOpen, setLangMenuOpen] = useState(false);

  const currentLangObj = LANGUAGES.find(l => l.code === language) || LANGUAGES[0];

  const handleSpeechHelper = () => {
    if (role === 'artisan') {
      speakText("शिल्पवाणी कारीगर मंच में आपका स्वागत है। नया उत्पाद जोड़ने के लिए नीचे दिए गए नारंगी बटन को दबाएं।");
    } else {
      speakText("शिल्पवाणी बाज़ार में आपका स्वागत है। भारत के ग्रामीण कारीगरों से सीधे थोक ऑर्डर करें।");
    }
  };

  return (
    <header className="app-header">
      {/* Brand: click goes to the role's home screen */}
      <button
        type="button"
        className="header-brand"
        onClick={() => navigateTo(role === 'artisan' ? 'home' : 'marketplace')}
        aria-label="ShilpVani home"
      >
        <ShilpVaniLogo size={28} />
        <span className="brand-title">ShilpVani</span>
        <span className="brand-divider" aria-hidden="true" />
        <span className="brand-role">
          {role === 'artisan' ? 'Crafts' : 'Market'}
        </span>
      </button>

      <div className="header-actions">
        {/* Audio helper for low literacy */}
        <button
          type="button"
          className={`pill-btn ${ttsSpeaking ? 'speaking' : ''}`}
          onClick={handleSpeechHelper}
          title={t('listenToScreen')}
          aria-label="Listen to this screen"
        >
          <Volume2 size={16} />
        </button>

        {/* Language Picker */}
        <div className="lang-menu-wrap">
          <button
            type="button"
            className="pill-btn"
            onClick={() => setLangMenuOpen(!langMenuOpen)}
            title="Change Language"
            aria-haspopup="listbox"
            aria-expanded={langMenuOpen}
          >
            <Globe size={15} />
            <span>{currentLangObj.name}</span>
          </button>

          {langMenuOpen && (
            <div className="lang-menu" role="listbox">
              <div className="lang-menu-title">
                भाषा चुनें (Select Language)
              </div>
              <div className="lang-menu-list">
                {LANGUAGES.map((l) => (
                  <button
                    key={l.code}
                    type="button"
                    role="option"
                    aria-selected={language === l.code}
                    className={`lang-menu-item ${language === l.code ? 'active' : ''}`}
                    onClick={() => {
                      setLanguage(l.code);
                      setLangMenuOpen(false);
                    }}
                  >
                    <span>{l.name}</span>
                    <small>{l.englishName}</small>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Logout Button */}
        <button
          type="button"
          className="pill-btn header-logout"
          onClick={logout}
          title="Logout from your account"
          aria-label="Logout"
        >
          <LogOut size={15} />
          <span>Logout</span>
        </button>

        {/* Device Frame Toggle (for presentation) */}
        <button
          type="button"
          className="pill-btn"
          onClick={() => setDeviceFrame(!deviceFrame)}
          title={deviceFrame ? "Full view" : "Mobile device frame view"}
          aria-label="Toggle mobile frame view"
        >
          {deviceFrame ? <Monitor size={15} /> : <Smartphone size={15} />}
        </button>
      </div>
    </header>
  );
}