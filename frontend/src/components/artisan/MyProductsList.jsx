import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { CRAFT_CATEGORIES } from '../../constants/categories';
import { Sparkles, Plus, Search, Filter, Layers, ChevronRight, CheckCircle2, Clock, FileText, AlertCircle } from 'lucide-react';

export default function MyProductsList() {
  const { products, artisanProfile, navigateTo, t } = useApp();
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all'); // 'all' | 'published' | 'draft' | 'ready'
  const [searchQuery, setSearchQuery] = useState('');

  const myProducts = products.filter(p => !p.artisan_id || p.artisan_id === artisanProfile.id);

  const filtered = myProducts.filter(p => {
    const pStatus = (p.status || 'published').toLowerCase();
    const matchesCat = selectedCategory === 'all' || p.category?.toLowerCase() === selectedCategory.toLowerCase();
    const matchesStatus = selectedStatus === 'all' || pStatus === selectedStatus.toLowerCase();
    const matchesSearch = !searchQuery ||
      p.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.description_english?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.description_hindi?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.material?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesStatus && matchesSearch;
  });

  const getStatusBadge = (status = 'published') => {
    switch (status.toLowerCase()) {
      case 'published':
        return { label: 'प्रकाशित (Live)', bg: '#D1FAE5', color: '#065F46', icon: <CheckCircle2 size={12} /> };
      case 'ready':
        return { label: 'तैयार (Ready)', bg: '#E0E7FF', color: '#3730A3', icon: <Sparkles size={12} /> };
      case 'draft':
        return { label: 'ड्राफ्ट (Draft)', bg: '#FEF3C7', color: '#92400E', icon: <FileText size={12} /> };
      case 'processing':
        return { label: 'प्रसंस्करण', bg: '#FFEDD5', color: '#C2410C', icon: <Clock size={12} /> };
      case 'failed':
        return { label: 'त्रुटि', bg: '#FEE2E2', color: '#991B1B', icon: <AlertCircle size={12} /> };
      default:
        return { label: 'सक्रिय', bg: '#D1FAE5', color: '#065F46', icon: <CheckCircle2 size={12} /> };
    }
  };

  const statusPills = [
    { id: 'all', label: `सभी (${myProducts.length})` },
    { id: 'published', label: `प्रकाशित (${myProducts.filter(p => (p.status || 'published') === 'published').length})` },
    { id: 'ready', label: `तैयार (${myProducts.filter(p => p.status === 'ready').length})` },
    { id: 'draft', label: `ड्राफ्ट (${myProducts.filter(p => p.status === 'draft').length})` }
  ];

  return (
    <div>
      <div className="section-header-row" style={{ marginBottom: '16px' }}>
        <div>
          <h2 className="section-title" style={{ fontSize: '1.4rem' }}>{t('myProducts')}</h2>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            कुल {myProducts.length} हस्तनिर्मित शिल्प कैटलॉग में हैं
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

      {/* Search Input */}
      <div className="search-bar-wrapper">
        <Search size={18} className="search-icon-pos" />
        <input
          type="text"
          className="search-input"
          placeholder="शिल्प, सामग्री या श्रेणी खोजें..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Status Filter Tabs (Checkpoint 7) */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '14px', overflowX: 'auto', paddingBottom: '4px', scrollbarWidth: 'none' }}>
        {statusPills.map((st) => (
          <button
            key={st.id}
            onClick={() => setSelectedStatus(st.id)}
            style={{
              padding: '6px 14px',
              borderRadius: '999px',
              fontSize: '0.78rem',
              fontWeight: 700,
              whiteSpace: 'nowrap',
              background: selectedStatus === st.id ? 'var(--royal-indigo)' : '#FFFFFF',
              color: selectedStatus === st.id ? '#FFFFFF' : 'var(--text-muted)',
              border: selectedStatus === st.id ? '1px solid var(--royal-indigo)' : '1px solid var(--border-light)'
            }}
          >
            {st.label}
          </button>
        ))}
      </div>

      {/* Craft Category Scroll */}
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
            चयनित फिल्टर के लिए कोई शिल्प उपलब्ध नहीं है।
          </p>
          <button className="btn-primary-large" onClick={() => navigateTo('add-wizard')}>
            <Plus size={18} />
            <span>नया शिल्प जोड़ें</span>
          </button>
        </div>
      ) : (
        <div className="products-grid">
          {filtered.map((product) => {
            const badge = getStatusBadge(product.status);
            return (
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
                  <span
                    style={{
                      position: 'absolute',
                      top: 12,
                      left: 12,
                      background: badge.bg,
                      color: badge.color,
                      padding: '4px 10px',
                      borderRadius: '999px',
                      fontSize: '0.72rem',
                      fontWeight: 700,
                      display: 'flex',
                      alignItems: 'center',
                      gap: '4px',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                    }}
                  >
                    {badge.icon}
                    <span>{badge.label}</span>
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
                      <span>खोलें</span>
                      <ChevronRight size={16} />
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
