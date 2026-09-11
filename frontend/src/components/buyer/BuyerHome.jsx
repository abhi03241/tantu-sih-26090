import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { CRAFT_CATEGORIES } from '../../constants/categories';
import { Search, Sparkles, MapPin, ShoppingBag, ArrowRight, ShieldCheck } from 'lucide-react';

export default function BuyerHome() {
  const { products, navigateTo, t } = useApp();
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const filtered = products.filter(p => {
    const isPublished = (p.status || 'published').toLowerCase() === 'published';
    const matchesCat = selectedCategory === 'all' || p.category?.toLowerCase() === selectedCategory.toLowerCase();
    const matchesSearch = !searchQuery ||
      p.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.description_english?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.description_hindi?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.material?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.artisan_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.location?.toLowerCase().includes(searchQuery.toLowerCase());
    return isPublished && matchesCat && matchesSearch;
  });

  return (
    <div>
      {/* Buyer Marketplace Hero */}
      <div className="buyer-hero-banner">
        <div className="buyer-badge">
          <ShieldCheck size={14} />
          <span>{t('buyerHeroBadge')}</span>
        </div>
        <h2 className="buyer-hero-title">
          {t('buyerHeroTitle')}
        </h2>
        <p className="buyer-hero-sub">
          {t('buyerHeroSub')}
        </p>
      </div>

      {/* Search Input */}
      <div className="search-bar-wrapper">
        <Search size={18} className="search-icon-pos" />
        <input
          type="text"
          className="search-input"
          placeholder={t('buyerSearchPlaceholder')}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Category Pills */}
      <div className="category-filter-scroll">
        {CRAFT_CATEGORIES.map((cat) => (
          <button
            key={cat.id}
            className={`category-chip ${selectedCategory === cat.id ? 'active' : ''}`}
            onClick={() => setSelectedCategory(cat.id)}
          >
            <span>{cat.nameEn}</span>
          </button>
        ))}
      </div>

      {/* Products Grid */}
      <div className="section-header-row">
        <h3 className="section-title">{t('buyerCataloguesLabel')} ({filtered.length})</h3>
        <span style={{ fontSize: '0.78rem', color: 'var(--text-light)', fontWeight: 600 }}>
          {t('buyerB2BLabel')}
        </span>
      </div>

      {filtered.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px 16px', background: '#FFFFFF', borderRadius: '20px', border: '1px solid var(--border-light)' }}>
          <ShoppingBag size={40} color="#94A3B8" style={{ marginBottom: '10px' }} />
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '6px' }}>{t('buyerNoResults')}</h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            {t('buyerNoResultsSub')}
          </p>
        </div>
      ) : (
        <div className="products-grid">
          {filtered.map((product) => (
            <div
              key={product.id}
              className="artisan-product-card"
              onClick={() => navigateTo('buyer-product-detail', product.id)}
            >
              <div className="product-img-wrapper">
                <img
                  src={product.enhanced_image_url || product.image_url}
                  alt={product.title}
                  className="product-img"
                />
                <span className="badge-ai-enhanced">
                  <Sparkles size={12} />
                  <span>AI Studio Lighting</span>
                </span>
                <span className="badge-category">{product.category}</span>
              </div>

              <div className="product-card-body">
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.78rem', color: 'var(--text-light)', marginBottom: '4px' }}>
                  <MapPin size={13} color="#EA580C" />
                  <span>{product.artisan_name || 'Artisan'} • {product.location || 'India'}</span>
                </div>

                <h4 className="product-card-title">{product.title}</h4>

                <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', lineHeight: '1.4', marginBottom: '12px', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                  {product.description_english}
                </p>

                <div className="product-card-footer">
                  <div className="price-tag-wrap">
                    <span className="price-label">{t('buyerSuggestedWholesale')}</span>
                    <span className="price-value">
                      ₹{product.suggested_price_min} - ₹{product.suggested_price_max}
                    </span>
                  </div>

                  <button
                    className="pill-btn"
                    style={{ background: 'var(--indigo-dark)', color: '#FFFFFF', borderColor: 'var(--indigo-dark)', fontWeight: 700 }}
                  >
                    <span>{t('buyerRequestBulk')}</span>
                    <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
