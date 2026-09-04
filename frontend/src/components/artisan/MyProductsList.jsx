import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { CRAFT_CATEGORIES } from '../../constants/categories';
import { Sparkles, Plus, Search, Filter, Layers, ChevronRight, Eye } from 'lucide-react';

export default function MyProductsList() {
  const { products, artisanProfile, navigateTo, t } = useApp();
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const myProducts = products.filter(p => !p.artisan_id || p.artisan_id === artisanProfile.id);

  const filtered = myProducts.filter(p => {
    const matchesCat = selectedCategory === 'all' || p.category?.toLowerCase() === selectedCategory.toLowerCase();
    const matchesSearch = !searchQuery ||
      p.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.description_english?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.description_hindi?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.material?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesSearch;
  });

  return (
    <div>
      <div className="section-header-row" style={{ marginBottom: '16px' }}>
        <div>
          <h2 className="section-title" style={{ fontSize: '1.4rem' }}>{t('myProducts')}</h2>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            कुल {myProducts.length} शिल्प कैटलॉग में प्रकाशित हैं
          </p>
        </div>

        <button
          onClick={() => navigateTo('add-wizard')}
          className="pill-btn"
          style={{ background: 'var(--terracotta)', color: '#FFFFFF', borderColor: 'var(--terracotta)', padding: '8px 14px' }}
        >
          <Plus size={16} strokeWidth={3} />
          <span>नया जोड़ें</span>
        </button>
      </div>

      {/* Search Bar */}
      <div className="search-bar-wrapper">
        <Search size={18} className="search-icon-pos" />
        <input
          type="text"
          className="search-input"
          placeholder="शिल्प या सामग्री खोजें..."
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
            <span>{cat.nameHi}</span>
          </button>
        ))}
      </div>

      {/* Products Grid */}
      {filtered.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px 16px', background: '#FFFFFF', borderRadius: '20px', border: '1px solid var(--border-light)' }}>
          <div style={{ width: 50, height: 50, borderRadius: '50%', background: 'var(--primary-50)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary-600)', marginBottom: '12px' }}>
            <Layers size={24} />
          </div>
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '6px' }}>कोई शिल्प नहीं मिला</h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
            अपने हस्तनिर्मित उत्पाद को कैटलॉग करने के लिए नीचे बटन दबाएं
          </p>
          <button className="btn-primary-large" onClick={() => navigateTo('add-wizard')}>
            <Plus size={18} />
            <span>पहला शिल्प जोड़ें</span>
          </button>
        </div>
      ) : (
        <div className="products-grid">
          {filtered.map((product) => (
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
                      ₹{product.suggested_price_min} - ₹{product.suggested_price_max}
                    </span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--primary-700)', fontWeight: 700, fontSize: '0.82rem' }}>
                    <span>विवरण</span>
                    <ChevronRight size={16} />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
