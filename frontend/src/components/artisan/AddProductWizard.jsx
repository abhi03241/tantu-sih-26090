import React, { useState, useRef, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { DEMO_SAMPLE_CRAFTS } from '../../constants/categories';
import { LANGUAGES } from '../../constants/languages';
import { productService } from '../../services/products';
import { PRODUCT_STATUSES } from '../../services/mockData';
import confetti from 'canvas-confetti';
import {
  Camera, Upload, Trash2, RefreshCw, Mic, MicOff, Sparkles, Check, CheckCircle2,
  ArrowRight, ArrowLeft, RotateCcw, Volume2, Edit3, Image as ImageIcon,
  Save, AlertCircle, Layers, Ruler, Clock, Heart, FileText, X
} from 'lucide-react';

export default function AddProductWizard() {
  const { artisanProfile, language, navigateTo, showToast, speakText, refreshData, t } = useApp();

  // Wizard Steps:
  // 1 = Photo (Checkpoint 3)
  // 2 = Voice / Text Input (Checkpoint 4)
  // 3 = AI Processing (Checkpoint 5)
  // 4 = Catalogue Review (Checkpoint 6)
  // 5 = Published / Saved Celebration
  const [currentStep, setCurrentStep] = useState(1);

  // CHECKPOINT 3: PHOTO STATE
  const [photoUrl, setPhotoUrl] = useState(DEMO_SAMPLE_CRAFTS[0].imageUrl);
  const [photoLoading, setPhotoLoading] = useState(false);
  const [photoError, setPhotoError] = useState('');
  const fileInputRef = useRef(null);

  // CHECKPOINT 4: VOICE & TEXT FALLBACK STATE
  const [isRecording, setIsRecording] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [transcript, setTranscript] = useState(DEMO_SAMPLE_CRAFTS[0].voiceTranscriptHi);
  const [textFallback, setTextFallback] = useState('');
  const [inputMode, setInputMode] = useState('voice'); // 'voice' | 'text'
  const [voiceError, setVoiceError] = useState('');
  const speechRecognitionRef = useRef(null);
  const timerRef = useRef(null);

  // CHECKPOINT 5: AI PROCESSING STATE
  const [aiStages, setAiStages] = useState([
    { id: 1, name: 'Understanding your product...', nameHi: 'आपके उत्पाद को समझ रहे हैं...', status: 'pending' },
    { id: 2, name: 'Creating your catalogue...', nameHi: 'आपका कैटलॉग तैयार कर रहे हैं...', status: 'pending' },
    { id: 3, name: 'Improving your product photo...', nameHi: 'उत्पाद का फोटो बेहतर बना रहे हैं...', status: 'pending' },
    { id: 4, name: 'Preparing your price suggestion...', nameHi: 'उचित मूल्य का सुझाव तैयार कर रहे हैं...', status: 'pending' }
  ]);
  const [aiProgress, setAiProgress] = useState(0);
  const [aiError, setAiError] = useState('');

  // CHECKPOINT 6: CATALOGUE REVIEW STATE
  const [generatedProduct, setGeneratedProduct] = useState(null);
  const [viewEnhanced, setViewEnhanced] = useState(true);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editFormData, setEditFormData] = useState({});
  const [lastAction, setLastAction] = useState('publish'); // 'publish' | 'draft'

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (speechRecognitionRef.current) speechRecognitionRef.current.stop();
    };
  }, []);

  // -------------------------------------------------------------
  // CHECKPOINT 3: PHOTO HANDLING
  // -------------------------------------------------------------
  const handleSelectSample = (sample) => {
    setPhotoError('');
    setPhotoUrl(sample.imageUrl);
    const transcriptMap = {
      en: sample.voiceTranscriptEn,
      hi: sample.voiceTranscriptHi,
      bn: sample.voiceTranscriptBn,
      mr: sample.voiceTranscriptMr,
      as: sample.voiceTranscriptAs,
      ta: sample.voiceTranscriptTa,
      te: sample.voiceTranscriptTe,
    };
    setTranscript(transcriptMap[language] || sample.voiceTranscriptHi || sample.voiceTranscriptEn);
    showToast(`चुना गया: ${sample.title.split(' ')[0]}`, 'info');
  };

  const handleFileUpload = (e) => {
    setPhotoError('');
    const file = e.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      setPhotoError('कृपया केवल फोटो/इमेज फाइल चुनें');
      return;
    }

    setPhotoLoading(true);
    const reader = new FileReader();
    reader.onload = (uploadEvent) => {
      setPhotoUrl(uploadEvent.target.result);
      setPhotoLoading(false);
      showToast('फोटो लोड हो गया!', 'success');
    };
    reader.onerror = () => {
      setPhotoLoading(false);
      setPhotoError('फोटो अपलोड करने में समस्या हुई। कृपया पुनः प्रयास करें।');
    };
    reader.readAsDataURL(file);
  };

  const handleRemovePhoto = () => {
    setPhotoUrl('');
    setPhotoError('कृपया आगे बढ़ने के लिए एक फोटो चुनें या अपलोड करें।');
  };

  const handleProceedToVoice = () => {
    if (!photoUrl) {
      setPhotoError('कृपया आगे बढ़ने के लिए उत्पाद का एक फोटो अपलोड करें।');
      return;
    }
    setPhotoError('');
    setCurrentStep(2);
    speakText("अब बोलकर या लिखकर अपने उत्पाद के बारे में बताएं।");
  };

  // -------------------------------------------------------------
  // CHECKPOINT 4: VOICE & TEXT HANDLING
  // -------------------------------------------------------------
  const handleToggleRecord = () => {
    setVoiceError('');
    if (isRecording) {
      // Stop recording
      setIsRecording(false);
      clearInterval(timerRef.current);
      if (speechRecognitionRef.current) {
        speechRecognitionRef.current.stop();
      }
      showToast(t('recordedSuccess'), 'success');
    } else {
      // Start recording
      setIsRecording(true);
      setRecordingSeconds(0);
      timerRef.current = setInterval(() => {
        setRecordingSeconds(prev => prev + 1);
      }, 1000);

      // Web Speech API
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        try {
          const recognition = new SpeechRecognition();
          recognition.continuous = true;
          recognition.interimResults = true;
          const langObj = LANGUAGES.find(l => l.code === language);
          recognition.lang = langObj ? langObj.locale : (language === 'en' ? 'en-IN' : 'hi-IN');

          recognition.onresult = (event) => {
            let current = '';
            for (let i = 0; i < event.results.length; i++) {
              current += event.results[i][0].transcript;
            }
            if (current) {
              setTranscript(current);
            }
          };

          recognition.onerror = (err) => {
            console.warn("Speech recognition error:", err);
            setIsRecording(false);
            clearInterval(timerRef.current);
            setVoiceError("माइक्रोफ़ोन एक्सेस नहीं मिला। आप नीचे लिखकर भी विवरण दर्ज कर सकते हैं।");
          };

          speechRecognitionRef.current = recognition;
          recognition.start();
        } catch (e) {
          console.warn("Speech recognition failed:", e);
          setIsRecording(false);
          clearInterval(timerRef.current);
          setVoiceError("ब्राउज़र में ध्वनि पहचान उपलब्ध नहीं है। कृपया नीचे लिखकर दर्ज करें।");
        }
      } else {
        // Speech API not supported in browser environment: fallback to text mode cleanly
        setTimeout(() => {
          setIsRecording(false);
          clearInterval(timerRef.current);
          setInputMode('text');
          setVoiceError("इस ब्राउज़र में सीधा माइक उपलब्ध नहीं है। कृपया लिखकर बताएं।");
        }, 1200);
      }
    }
  };

  const effectiveNarrative = inputMode === 'text' ? textFallback : transcript;

  const handleProceedToAI = () => {
    if (!effectiveNarrative || !effectiveNarrative.trim()) {
      setVoiceError("कृपया बोलकर या लिखकर उत्पाद का कुछ विवरण दें।");
      return;
    }
    setVoiceError('');
    startAiProcessing();
  };

  // -------------------------------------------------------------
  // CHECKPOINT 5: AI PROCESSING PIPELINE
  // -------------------------------------------------------------
  const startAiProcessing = async () => {
    setCurrentStep(3);
    setAiError('');
    setAiProgress(10);
    speakText("तंतु AI आपके उत्पाद का विश्लेषण कर रहा है।");

    const baseProduct = {
      title: 'Handcrafted Artisan Craft',
      image_url: photoUrl,
      artisan_id: artisanProfile.id,
      artisan_name: artisanProfile.name,
      location: artisanProfile.location,
      status: PRODUCT_STATUSES.PROCESSING
    };

    try {
      // Stage 1: Understanding your product...
      updateStage(1, 'in-progress');
      await delay(900);
      setAiProgress(30);
      updateStage(1, 'completed');

      // Stage 2: Creating your catalogue...
      updateStage(2, 'in-progress');
      const voiceProcessed = await productService.processVoice('new-draft', {
        audio_transcript: effectiveNarrative,
        language: language
      });
      await delay(900);
      setAiProgress(60);
      updateStage(2, 'completed');

      // Stage 3: Improving your product photo...
      updateStage(3, 'in-progress');
      const enhanced = await productService.enhanceImage('new-draft', {
        image_url: photoUrl,
        prompt: 'Clean studio backdrop with soft warm lighting'
      });
      await delay(900);
      setAiProgress(85);
      updateStage(3, 'completed');

      // Stage 4: Preparing your price suggestion...
      updateStage(4, 'in-progress');
      const priced = await productService.calculatePrice('new-draft', {
        raw_material_cost: 300,
        labor_hours: 16
      });
      await delay(800);
      setAiProgress(100);
      updateStage(4, 'completed');

      // Assemble final generated product
      const finalProduct = {
        ...baseProduct,
        ...voiceProcessed,
        ...enhanced,
        ...priced,
        image_url: photoUrl,
        enhanced_image_url: enhanced.enhanced_image_url || photoUrl,
        id: `prod-${Date.now().toString(16).slice(-6)}`,
        status: PRODUCT_STATUSES.READY,
        created_at: new Date().toISOString()
      };

      setGeneratedProduct(finalProduct);
      setEditFormData(finalProduct);

      await delay(600);
      setCurrentStep(4);
      speakText("आपका कैटलॉग तैयार है! कृपया विवरण की समीक्षा करें।");
    } catch (err) {
      console.error("AI Pipeline error:", err);
      setAiError("AI प्रसंस्करण के दौरान समस्या आई। कृपया पुनः प्रयास करें।");
    }
  };

  const updateStage = (stageId, status) => {
    setAiStages(prev => prev.map(s => s.id === stageId ? { ...s, status } : s));
  };

  const delay = (ms) => new Promise(res => setTimeout(res, ms));

  // -------------------------------------------------------------
  // CHECKPOINT 6: SAVE DRAFT & PUBLISH
  // -------------------------------------------------------------
  const handlePublish = async () => {
    try {
      const payload = {
        ...generatedProduct,
        status: PRODUCT_STATUSES.PUBLISHED
      };
      await productService.createProduct(payload);
      refreshData();
      setLastAction('publish');
      setCurrentStep(5);

      try {
        confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
      } catch (e) {}

      showToast(t('publishedSuccess'), 'success');
      speakText("बधाई! आपका शिल्प सफलतापूर्वक प्रकाशित हो गया है।");
    } catch (e) {
      showToast("प्रकाशित करने में त्रुटि", "error");
    }
  };

  const handleSaveDraft = async () => {
    try {
      const payload = {
        ...generatedProduct,
        status: PRODUCT_STATUSES.DRAFT
      };
      await productService.saveDraft(payload);
      refreshData();
      setLastAction('draft');
      setCurrentStep(5);
      showToast("ड्राफ्ट सफलतापूर्वक सहेजा गया!", "info");
      speakText("आपका शिल्प ड्राफ्ट के रूप में सहेज लिया गया है।");
    } catch (e) {
      showToast("ड्राफ्ट सहेजने में त्रुटि", "error");
    }
  };

  const handleSaveEditModal = () => {
    setGeneratedProduct(prev => ({
      ...prev,
      ...editFormData,
      suggested_price_min: Number(editFormData.suggested_price_min) || prev.suggested_price_min,
      suggested_price_max: Number(editFormData.suggested_price_max) || prev.suggested_price_max
    }));
    setIsEditModalOpen(false);
    showToast("कैटलॉग विवरण अपडेट कर दिए गए हैं", "success");
  };

  return (
    <div>
      {/* Wizard Progress Dots */}
      {currentStep < 5 && (
        <div className="step-wizard-header">
          <div className="step-indicator-row">
            <div className={`step-dot ${currentStep === 1 ? 'active' : currentStep > 1 ? 'completed' : ''}`}>
              {currentStep > 1 ? <Check size={16} strokeWidth={3} /> : '1'}
            </div>
            <div className={`step-line ${currentStep > 1 ? 'completed' : ''}`} />
            <div className={`step-dot ${currentStep === 2 ? 'active' : currentStep > 2 ? 'completed' : ''}`}>
              {currentStep > 2 ? <Check size={16} strokeWidth={3} /> : '2'}
            </div>
            <div className={`step-line ${currentStep > 2 ? 'completed' : ''}`} />
            <div className={`step-dot ${currentStep === 3 ? 'active' : currentStep > 3 ? 'completed' : ''}`}>
              {currentStep > 3 ? <Check size={16} strokeWidth={3} /> : '3'}
            </div>
            <div className={`step-line ${currentStep > 3 ? 'completed' : ''}`} />
            <div className={`step-dot ${currentStep === 4 ? 'active' : ''}`}>
              4
            </div>
          </div>
        </div>
      )}

      {/* =========================================================================
          CHECKPOINT 3: PHOTO UPLOAD / PREVIEW / REPLACE / REMOVE
          ========================================================================= */}
      {currentStep === 1 && (
        <div>
          <div style={{ marginBottom: '18px' }}>
            <h2 className="wizard-title">{t('step1Photo')}</h2>
            <p className="wizard-sub">उत्पाद का स्पष्ट फोटो खींचें या गैलरी से चुनें</p>
          </div>

          {photoError && (
            <div style={{ background: '#FEE2E2', border: '1px solid #F87171', color: '#991B1B', padding: '10px 14px', borderRadius: '12px', fontSize: '0.82rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertCircle size={16} />
              <span>{photoError}</span>
            </div>
          )}

          {/* Photo Preview or Empty Box */}
          {photoUrl ? (
            <div className="photo-preview-box">
              <img src={photoUrl} alt="Product preview" className="photo-preview-img" />
              <div className="photo-preview-overlay">
                <span style={{ fontSize: '0.8rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <CheckCircle2 size={16} color="#10B981" />
                  <span>फोटो तैयार</span>
                </span>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <button
                    onClick={() => fileInputRef.current && fileInputRef.current.click()}
                    style={{ background: 'rgba(255, 255, 255, 0.95)', color: '#0F172A', padding: '5px 12px', borderRadius: '999px', fontSize: '0.75rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '4px' }}
                  >
                    <RefreshCw size={12} />
                    <span>बदलें (Replace)</span>
                  </button>
                  <button
                    onClick={handleRemovePhoto}
                    style={{ background: 'rgba(220, 38, 38, 0.95)', color: '#FFFFFF', padding: '5px 10px', borderRadius: '999px', fontSize: '0.75rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '4px' }}
                  >
                    <Trash2 size={12} />
                    <span>हटाएं</span>
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div
              className="upload-dropzone"
              onClick={() => fileInputRef.current && fileInputRef.current.click()}
            >
              <Camera size={44} color="#EA580C" style={{ marginBottom: '8px' }} />
              <div style={{ fontWeight: 800, fontSize: '1rem', color: 'var(--text-main)' }}>
                फोटो खींचें या अपलोड करें
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                PNG, JPG या WEBP समर्थित है
              </div>
            </div>
          )}

          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept="image/*"
            style={{ display: 'none' }}
          />

          {/* Large Action Buttons */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '20px' }}>
            <button
              className="btn-secondary-large"
              onClick={() => fileInputRef.current && fileInputRef.current.click()}
              disabled={photoLoading}
            >
              <Camera size={20} color="#EA580C" />
              <span>{photoLoading ? 'लोड हो रहा...' : t('takePhoto')}</span>
            </button>

            <button
              className="btn-secondary-large"
              onClick={() => fileInputRef.current && fileInputRef.current.click()}
              disabled={photoLoading}
            >
              <Upload size={20} color="#EA580C" />
              <span>{photoLoading ? 'लोड हो रहा...' : t('uploadPhoto')}</span>
            </button>
          </div>

          {/* Quick Demo Sample Picker */}
          <div style={{ marginBottom: '24px' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '10px' }}>
              या परीक्षण के लिए शिल्प चुनें:
            </div>
            <div className="sample-picker-grid">
              {DEMO_SAMPLE_CRAFTS.map((sample) => (
                <div
                  key={sample.id}
                  className={`sample-craft-card ${photoUrl === sample.imageUrl ? 'selected' : ''}`}
                  onClick={() => handleSelectSample(sample)}
                >
                  <img src={sample.imageUrl} alt={sample.title} className="sample-thumb" />
                  <div className="sample-craft-name">{sample.title.split(' ')[0]} {sample.category.split(' ')[0]}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Proceed Button */}
          <button
            className="btn-primary-large"
            onClick={handleProceedToVoice}
          >
            <span>आगे बढ़ें: उत्पाद की जानकारी दें</span>
            <ArrowRight size={20} />
          </button>
        </div>
      )}

      {/* =========================================================================
          CHECKPOINT 4: VOICE RECORDING & TEXT FALLBACK
          ========================================================================= */}
      {currentStep === 2 && (
        <div>
          <div style={{ marginBottom: '18px' }}>
            <h2 className="wizard-title">{t('step2Voice')}</h2>
            <p className="wizard-sub">बोलकर या लिखकर अपने शिल्प की कहानी और सामग्री बताएं</p>
          </div>

          {/* Voice / Text Mode Toggle */}
          <div style={{ display: 'flex', background: 'var(--primary-100)', padding: '4px', borderRadius: '14px', marginBottom: '18px' }}>
            <button
              onClick={() => setInputMode('voice')}
              style={{
                flex: 1,
                padding: '8px 12px',
                borderRadius: '10px',
                fontSize: '0.82rem',
                fontWeight: 700,
                background: inputMode === 'voice' ? '#FFFFFF' : 'transparent',
                color: inputMode === 'voice' ? 'var(--primary-800)' : 'var(--text-muted)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px'
              }}
            >
              <Mic size={15} />
              <span>आवाज़ से बताएं (Voice)</span>
            </button>
            <button
              onClick={() => setInputMode('text')}
              style={{
                flex: 1,
                padding: '8px 12px',
                borderRadius: '10px',
                fontSize: '0.82rem',
                fontWeight: 700,
                background: inputMode === 'text' ? '#FFFFFF' : 'transparent',
                color: inputMode === 'text' ? 'var(--primary-800)' : 'var(--text-muted)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px'
              }}
            >
              <FileText size={15} />
              <span>लिखकर बताएं (Text Fallback)</span>
            </button>
          </div>

          {voiceError && (
            <div style={{ background: '#FEF3C7', border: '1px solid #F59E0B', color: '#92400E', padding: '10px 14px', borderRadius: '12px', fontSize: '0.82rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertCircle size={16} />
              <span>{voiceError}</span>
            </div>
          )}

          {/* Voice Input Container */}
          {inputMode === 'voice' ? (
            <div className="voice-recorder-container">
              <div className="mic-button-wrapper">
                <button
                  className={`mic-circle-btn ${isRecording ? 'recording' : ''}`}
                  onClick={handleToggleRecord}
                >
                  {isRecording ? <MicOff size={42} /> : <Mic size={42} />}
                </button>
                {isRecording && <div className="mic-pulse-wave" />}
              </div>

              <div style={{ fontSize: '1.15rem', fontWeight: 800, color: isRecording ? '#DC2626' : 'var(--text-main)', marginBottom: '6px' }}>
                {isRecording ? `सुन रहे हैं... (00:${recordingSeconds < 10 ? '0' : ''}${recordingSeconds})` : 'माइक दबाकर बोलना शुरू करें'}
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-light)', maxWidth: '320px' }}>
                जैसे: "यह बांस की टोकरी है, असम के सिलचर में 3 दिन में बनी है..."
              </p>

              {isRecording && (
                <div className="voice-waveform-visualizer" style={{ marginTop: '14px' }}>
                  <div className="wave-bar" />
                  <div className="wave-bar" />
                  <div className="wave-bar" />
                  <div className="wave-bar" />
                  <div className="wave-bar" />
                  <div className="wave-bar" />
                  <div className="wave-bar" />
                  <div className="wave-bar" />
                </div>
              )}

              {transcript && (
                <div className="transcript-display-box">
                  <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary-700)', textTransform: 'uppercase', marginBottom: '4px' }}>
                    पहचानी गई आवाज़:
                  </div>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text-main)', fontStyle: 'italic' }}>
                    "{transcript}"
                  </p>
                  <div style={{ display: 'flex', gap: '8px', marginTop: '10px' }}>
                    <button
                      onClick={() => speakText(transcript)}
                      style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary-800)', display: 'flex', alignItems: 'center', gap: '4px' }}
                    >
                      <Volume2 size={14} />
                      <span>{t('playVoice')}</span>
                    </button>
                    <button
                      onClick={() => setTranscript('')}
                      style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-light)', display: 'flex', alignItems: 'center', gap: '4px' }}
                    >
                      <RotateCcw size={13} />
                      <span>{t('reRecord')}</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            /* Text Fallback Container */
            <div style={{ background: '#FFFFFF', border: '1.5px solid var(--border-light)', borderRadius: '20px', padding: '18px 16px', marginBottom: '20px' }}>
              <label style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '6px', display: 'block' }}>
                उत्पाद के बारे में संक्षेप में लिखें (हिन्दी या अंग्रेजी):
              </label>
              <textarea
                rows={4}
                value={textFallback}
                onChange={(e) => setTextFallback(e.target.value)}
                placeholder="उदा. यह हाथ से बुना बांस का झूला / टोकरी है। असम के सिलचर में प्राकृतिक बांस से 3 दिन में बना है।"
                style={{ width: '100%', padding: '12px', borderRadius: '12px', border: '1.5px solid var(--border-light)', fontSize: '0.9rem' }}
              />
            </div>
          )}

          {/* Navigation Buttons */}
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              className="btn-secondary-large"
              style={{ width: '40%' }}
              onClick={() => setCurrentStep(1)}
            >
              <ArrowLeft size={18} />
              <span>वापस</span>
            </button>

            <button
              className="btn-primary-large"
              style={{ width: '60%' }}
              onClick={handleProceedToAI}
            >
              <Sparkles size={18} />
              <span>AI कैटलॉग बनाएं</span>
            </button>
          </div>
        </div>
      )}

      {/* =========================================================================
          CHECKPOINT 5: AI PROCESSING SCREEN
          ========================================================================= */}
      {currentStep === 3 && (
        <div className="ai-processing-container">
          <div className="ai-processing-header">
            <div className="ai-sparkle-badge">
              <Sparkles size={15} />
              <span>TANTU MULTIMODAL AI PIPELINE</span>
            </div>
            <h2 className="ai-processing-title">तंतु AI विश्लेषण जारी है...</h2>
            <p className="ai-processing-sub">
              आपकी आवाज़ और फोटो से स्मार्ट कैटलॉग तैयार किया जा रहा है
            </p>
          </div>

          {/* Live Progress Indicator */}
          <div style={{ marginBottom: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94A3B8', marginBottom: '6px' }}>
              <span>प्रगति</span>
              <span>{aiProgress}%</span>
            </div>
            <div className="ai-overall-progress-bar">
              <div className="ai-progress-fill" style={{ width: `${aiProgress}%` }} />
            </div>
          </div>

          {/* 4 Friendly Messages Matching Prompt Specification */}
          <div className="ai-stages-list">
            {aiStages.map((stage) => {
              const isDone = stage.status === 'completed';
              const isInProgress = stage.status === 'in-progress';

              return (
                <div
                  key={stage.id}
                  className={`ai-stage-item ${isDone ? 'completed' : isInProgress ? 'in-progress' : ''}`}
                >
                  <div className="stage-icon-box">
                    {isDone ? (
                      <Check size={18} strokeWidth={3} />
                    ) : isInProgress ? (
                      <Sparkles size={18} />
                    ) : (
                      <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#64748B' }} />
                    )}
                  </div>
                  <div className="stage-text-wrap">
                    <div className="stage-title">{stage.nameHi}</div>
                    <div className="stage-desc">{stage.name}</div>
                  </div>
                  {isDone && (
                    <span style={{ fontSize: '0.7rem', color: '#10B981', fontWeight: 700 }}>सफल ✓</span>
                  )}
                </div>
              );
            })}
          </div>

          {aiError ? (
            <div style={{ textAlign: 'center', marginTop: '16px' }}>
              <p style={{ color: '#FCA5A5', fontSize: '0.85rem', marginBottom: '10px' }}>{aiError}</p>
              <button className="btn-primary-large" onClick={startAiProcessing}>
                <RefreshCw size={16} />
                <span>पुनः प्रयास करें (Retry)</span>
              </button>
            </div>
          ) : (
            <div style={{ textAlign: 'center', fontSize: '0.75rem', color: '#64748B' }}>
              NLP & Voice (M) • Vision Enhancement (R) • Smart Pricing (S)
            </div>
          )}
        </div>
      )}

      {/* =========================================================================
          CHECKPOINT 6: CATALOGUE REVIEW & SAVE DRAFT / PUBLISH
          ========================================================================= */}
      {currentStep === 4 && generatedProduct && (
        <div>
          <div style={{ marginBottom: '16px' }}>
            <h2 className="wizard-title">{t('step4Catalog')}</h2>
            <p className="wizard-sub">तैयार विवरण जांचें, सुधार करें और प्रकाशित करें</p>
          </div>

          <div className="catalog-display-card">
            {/* Before vs After Comparison */}
            <div className="comparison-toggle-bar">
              <button
                className={`toggle-btn ${viewEnhanced ? 'active' : ''}`}
                onClick={() => setViewEnhanced(true)}
              >
                <Sparkles size={14} color="#EA580C" />
                <span>AI स्टूडियो लाइटिंग फोटो</span>
              </button>
              <button
                className={`toggle-btn ${!viewEnhanced ? 'active' : ''}`}
                onClick={() => setViewEnhanced(false)}
              >
                <ImageIcon size={14} />
                <span>मूल फोटो (Original)</span>
              </button>
            </div>

            <div className="product-img-wrapper" style={{ height: '240px' }}>
              <img
                src={viewEnhanced ? generatedProduct.enhanced_image_url : generatedProduct.image_url}
                alt={generatedProduct.title}
                className="product-img"
              />
              <span className="badge-ai-enhanced">
                <Sparkles size={12} />
                <span>{viewEnhanced ? 'AI Studio Enhanced' : 'Raw Capture'}</span>
              </span>
              <span className="badge-category">{generatedProduct.category}</span>
            </div>

            <div className="catalog-body">
              <h3 className="catalog-title">{generatedProduct.title}</h3>
              {generatedProduct.description_hindi && (
                <p className="catalog-hindi-title">{generatedProduct.description_hindi}</p>
              )}
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '14px' }}>
                {generatedProduct.description_english}
              </p>

              {/* Specs */}
              <div className="spec-pills-row">
                <span className="spec-pill">
                  <Layers size={13} color="#EA580C" />
                  <span>{generatedProduct.material}</span>
                </span>
                <span className="spec-pill">
                  <Ruler size={13} color="#EA580C" />
                  <span>{generatedProduct.dimensions || '30cm x 30cm'}</span>
                </span>
                <span className="spec-pill">
                  <Clock size={13} color="#EA580C" />
                  <span>{generatedProduct.production_time || '3 days'}</span>
                </span>
              </div>

              {/* Tags */}
              {generatedProduct.tags && generatedProduct.tags.length > 0 && (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '16px' }}>
                  {generatedProduct.tags.map((tag, i) => (
                    <span
                      key={i}
                      style={{ background: '#F1F5F9', color: '#475569', padding: '3px 8px', borderRadius: '6px', fontSize: '0.72rem', fontWeight: 600 }}
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}

              {/* Story */}
              <div className="catalog-story-box">
                <div className="story-heading">
                  <Heart size={14} color="#D97706" />
                  <span>कारीगर की विरासत कथा ({generatedProduct.narrative_type || 'Cultural Heritage'})</span>
                </div>
                <p className="story-text">"{generatedProduct.story}"</p>
              </div>

              {/* Price Range */}
              <div className="pricing-highlight-box">
                <div>
                  <div className="pricing-title">AI अनुमानित उचित दर</div>
                  <div style={{ fontSize: '0.72rem', color: '#065F46' }}>कारीगर के लिए न्यायसंगत मूल्य</div>
                </div>
                <div className="pricing-range">
                  ₹{generatedProduct.suggested_price_min} - ₹{generatedProduct.suggested_price_max}
                </div>
              </div>

              {/* Action Buttons: Publish, Save Draft, Edit */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <button
                  className="btn-primary-large"
                  onClick={handlePublish}
                >
                  <Check size={20} strokeWidth={2.8} />
                  <span>प्रकाशित करें (Publish to Marketplace)</span>
                </button>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                  <button
                    className="btn-secondary-large"
                    onClick={handleSaveDraft}
                  >
                    <Save size={16} />
                    <span>ड्राफ्ट सहेजें (Save Draft)</span>
                  </button>

                  <button
                    className="btn-secondary-large"
                    onClick={() => setIsEditModalOpen(true)}
                  >
                    <Edit3 size={16} />
                    <span>सुधार करें (Edit)</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* =========================================================================
          CHECKPOINT 6 / PUBLISHED OR DRAFT CELEBRATION
          ========================================================================= */}
      {currentStep === 5 && (
        <div style={{ textAlign: 'center', padding: '36px 16px' }}>
          <div
            style={{
              width: '80px',
              height: '80px',
              borderRadius: '50%',
              background: lastAction === 'publish' ? 'linear-gradient(135deg, #10B981 0%, #059669 100%)' : 'linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)',
              color: '#FFFFFF',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 10px 25px rgba(16, 185, 129, 0.35)',
              marginBottom: '20px'
            }}
          >
            <Check size={42} strokeWidth={3} />
          </div>

          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-main)', marginBottom: '8px' }}>
            {lastAction === 'publish' ? 'बधाई हो! शिल्प प्रकाशित हो गया' : 'ड्राफ्ट सफलतापूर्वक सहेजा गया'}
          </h2>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: '1.5', maxWidth: '340px', margin: '0 auto 28px auto' }}>
            {lastAction === 'publish'
              ? 'आपका शिल्प अब बाज़ार में लाइव है और खरीदार थोक ऑर्डर भेज सकते हैं।'
              : 'आप इसे कभी भी "मेरे शिल्प" में जाकर पूरा कर सकते हैं।'}
          </p>

          <button
            className="btn-primary-large"
            onClick={() => navigateTo('my-products')}
          >
            <span>मेरे शिल्पों में देखें (My Crafts)</span>
            <ArrowRight size={20} />
          </button>

          <button
            className="btn-secondary-large"
            onClick={() => {
              setCurrentStep(1);
              setPhotoUrl(DEMO_SAMPLE_CRAFTS[0].imageUrl);
              setTranscript(DEMO_SAMPLE_CRAFTS[0].voiceTranscriptHi);
              setTextFallback('');
              setGeneratedProduct(null);
            }}
          >
            <span>+ एक और नया शिल्प जोड़ें</span>
          </button>
        </div>
      )}

      {/* Edit Catalogue Modal */}
      {isEditModalOpen && (
        <div className="modal-backdrop" onClick={() => setIsEditModalOpen(false)}>
          <div className="modal-content-sheet" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header-row">
              <h3 className="modal-title">कैटलॉग में सुधार करें</h3>
              <button className="modal-close-btn" onClick={() => setIsEditModalOpen(false)}>
                <X size={18} />
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div>
                <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>
                  शिल्प का नाम (Title)
                </label>
                <input
                  type="text"
                  value={editFormData.title || ''}
                  onChange={(e) => setEditFormData({ ...editFormData, title: e.target.value })}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '12px', border: '1.5px solid var(--border-light)' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>
                  हिन्दी विवरण
                </label>
                <textarea
                  rows={2}
                  value={editFormData.description_hindi || ''}
                  onChange={(e) => setEditFormData({ ...editFormData, description_hindi: e.target.value })}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '12px', border: '1.5px solid var(--border-light)' }}
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <div>
                  <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>
                    सामग्री (Material)
                  </label>
                  <input
                    type="text"
                    value={editFormData.material || ''}
                    onChange={(e) => setEditFormData({ ...editFormData, material: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '12px', border: '1.5px solid var(--border-light)' }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>
                    माप (Dimensions)
                  </label>
                  <input
                    type="text"
                    value={editFormData.dimensions || ''}
                    onChange={(e) => setEditFormData({ ...editFormData, dimensions: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '12px', border: '1.5px solid var(--border-light)' }}
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <div>
                  <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>
                    न्यूनतम मूल्य (₹ Min)
                  </label>
                  <input
                    type="number"
                    value={editFormData.suggested_price_min || ''}
                    onChange={(e) => setEditFormData({ ...editFormData, suggested_price_min: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '12px', border: '1.5px solid var(--border-light)' }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>
                    अधिकतम मूल्य (₹ Max)
                  </label>
                  <input
                    type="number"
                    value={editFormData.suggested_price_max || ''}
                    onChange={(e) => setEditFormData({ ...editFormData, suggested_price_max: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '12px', border: '1.5px solid var(--border-light)' }}
                  />
                </div>
              </div>

              <button
                className="btn-primary-large"
                onClick={handleSaveEditModal}
                style={{ marginTop: '10px' }}
              >
                <span>बदलाव सहेजें</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
