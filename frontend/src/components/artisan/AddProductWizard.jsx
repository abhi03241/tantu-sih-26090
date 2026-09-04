import React, { useState, useRef, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { DEMO_SAMPLE_CRAFTS, CRAFT_CATEGORIES } from '../../constants/categories';
import { productService } from '../../services/products';
import confetti from 'canvas-confetti';
import {
  Camera, Upload, Mic, MicOff, Sparkles, Check, CheckCircle2,
  ArrowRight, ArrowLeft, RotateCcw, Volume2, Edit3, Image as ImageIcon,
  Sliders, ShieldCheck, Tag, Clock, Ruler, Layers, Heart
} from 'lucide-react';

export default function AddProductWizard() {
  const { artisanProfile, language, navigateTo, showToast, speakText, refreshData, t } = useApp();

  // Wizard Steps: 1 = Photo, 2 = Voice, 3 = AI Processing, 4 = Catalog Review, 5 = Published Success
  const [currentStep, setCurrentStep] = useState(1);

  // Step 1: Photo state
  const [photoUrl, setPhotoUrl] = useState(DEMO_SAMPLE_CRAFTS[0].imageUrl);
  const [photoSource, setPhotoSource] = useState('sample');
  const fileInputRef = useRef(null);

  // Step 2: Voice state
  const [isRecording, setIsRecording] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [transcript, setTranscript] = useState(DEMO_SAMPLE_CRAFTS[0].voiceTranscriptHi);
  const [hasVoiceRecorded, setHasVoiceRecorded] = useState(true);
  const speechRecognitionRef = useRef(null);
  const timerRef = useRef(null);

  // Step 3: AI Processing state
  const [aiStages, setAiStages] = useState([
    { id: 1, name: 'Understanding your voice (आवाज़ का विश्लेषण)', desc: 'Natural speech-to-text and dialect translation', status: 'pending', icon: 'mic' },
    { id: 2, name: 'Identifying product & craft category (उत्पाद की पहचान)', desc: 'Detecting craft lineage & raw materials', status: 'pending', icon: 'search' },
    { id: 3, name: 'Creating bilingual catalogue & story (कैटलॉग और विरासत निर्माण)', desc: 'Crafting English & Hindi narrative descriptions', status: 'pending', icon: 'file' },
    { id: 4, name: 'Enhancing image with AI studio lighting (चित्र संवर्धन)', desc: 'Removing background noise & simulating softbox lighting', status: 'pending', icon: 'image' },
    { id: 5, name: 'Estimating fair market price range (उचित मूल्य अनुमान)', desc: 'Calculating material costs, hours & fair artisan margin', status: 'pending', icon: 'tag' }
  ]);
  const [aiProgress, setAiProgress] = useState(0);

  // Step 4: Generated Catalogue state
  const [generatedProduct, setGeneratedProduct] = useState(null);
  const [viewEnhanced, setViewEnhanced] = useState(true); // Before vs After toggle
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editFormData, setEditFormData] = useState({});

  // Clean up timer
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (speechRecognitionRef.current) speechRecognitionRef.current.stop();
    };
  }, []);

  // One-click demo sample picker
  const handleSelectSample = (sample) => {
    setPhotoUrl(sample.imageUrl);
    setPhotoSource('sample');
    setTranscript(language === 'hi' ? sample.voiceTranscriptHi : sample.voiceTranscriptEn);
    setHasVoiceRecorded(true);
    showToast(`चुना गया: ${sample.title}`, 'info');
  };

  // Custom photo file upload
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (uploadEvent) => {
        setPhotoUrl(uploadEvent.target.result);
        setPhotoSource('upload');
        showToast('फोटो लोड हो गया!', 'success');
      };
      reader.readAsDataURL(file);
    }
  };

  // Voice recording toggle with Web Speech API
  const handleToggleRecord = () => {
    if (isRecording) {
      // Stop recording
      setIsRecording(false);
      clearInterval(timerRef.current);
      if (speechRecognitionRef.current) {
        speechRecognitionRef.current.stop();
      }
      setHasVoiceRecorded(true);
      showToast(t('recordedSuccess'), 'success');
    } else {
      // Start recording
      setIsRecording(true);
      setRecordingSeconds(0);
      timerRef.current = setInterval(() => {
        setRecordingSeconds(prev => prev + 1);
      }, 1000);

      // Web Speech API integration
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        try {
          const recognition = new SpeechRecognition();
          recognition.continuous = true;
          recognition.interimResults = true;
          recognition.lang = language === 'en' ? 'en-IN' : 'hi-IN';

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
          };

          speechRecognitionRef.current = recognition;
          recognition.start();
        } catch (e) {
          console.warn("Speech recognition start failed:", e);
        }
      }
    }
  };

  // Start AI Processing Pipeline
  const startAiProcessing = async () => {
    setCurrentStep(3);
    setAiProgress(10);
    speakText("तंतु AI आपके शिल्प का विश्लेषण कर रहा है। कृपया प्रतीक्षा करें।");

    // Initialize temporary product record
    const baseProduct = {
      title: 'Handcrafted Artisan Craft',
      image_url: photoUrl,
      artisan_id: artisanProfile.id,
      artisan_name: artisanProfile.name,
      location: artisanProfile.location
    };

    try {
      // Stage 1: Understanding Voice
      updateStage(1, 'in-progress');
      await delay(900);
      setAiProgress(30);
      updateStage(1, 'completed');

      // Stage 2: Identifying Product
      updateStage(2, 'in-progress');
      await delay(900);
      setAiProgress(50);
      updateStage(2, 'completed');

      // Stage 3: Creating Bilingual Catalogue
      updateStage(3, 'in-progress');
      const voiceProcessed = await productService.processVoice('new-draft', {
        audio_transcript: transcript,
        language: language
      });
      await delay(900);
      setAiProgress(70);
      updateStage(3, 'completed');

      // Stage 4: Enhancing Image
      updateStage(4, 'in-progress');
      const enhanced = await productService.enhanceImage('new-draft', {
        image_url: photoUrl,
        prompt: 'Clean studio backdrop with soft warm lighting'
      });
      await delay(900);
      setAiProgress(90);
      updateStage(4, 'completed');

      // Stage 5: Estimating Price
      updateStage(5, 'in-progress');
      const priced = await productService.calculatePrice('new-draft', {
        raw_material_cost: 300,
        labor_hours: 16
      });
      await delay(800);
      setAiProgress(100);
      updateStage(5, 'completed');

      // Assemble final generated product
      const finalProduct = {
        ...baseProduct,
        ...voiceProcessed,
        ...enhanced,
        ...priced,
        image_url: photoUrl,
        enhanced_image_url: enhanced.enhanced_image_url || photoUrl,
        id: `prod-${Date.now().toString(16).slice(-6)}`,
        created_at: new Date().toISOString()
      };

      setGeneratedProduct(finalProduct);
      setEditFormData(finalProduct);

      // Transition to Catalogue step
      await delay(600);
      setCurrentStep(4);
      speakText("आपका स्मार्ट कैटलॉग तैयार है! विवरण जांचें और प्रकाशित करें।");
    } catch (err) {
      console.error("AI Pipeline error:", err);
      showToast("AI विश्लेषण में त्रुटि", "error");
    }
  };

  const updateStage = (stageId, status) => {
    setAiStages(prev => prev.map(s => s.id === stageId ? { ...s, status } : s));
  };

  const delay = (ms) => new Promise(res => setTimeout(res, ms));

  // Approve & Publish Product
  const handleApproveAndPublish = async () => {
    try {
      const saved = await productService.createProduct(generatedProduct);
      refreshData();
      setCurrentStep(5);

      // Trigger celebration confetti
      try {
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 }
        });
      } catch (e) {
        // Confetti fallback
      }

      showToast(t('publishedSuccess'), 'success');
      speakText("बधाई! आपका शिल्प सफलतापूर्वक प्रकाशित हो गया है और अब खरीदारों को दिखेगा।");
    } catch (e) {
      showToast("प्रकाशित करने में त्रुटि", "error");
    }
  };

  // Save edits from modal
  const handleSaveEdit = () => {
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
      {/* Wizard Step Indicator */}
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
          STEP 1: PHOTO CAPTURE / UPLOAD
          ========================================================================= */}
      {currentStep === 1 && (
        <div>
          <div style={{ marginBottom: '18px' }}>
            <h2 className="wizard-title">{t('step1Photo')}</h2>
            <p className="wizard-sub">{t('step1PhotoSub')}</p>
          </div>

          {/* Current Photo Preview Box */}
          <div className="photo-preview-box">
            <img src={photoUrl} alt="Craft to catalog" className="photo-preview-img" />
            <div className="photo-preview-overlay">
              <span style={{ fontSize: '0.8rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '6px' }}>
                <CheckCircle2 size={16} color="#10B981" />
                <span>फोटो तैयार है</span>
              </span>
              <button
                onClick={() => fileInputRef.current && fileInputRef.current.click()}
                style={{ background: 'rgba(255, 255, 255, 0.9)', color: '#0F172A', padding: '4px 10px', borderRadius: '999px', fontSize: '0.75rem', fontWeight: 700 }}
              >
                बदलें (Change)
              </button>
            </div>
          </div>

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
            >
              <Camera size={20} color="#EA580C" />
              <span>{t('takePhoto')}</span>
            </button>

            <button
              className="btn-secondary-large"
              onClick={() => fileInputRef.current && fileInputRef.current.click()}
            >
              <Upload size={20} color="#EA580C" />
              <span>{t('uploadPhoto')}</span>
            </button>
          </div>

          {/* Or 1-Click Demo Sample Crafts */}
          <div style={{ marginBottom: '24px' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '10px' }}>
              {t('orUseSample')}
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

          {/* Continue to Voice */}
          <button
            className="btn-primary-large"
            onClick={() => {
              setCurrentStep(2);
              speakText("अब माइक दबाएं और अपने शिल्प के बारे में बोलकर बताएं।");
            }}
          >
            <span>आगे बढ़ें: आवाज़ रिकॉर्ड करें</span>
            <ArrowRight size={20} />
          </button>
        </div>
      )}

      {/* =========================================================================
          STEP 2: RECORD VOICE NARRATIVE
          ========================================================================= */}
      {currentStep === 2 && (
        <div>
          <div style={{ marginBottom: '18px' }}>
            <h2 className="wizard-title">{t('step2Voice')}</h2>
            <p className="wizard-sub">{t('step2VoiceSub')}</p>
          </div>

          {/* Voice Recorder Container */}
          <div className="voice-recorder-container">
            <div className="mic-button-wrapper">
              <button
                className={`mic-circle-btn ${isRecording ? 'recording' : ''}`}
                onClick={handleToggleRecord}
                title="Tap to record voice"
              >
                {isRecording ? <MicOff size={42} /> : <Mic size={42} />}
              </button>
              {isRecording && <div className="mic-pulse-wave" />}
            </div>

            <div style={{ fontSize: '1.15rem', fontWeight: 800, color: isRecording ? '#DC2626' : 'var(--text-main)', marginBottom: '6px' }}>
              {isRecording ? `${t('listening')} (00:${recordingSeconds < 10 ? '0' : ''}${recordingSeconds})` : t('tapToRecord')}
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-light)', maxWidth: '320px' }}>
              सामग्री, बनाने में लगा समय, और अपने परिवार की परंपरा के बारे में बताएं।
            </p>

            {/* Simulated Live Waveform */}
            {isRecording && (
              <div className="voice-waveform-visualizer" style={{ marginTop: '16px' }}>
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

            {/* Transcript Preview */}
            {transcript && (
              <div className="transcript-display-box">
                <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary-700)', textTransform: 'uppercase', marginBottom: '4px' }}>
                  पहचानी गई आवाज़ (Voice Transcript):
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

          {/* Actions */}
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              className="btn-secondary-large"
              style={{ width: '45%' }}
              onClick={() => setCurrentStep(1)}
            >
              <ArrowLeft size={18} />
              <span>वापस (Back)</span>
            </button>

            <button
              className="btn-primary-large"
              style={{ width: '55%' }}
              onClick={startAiProcessing}
            >
              <Sparkles size={18} />
              <span>{t('proceedToAi')}</span>
            </button>
          </div>
        </div>
      )}

      {/* =========================================================================
          STEP 3: AI PROCESSING SCREEN (SIH Presentation Showcase)
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
              आवाज़, भाषा और फोटो से स्मार्ट ई-कॉमर्स कैटलॉग निर्मित हो रहा है
            </p>
          </div>

          {/* Progress Bar */}
          <div style={{ marginBottom: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94A3B8', marginBottom: '6px' }}>
              <span>प्रगति (Progress)</span>
              <span>{aiProgress}%</span>
            </div>
            <div className="ai-overall-progress-bar">
              <div className="ai-progress-fill" style={{ width: `${aiProgress}%` }} />
            </div>
          </div>

          {/* Stage List */}
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
                    <div className="stage-title">{stage.name}</div>
                    <div className="stage-desc">{stage.desc}</div>
                  </div>
                  {isDone && (
                    <span style={{ fontSize: '0.7rem', color: '#10B981', fontWeight: 700 }}>सफल ✓</span>
                  )}
                </div>
              );
            })}
          </div>

          <div style={{ textAlign: 'center', fontSize: '0.75rem', color: '#64748B' }}>
            Powered by Voice NLP (Member M) • Vision Studio (Member R) • Smart Pricing (Member S)
          </div>
        </div>
      )}

      {/* =========================================================================
          STEP 4: SMART CATALOGUE PREVIEW & EDIT
          ========================================================================= */}
      {currentStep === 4 && generatedProduct && (
        <div>
          <div style={{ marginBottom: '16px' }}>
            <h2 className="wizard-title">{t('step4Catalog')}</h2>
            <p className="wizard-sub">{t('step4CatalogSub')}</p>
          </div>

          {/* Catalogue Card */}
          <div className="catalog-display-card">
            {/* Before vs After Image Toggle */}
            <div className="comparison-toggle-bar">
              <button
                className={`toggle-btn ${viewEnhanced ? 'active' : ''}`}
                onClick={() => setViewEnhanced(true)}
              >
                <Sparkles size={14} color="#EA580C" />
                <span>{t('viewEnhanced')}</span>
              </button>
              <button
                className={`toggle-btn ${!viewEnhanced ? 'active' : ''}`}
                onClick={() => setViewEnhanced(false)}
              >
                <ImageIcon size={14} />
                <span>{t('viewOriginal')}</span>
              </button>
            </div>

            <div className="product-img-wrapper" style={{ height: '250px' }}>
              <img
                src={viewEnhanced ? generatedProduct.enhanced_image_url : generatedProduct.image_url}
                alt={generatedProduct.title}
                className="product-img"
              />
              <span className="badge-ai-enhanced">
                <Sparkles size={12} />
                <span>{viewEnhanced ? 'AI Studio Lighting' : 'Original Capture'}</span>
              </span>
              <span className="badge-category">{generatedProduct.category}</span>
            </div>

            <div className="catalog-body">
              <h3 className="catalog-title">{generatedProduct.title}</h3>
              {generatedProduct.description_hindi && (
                <p className="catalog-hindi-title">
                  {generatedProduct.description_hindi}
                </p>
              )}

              {/* Spec Pills */}
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
                      style={{
                        background: '#F1F5F9',
                        color: '#475569',
                        padding: '3px 8px',
                        borderRadius: '6px',
                        fontSize: '0.72rem',
                        fontWeight: 600
                      }}
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}

              {/* Heritage Story Box */}
              <div className="catalog-story-box">
                <div className="story-heading">
                  <Heart size={14} color="#D97706" />
                  <span>{t('heritageStory')} ({generatedProduct.narrative_type || 'Cultural Heritage'})</span>
                </div>
                <p className="story-text">"{generatedProduct.story}"</p>
                <div style={{ marginTop: '8px', fontSize: '0.75rem', color: '#92400E', fontWeight: 600 }}>
                  संवेदना: {generatedProduct.sentiment || 'Warm, authentic'}
                </div>
              </div>

              {/* Suggested Price Highlight */}
              <div className="pricing-highlight-box">
                <div>
                  <div className="pricing-title">{t('suggestedPrice')}</div>
                  <div style={{ fontSize: '0.72rem', color: '#065F46' }}>
                    सामग्री और {generatedProduct.production_time || 'श्रम'} के आधार पर
                  </div>
                </div>
                <div className="pricing-range">
                  ₹{generatedProduct.suggested_price_min} - ₹{generatedProduct.suggested_price_max}
                </div>
              </div>

              {/* Primary Action Buttons */}
              <button
                className="btn-primary-large"
                onClick={handleApproveAndPublish}
              >
                <Check size={22} strokeWidth={2.8} />
                <span>{t('approvePublish')}</span>
              </button>

              <button
                className="btn-secondary-large"
                onClick={() => setIsEditModalOpen(true)}
              >
                <Edit3 size={18} />
                <span>{t('editDetails')}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* =========================================================================
          STEP 5: PUBLISHED CELEBRATION
          ========================================================================= */}
      {currentStep === 5 && (
        <div style={{ textAlign: 'center', padding: '36px 16px' }}>
          <div
            style={{
              width: '80px',
              height: '80px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
              color: '#FFFFFF',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 10px 25px rgba(16, 185, 129, 0.4)',
              marginBottom: '20px'
            }}
          >
            <Check size={42} strokeWidth={3} />
          </div>

          <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--text-main)', marginBottom: '8px' }}>
            बधाई हो! शिल्प प्रकाशित हुआ
          </h2>
          <p style={{ fontSize: '0.92rem', color: 'var(--text-muted)', lineHeight: '1.5', maxWidth: '340px', margin: '0 auto 28px auto' }}>
            {t('publishedSuccess')}
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
              // Reset wizard
              setCurrentStep(1);
              setTranscript('');
              setGeneratedProduct(null);
            }}
          >
            <span>+ एक और नया शिल्प जोड़ें</span>
          </button>
        </div>
      )}

      {/* =========================================================================
          EDIT CATALOGUE MODAL
          ========================================================================= */}
      {isEditModalOpen && (
        <div className="modal-backdrop" onClick={() => setIsEditModalOpen(false)}>
          <div className="modal-content-sheet" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header-row">
              <h3 className="modal-title">कैटलॉग में सुधार करें</h3>
              <button className="modal-close-btn" onClick={() => setIsEditModalOpen(false)}>✕</button>
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
                  हिन्दी विवरण (Hindi Description)
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

              <div>
                <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>
                  शिल्पकार की कहानी (Artisan Story)
                </label>
                <textarea
                  rows={3}
                  value={editFormData.story || ''}
                  onChange={(e) => setEditFormData({ ...editFormData, story: e.target.value })}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '12px', border: '1.5px solid var(--border-light)' }}
                />
              </div>

              <button
                className="btn-primary-large"
                onClick={handleSaveEdit}
                style={{ marginTop: '10px' }}
              >
                <span>बदलाव सहेजें (Save Changes)</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
