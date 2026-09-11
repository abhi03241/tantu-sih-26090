import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { LANGUAGES } from '../../constants/languages';
import { Globe, Smartphone, Monitor, Volume2, Sparkles, ShoppingBag, Palette } from 'lucide-react';

export default function Header() {
  const {
    language,
    setLanguage,
    role,
    switchRole,
    backendOnline,
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
      speakText("तंतु कारीगर मंच में आपका स्वागत है। नया उत्पाद जोड़ने के लिए नीचे दिए गए नारंगी बटन को दबाएं।");
    } else {
      speakText("तंतु बाज़ार में आपका स्वागत है। भारत के ग्रामीण कारीगरों से सीधे थोक ऑर्डर करें।");
    }
  };

  return (
    <header className="app-header">
      <div className="header-brand" onClick={() => navigateTo(role === 'artisan' ? 'home' : 'marketplace')} style={{ cursor: 'pointer' }}>
        <div className="brand-icon-box">
          <Sparkles size={22} />
        </div>
        <div>
          <div className="brand-title">
            <span>तंतु</span>
            <span style={{ fontSize: '1.05rem', color: 'var(--text-main)', fontWeight: 800 }}>TANTU</span>
          </div>
          <div className="brand-subtitle">
            {backendOnline ? '🟢 Backend Live' : '🟡 AI Demo Active'}
          </div>
        </div>
      </div>

      <div className="header-actions">
        {/* Audio helper for low literacy */}
        <button
          className={`pill-btn ${ttsSpeaking ? 'speaking' : ''}`}
          onClick={handleSpeechHelper}
          title={t('listenToScreen')}
          style={{ padding: '6px 10px' }}
        >
          <Volume2 size={16} color={ttsSpeaking ? '#EA580C' : '#57534E'} />
        </button>

        {/* Language Picker */}
        <div style={{ position: 'relative' }}>
          <button
            className="pill-btn"
            onClick={() => setLangMenuOpen(!langMenuOpen)}
            title="Change Language"
          >
            <Globe size={15} />
            <span>{currentLangObj.name}</span>
          </button>

          {langMenuOpen && (
            <div
              style={{
                position: 'absolute',
                top: '110%',
                right: 0,
                background: '#FFFFFF',
                borderRadius: '16px',
                boxShadow: 'var(--shadow-lg)',
                border: '1px solid var(--border-light)',
                minWidth: '200px',
                padding: '8px',
                zIndex: 100
              }}
            >
              <div style={{ fontSize: '0.75rem', fontWeight: 700, padding: '6px 10px', color: 'var(--text-light)', borderBottom: '1px solid var(--border-light)' }}>
                {t('selectLanguage')}
              </div>
              <div style={{ maxHeight: '280px', overflowY: 'auto' }}>
                {LANGUAGES.map((l) => (
                  <button
                    key={l.code}
                    onClick={() => {
                      setLanguage(l.code);
                      setLangMenuOpen(false);
                    }}
                    style={{
                      width: '100%',
                      textAlign: 'left',
                      padding: '8px 12px',
                      borderRadius: '8px',
                      fontSize: '0.85rem',
                      fontWeight: language === l.code ? 700 : 500,
                      background: language === l.code ? 'var(--primary-100)' : 'transparent',
                      color: language === l.code ? 'var(--primary-800)' : 'var(--text-main)',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}
                  >
                    <span>{l.name}</span>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-light)' }}>{l.englishName}</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Role Switcher Pill */}
        <button
          className={`pill-btn role-badge ${role === 'buyer' ? 'buyer' : ''}`}
          onClick={() => switchRole(role === 'artisan' ? 'buyer' : 'artisan')}
          title="Switch persona between Artisan and Buyer"
        >
          {role === 'artisan' ? <Palette size={14} /> : <ShoppingBag size={14} />}
          <span>{role === 'artisan' ? t('artisanRole').split(' ')[0] : t('buyerRole').split(' ')[0]}</span>
        </button>

        {/* Device Frame Toggle (for presentation) */}
        <button
          className="pill-btn"
          onClick={() => setDeviceFrame(!deviceFrame)}
          title={deviceFrame ? "Full view" : "Mobile device frame view"}
          style={{ padding: '6px 8px' }}
        >
          {deviceFrame ? <Monitor size={15} /> : <Smartphone size={15} />}
        </button>
      </div>
    </header>
  );
}
