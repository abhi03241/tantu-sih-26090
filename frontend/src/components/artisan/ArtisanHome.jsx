import React from 'react';
import { useApp } from '../../context/AppContext';
import { Sparkles, Plus, MapPin, Volume2, ArrowRight, Eye, CheckCircle2, ChevronRight, Package, Inbox } from 'lucide-react';

export default function ArtisanHome() {
  const { artisanProfile, products, orders, navigateTo, speakText, t } = useApp();

  const myProducts = products.filter(p => !p.artisan_id || p.artisan_id === artisanProfile.id);
  const myOrders = orders.filter(o => !o.artisan_id || o.artisan_id === artisanProfile.id);
  const pendingOrders = myOrders.filter(o => o.status === 'pending');

  const totalEarningsEst = myOrders
    .filter(o => o.status === 'accepted')
    .reduce((sum, o) => sum + (o.quantity * (o.price_offered || 800)), 0);

  const handleReadGuide = () => {
    speakText(`नमस्ते ${artisanProfile.name} जी! आपके पास ${myProducts.length} शिल्प कैटलॉग में हैं, और ${pendingOrders.length} नए खरीदार अनुरोध आए हुए हैं। नया शिल्प जोड़ने के लिए बड़ा नारंगी बटन दबाएं।`);
  };

  return (
    <div>
      {/* Artisan Hero Banner */}
      <div className="artisan-hero-card">
        <div className="artisan-avatar-row">
          <div className="artisan-profile-badge">
            <img src={artisanProfile.avatar} alt={artisanProfile.name} className="artisan-img" />
            <div>
              <div className="artisan-name">{artisanProfile.name}</div>
              <div className="artisan-location">
                <MapPin size={13} color="#EA580C" />
                <span>{artisanProfile.location}</span>
              </div>
            </div>
          </div>
          <button
            className="tts-speaker-btn"
            onClick={handleReadGuide}
            title="Read summary aloud"
          >
            <Volume2 size={15} />
            <span>सुनें</span>
          </button>
        </div>

        <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', lineHeight: '1.45', marginTop: '4px' }}>
          {t('welcomeBack')}
        </p>
      </div>

      {/* Giant CTA: Add Product via Voice & Photo */}
      <div
        className="big-action-card"
        onClick={() => navigateTo('add-wizard')}
        role="button"
        tabIndex={0}
      >
        <div className="big-action-icon-circle">
          <Plus size={36} strokeWidth={3} />
        </div>
        <h2 className="big-action-title">
          {t('addNewCraft')}
        </h2>
        <p className="big-action-sub">
          {t('addNewCraftSub')}
        </p>
        <div className="big-action-btn-pill">
          <Sparkles size={18} color="#C84B20" />
          <span>{t('startNow')}</span>
          <ArrowRight size={18} />
        </div>
      </div>

      {/* Metrics Row */}
      <div className="metrics-row">
        <div className="metric-card" onClick={() => navigateTo('my-products')} style={{ cursor: 'pointer' }}>
          <div className="metric-value">{myProducts.length}</div>
          <div className="metric-label">{t('totalProducts')}</div>
        </div>

        <div className="metric-card" onClick={() => navigateTo('orders')} style={{ cursor: 'pointer' }}>
          <div className="metric-value" style={{ color: pendingOrders.length > 0 ? '#EA580C' : 'var(--text-main)' }}>
            {pendingOrders.length}
          </div>
          <div className="metric-label">{t('activeOrders')}</div>
        </div>

        <div className="metric-card">
          <div className="metric-value" style={{ color: '#059669', fontSize: '1.15rem' }}>
            ₹{(totalEarningsEst || 45000).toLocaleString('en-IN')}
          </div>
          <div className="metric-label">{t('estEarnings')}</div>
        </div>
      </div>

      {/* Order Inquiries Alert if any */}
      {pendingOrders.length > 0 && (
        <div
          onClick={() => navigateTo('orders')}
          style={{
            background: 'linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%)',
            border: '1.5px solid #F59E0B',
            borderRadius: '16px',
            padding: '14px 16px',
            marginBottom: '22px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: 'pointer'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: '#F59E0B', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#FFFFFF' }}>
              <Inbox size={20} />
            </div>
            <div>
              <div style={{ fontSize: '0.92rem', fontWeight: 800, color: '#92400E' }}>
                {pendingOrders.length} नया थोक ऑर्डर अनुरोध आया है!
              </div>
              <div style={{ fontSize: '0.78rem', color: '#B45309' }}>
                {pendingOrders[0].buyer_name} ({pendingOrders[0].quantity} इकाइयाँ)
              </div>
            </div>
          </div>
          <ChevronRight size={18} color="#92400E" />
        </div>
      )}

      {/* Recent Uploads Section */}
      <div className="section-header-row">
        <h3 className="section-title">{t('recentUploads')}</h3>
        <button className="section-link" onClick={() => navigateTo('my-products')}>
          {t('viewAll')} ({myProducts.length})
        </button>
      </div>

      <div className="products-grid">
        {myProducts.slice(0, 3).map((product) => (
          <div
            key={product.id}
            className="artisan-product-card"
            onClick={() => navigateTo('product-detail', product.id)}
          >
            <div className="product-img-wrapper">
              <img
                src={product.enhanced_image_url || product.image_url}
                alt={product.title}
                className="product-img"
              />
              <span className="badge-ai-enhanced">
                <Sparkles size={12} />
                <span>AI Enhanced</span>
              </span>
              <span className="badge-category">{product.category}</span>
            </div>

            <div className="product-card-body">
              <h4 className="product-card-title">{product.title}</h4>
              {product.description_hindi && (
                <p className="product-card-hindi">{product.description_hindi}</p>
              )}

              <div className="product-card-footer">
                <div className="price-tag-wrap">
                  <span className="price-label">{t('suggestedPrice')}</span>
                  <span className="price-value">
                    ₹{product.suggested_price_min || 650} - ₹{product.suggested_price_max || 950}
                  </span>
                </div>
                <button className="btn-card-action">
                  <span>विवरण देखें</span>
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
