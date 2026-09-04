import React from 'react';
import { useApp } from '../../context/AppContext';
import { LANGUAGES } from '../../constants/languages';
import { Volume2, Sparkles, ArrowRight, Check } from 'lucide-react';

export default function LanguageSelection({ onComplete }) {
  const { language, setLanguage, speakText, t } = useApp();

  const handleSelect = (code) => {
    setLanguage(code);
    const item = LANGUAGES.find(l => l.code === code);
    if (item) {
      speakText(item.greeting, code);
    }
  };

  return (
    <div style={{ padding: '24px 16px', minHeight: '80vh', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
      <div style={{ textAlign: 'center', marginBottom: '28px' }}>
        <div
          style={{
            width: '64px',
            height: '64px',
            borderRadius: '20px',
            background: 'linear-gradient(135deg, var(--terracotta) 0%, var(--turmeric) 100%)',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#FFFFFF',
            boxShadow: '0 8px 20px rgba(200, 75, 32, 0.3)',
            marginBottom: '16px'
          }}
        >
          <Sparkles size={32} />
        </div>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--terracotta-dark)', marginBottom: '6px' }}>
          तंतु TANTU
        </h1>
        <p style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '4px' }}>
          अपनी भाषा चुनें / Choose Language
        </p>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          सुविधाजनक उपयोग के लिए अपनी मातृभाषा का चयन करें
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px', marginBottom: '28px' }}>
        {LANGUAGES.map((item) => {
          const isSelected = language === item.code;
          return (
            <button
              key={item.code}
              onClick={() => handleSelect(item.code)}
              style={{
                background: isSelected ? 'var(--primary-50)' : '#FFFFFF',
                border: isSelected ? '2px solid var(--terracotta)' : '1.5px solid var(--border-light)',
                borderRadius: '16px',
                padding: '16px 12px',
                textAlign: 'center',
                boxShadow: isSelected ? '0 4px 12px rgba(200, 75, 32, 0.15)' : 'var(--shadow-sm)',
                position: 'relative',
                transition: 'all 0.2s ease'
              }}
            >
              {isSelected && (
                <div
                  style={{
                    position: 'absolute',
                    top: '8px',
                    right: '8px',
                    width: '20px',
                    height: '20px',
                    borderRadius: '50%',
                    background: 'var(--terracotta)',
                    color: '#FFFFFF',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                >
                  <Check size={12} strokeWidth={3} />
                </div>
              )}
              <div style={{ fontSize: '1.25rem', fontWeight: 800, color: isSelected ? 'var(--terracotta)' : 'var(--text-main)', marginBottom: '4px' }}>
                {item.name}
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-light)', fontWeight: 600 }}>
                {item.englishName}
              </div>
            </button>
          );
        })}
      </div>

      <button
        className="btn-primary-large"
        onClick={() => {
          if (onComplete) onComplete();
        }}
        style={{ minHeight: '56px', fontSize: '1.1rem' }}
      >
        <span>{t('continueBtn')}</span>
        <ArrowRight size={20} />
      </button>

      <div style={{ textAlign: 'center', marginTop: '14px' }}>
        <button
          onClick={() => speakText("तंतु में आपका स्वागत है। आगे बढ़ने के लिए अपनी भाषा चुनकर नारंगी बटन दबाएं।")}
          className="tts-speaker-btn"
        >
          <Volume2 size={16} />
          <span>निर्देश सुनें (Listen Guide)</span>
        </button>
      </div>
    </div>
  );
}
