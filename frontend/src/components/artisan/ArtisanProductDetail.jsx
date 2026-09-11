import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import {
  ArrowLeft, Sparkles, Image as ImageIcon, Volume2, Heart,
  Layers, Ruler, Clock, Tag, MapPin, Share2, ShoppingBag, CheckCircle
} from 'lucide-react';

export default function ArtisanProductDetail({ productId, onBack }) {
  const { products, orders, navigateTo, switchRole, speakText, showToast, t } = useApp();
  const [viewEnhanced, setViewEnhanced] = useState(true);

  const product = products.find(p => p.id === productId) || products[0];
  const relatedOrders = orders.filter(o => o.product_id === product?.id);

  if (!product) {
    return (
      <div style={{ padding: '30px 16px', textAlign: 'center' }}>
        <p>उत्पाद नहीं मिला</p>
        <button className="btn-primary-large" onClick={onBack}>वापस जाएं</button>
      </div>
    );
  }

  const handleReadAloud = () => {
    speakText(`${product.title}। ${product.description_hindi || product.description_english}। सामग्री: ${product.material}। अनुमानित मूल्य ₹${product.suggested_price_min} से ₹${product.suggested_price_max}।`);
  };

  const handleShare = () => {
    navigator.clipboard?.writeText(window.location.href);
    showToast("कैटलॉग लिंक कॉपी कर लिया गया है!", "success");
  };

  return (
    <div>
      {/* Top Bar with Back Button */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <button
          onClick={onBack}
          style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.88rem', fontWeight: 700, color: 'var(--text-main)' }}
        >
          <ArrowLeft size={20} />
          <span>वापस (Back)</span>
        </button>

        <div style={{ display: 'flex', gap: '8px' }}>
          <button className="pill-btn" onClick={handleReadAloud} title="Read details aloud">
            <Volume2 size={16} />
            <span>सुनें</span>
          </button>
          <button className="pill-btn" onClick={handleShare} title="Share craft link">
            <Share2 size={16} />
          </button>
        </div>
      </div>

      {/* Catalog Display Card */}
      <div className="catalog-display-card">
        {/* Before vs After comparison slider */}
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

        <div className="product-img-wrapper" style={{ height: '260px' }}>
          <img
            src={viewEnhanced ? (product.enhanced_image_url || product.image_url) : product.image_url}
            alt={product.title}
            className="product-img"
          />
          <span className="badge-ai-enhanced">
            <Sparkles size={12} />
            <span>{viewEnhanced ? 'AI Studio Enhanced' : 'Original Raw'}</span>
          </span>
          <span className="badge-category">{product.category}</span>
        </div>

        <div className="catalog-body">
          <h2 className="catalog-title">{product.title}</h2>
          {product.description_hindi && (
            <p className="catalog-hindi-title">{product.description_hindi}</p>
          )}

          <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: '1.5', marginBottom: '18px' }}>
            {product.description_english}
          </p>

          {/* Specs Row */}
          <div className="spec-pills-row">
            <span className="spec-pill">
              <Layers size={13} color="#EA580C" />
              <span>{product.material}</span>
            </span>
            <span className="spec-pill">
              <Ruler size={13} color="#EA580C" />
              <span>{product.dimensions || '30cm x 30cm'}</span>
            </span>
            <span className="spec-pill">
              <Clock size={13} color="#EA580C" />
              <span>{product.production_time || '3 days'}</span>
            </span>
          </div>

          {/* Tags */}
          {product.tags && product.tags.length > 0 && (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '18px' }}>
              {product.tags.map((tag, i) => (
                <span
                  key={i}
                  style={{
                    background: '#F1F5F9',
                    color: '#475569',
                    padding: '4px 10px',
                    borderRadius: '8px',
                    fontSize: '0.74rem',
                    fontWeight: 600
                  }}
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}

          {/* Heritage Story & Sentiment */}
          <div className="catalog-story-box">
            <div className="story-heading">
              <Heart size={14} color="#D97706" />
              <span>{t('heritageStory')}</span>
            </div>
            <p className="story-text">"{product.story}"</p>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px', fontSize: '0.75rem', color: '#92400E', fontWeight: 600 }}>
              <span>शैली: {product.narrative_type || 'Cultural Heritage'}</span>
              <span>संवेदना: {product.sentiment || 'Warm, authentic'}</span>
            </div>
          </div>

          {/* Fair Pricing Highlight */}
          <div className="pricing-highlight-box">
            <div>
              <div className="pricing-title">{t('suggestedPrice')}</div>
              <div style={{ fontSize: '0.75rem', color: '#065F46' }}>
                पारदर्शी व उचित कारीगर दर
              </div>
            </div>
            <div className="pricing-range">
              ₹{product.suggested_price_min} - ₹{product.suggested_price_max}
            </div>
          </div>

          {/* Orders Received for this item */}
          <div style={{ marginTop: '22px', borderTop: '1px solid var(--border-light)', paddingTop: '16px' }}>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '10px' }}>
              इस शिल्प के थोक ऑर्डर ({relatedOrders.length})
            </h4>

            {relatedOrders.length === 0 ? (
              <p style={{ fontSize: '0.82rem', color: 'var(--text-light)' }}>
                अभी तक कोई नया ऑर्डर नहीं आया है। बाज़ार में यह शिल्प प्रदर्शित है।
              </p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {relatedOrders.map((ord) => (
                  <div
                    key={ord.id}
                    style={{
                      background: 'var(--primary-50)',
                      border: '1px solid var(--primary-200)',
                      borderRadius: '12px',
                      padding: '10px 14px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between'
                    }}
                  >
                    <div>
                      <div style={{ fontSize: '0.85rem', fontWeight: 700 }}>{ord.buyer_name}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        {ord.quantity} इकाइयाँ @ ₹{ord.price_offered}
                      </div>
                    </div>
                    <span
                      style={{
                        fontSize: '0.72rem',
                        fontWeight: 700,
                        padding: '3px 8px',
                        borderRadius: '999px',
                        background: ord.status === 'accepted' ? '#D1FAE5' : '#FEF3C7',
                        color: ord.status === 'accepted' ? '#065F46' : '#92400E'
                      }}
                    >
                      {ord.status === 'accepted' ? 'स्वीकृत' : 'लंबित'}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Switch to Buyer View for testing */}
          <button
            className="btn-secondary-large"
            style={{ marginTop: '20px' }}
            onClick={() => {
              switchRole('buyer');
              navigateTo('buyer-product-detail', product.id);
            }}
          >
            <ShoppingBag size={18} color="#EA580C" />
            <span>खरीदार के रूप में देखें (View as Buyer)</span>
          </button>
        </div>
      </div>
    </div>
  );
}
