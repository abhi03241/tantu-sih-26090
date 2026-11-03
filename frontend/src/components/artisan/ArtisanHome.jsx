import React from 'react';
import { useApp } from '../../context/AppContext';
import { Sparkles, Mic, MapPin, Volume2, ArrowRight, ChevronRight, Inbox } from 'lucide-react';

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
      {/* Artisan greeting card */}
      <div className="artisan-hero-card">
        <div className="artisan-avatar-row">
          <div className="artisan-profile-badge">
            <img src={artisanProfile.avatar} alt={artisanProfile.name} className="artisan-img" />
            <div>
              <div className="artisan-name">{artisanProfile.name}</div>
              <div className="artisan-location">
                <MapPin size={13} />
                <span>{artisanProfile.location}</span>
              </div>
            </div>
          </div>
          <button
            type="button"
            className="tts-speaker-btn"
            onClick={handleReadGuide}
            title="Read summary aloud"
          >
            <Volume2 size={15} />
            <span>सुनें</span>
          </button>
        </div>

        {artisanProfile.craft && (
          <span className="vk-tag vk-tag-gold">{artisanProfile.craft}</span>
        )}

        <p className="ah-welcome">
          {t('welcomeBack')}
        </p>
      </div>

      {/* Main call to action: add a product with voice & photo */}
      <div
        className="big-action-card"
        onClick={() => navigateTo('add-wizard')}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            navigateTo('add-wizard');
          }
        }}
        role="button"
        tabIndex={0}
      >
        <div className="big-action-icon-circle">
          <Mic size={30} />
        </div>
        <h2 className="big-action-title">
          {t('addNewCraft')}
        </h2>
        <p className="big-action-sub">
          {t('addNewCraftSub')}
        </p>
        <div className="big-action-btn-pill">
          <Sparkles size={18} />
          <span>{t('startNow')}</span>
          <ArrowRight size={18} />
        </div>
      </div>

      {/* Metrics */}
      <div className="metrics-row">
        <div className="metric-card is-clickable" onClick={() => navigateTo('my-products')}>
          <div className="metric-value">{myProducts.length}</div>
          <div className="metric-label">{t('totalProducts')}</div>
        </div>

        <div className="metric-card is-clickable" onClick={() => navigateTo('orders')}>
          <div className={`metric-value ${pendingOrders.length > 0 ? 'is-alert' : ''}`}>
            {pendingOrders.length}
          </div>
          <div className="metric-label">{t('activeOrders')}</div>
        </div>

        <div className="metric-card">
          <div className="metric-value is-money">
            ₹{(totalEarningsEst || 45000).toLocaleString('en-IN')}
          </div>
          <div className="metric-label">{t('estEarnings')}</div>
        </div>
      </div>

      {/* New order alert */}
      {pendingOrders.length > 0 && (
        <button
          type="button"
          className="ah-alert"
          onClick={() => navigateTo('orders')}
        >
          <span className="ah-alert-main">
            <span className="ah-alert-icon">
              <Inbox size={20} />
            </span>
            <span>
              <span className="ah-alert-title">
                {pendingOrders.length} नया थोक ऑर्डर अनुरोध आया है!
              </span>
              <span className="ah-alert-sub">
                {pendingOrders[0].buyer_name} ({pendingOrders[0].quantity} इकाइयाँ)
              </span>
            </span>
          </span>
          <ChevronRight size={18} />
        </button>
      )}

      {/* Recent uploads */}
      <div className="section-header-row">
        <h3 className="section-title">{t('recentUploads')}</h3>
        <button type="button" className="section-link" onClick={() => navigateTo('my-products')}>
          {t('viewAll')} ({myProducts.length})
        </button>
      </div>

      <div className="ah-list">
        {myProducts.slice(0, 3).map((product) => (
          <div
            key={product.id}
            className="ah-item"
            role="button"
            tabIndex={0}
            onClick={() => navigateTo('product-detail', product.id)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                navigateTo('product-detail', product.id);
              }
            }}
          >
            <img
              src={product.enhanced_image_url || product.image_url}
              alt={product.title}
            />

            <div className="ah-item-body">
              {product.category && (
                <span className="vk-eyebrow ah-item-cat">{product.category}</span>
              )}
              <h4 className="ah-item-title">{product.title}</h4>
              {product.description_hindi && (
                <p className="ah-item-hindi">{product.description_hindi}</p>
              )}

              <div className="ah-item-foot">
                <div className="price-tag-wrap">
                  <span className="price-label">{t('suggestedPrice')}</span>
                  <span className="ah-item-price">
                    ₹{product.suggested_price_min || 650} - ₹{product.suggested_price_max || 950}
                  </span>
                </div>
                <span className="btn-card-action">
                  <span>विवरण देखें</span>
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}