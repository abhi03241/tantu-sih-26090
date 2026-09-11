import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import BulkOrderModal from './BulkOrderModal';
import {
  ArrowLeft, Sparkles, Image as ImageIcon, Heart, Layers,
  Ruler, Clock, MapPin, ShieldCheck, Share2, ShoppingBag, Check
} from 'lucide-react';

export default function BuyerProductDetail({ productId, onBack }) {
  const { products, showToast } = useApp();
  const [viewEnhanced, setViewEnhanced] = useState(true);
  const [isBulkModalOpen, setIsBulkModalOpen] = useState(false);

  const product = products.find(p => p.id === productId) || products[0];

  if (!product) {
    return (
      <div style={{ padding: '30px 16px', textAlign: 'center' }}>
        <p>Product not found.</p>
        <button className="btn-primary-large" onClick={onBack}>Go Back</button>
      </div>
    );
  }

  const handleShare = () => {
    navigator.clipboard?.writeText(window.location.href);
    showToast("Product link copied to clipboard!", "success");
  };

  return (
    <div>
      {/* Top Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <button
          onClick={onBack}
          style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.88rem', fontWeight: 700, color: 'var(--text-main)' }}
        >
          <ArrowLeft size={20} />
          <span>Back to Marketplace</span>
        </button>

        <button className="pill-btn" onClick={handleShare}>
          <Share2 size={16} />
          <span>Share</span>
        </button>
      </div>

      {/* Main Product Card */}
      <div className="catalog-display-card">
        {/* Studio Lighting Toggle */}
        <div className="comparison-toggle-bar">
          <button
            className={`toggle-btn ${viewEnhanced ? 'active' : ''}`}
            onClick={() => setViewEnhanced(true)}
          >
            <Sparkles size={14} color="#EA580C" />
            <span>AI Studio Lighting</span>
          </button>
          <button
            className={`toggle-btn ${!viewEnhanced ? 'active' : ''}`}
            onClick={() => setViewEnhanced(false)}
          >
            <ImageIcon size={14} />
            <span>Raw Capture</span>
          </button>
        </div>

        <div className="product-img-wrapper" style={{ height: '280px' }}>
          <img
            src={viewEnhanced ? (product.enhanced_image_url || product.image_url) : product.image_url}
            alt={product.title}
            className="product-img"
          />
          <span className="badge-ai-enhanced">
            <Sparkles size={12} />
            <span>{viewEnhanced ? 'Enhanced by ShilpVani AI' : 'Original Photo'}</span>
          </span>
          <span className="badge-category">{product.category}</span>
        </div>

        <div className="catalog-body">
          {/* Artisan Provenance Card */}
          <div
            style={{
              background: 'linear-gradient(135deg, #FFF7ED 0%, #FEF3C7 100%)',
              border: '1px solid #FED7AA',
              borderRadius: '16px',
              padding: '12px 14px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '16px'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--terracotta)', color: '#FFFFFF', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800 }}>
                {product.artisan_name ? product.artisan_name[0] : 'A'}
              </div>
              <div>
                <div style={{ fontSize: '0.9rem', fontWeight: 800, color: 'var(--text-main)' }}>
                  {product.artisan_name || 'Artisan Lakshmi Devi'}
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                  <MapPin size={12} color="#EA580C" />
                  <span>{product.location || 'Silchar, Assam'}</span>
                </div>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.72rem', fontWeight: 700, color: '#059669', background: '#D1FAE5', padding: '4px 8px', borderRadius: '999px' }}>
              <ShieldCheck size={13} />
              <span>Verified Artisan</span>
            </div>
          </div>

          <h2 className="catalog-title">{product.title}</h2>
          {product.description_hindi && (
            <p className="catalog-hindi-title">{product.description_hindi}</p>
          )}

          <p style={{ fontSize: '0.92rem', color: 'var(--text-muted)', lineHeight: '1.55', marginBottom: '18px' }}>
            {product.description_english}
          </p>

          {/* Specifications */}
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

          {/* Cultural Heritage Story */}
          <div className="catalog-story-box">
            <div className="story-heading">
              <Heart size={14} color="#D97706" />
              <span>Artisan Heritage Story ({product.narrative_type || 'Cultural Heritage'})</span>
            </div>
            <p className="story-text">"{product.story}"</p>
            <div style={{ marginTop: '8px', fontSize: '0.75rem', color: '#92400E', fontWeight: 600 }}>
              Sentiment: {product.sentiment || 'Warm, authentic, heritage-focused'}
            </div>
          </div>

          {/* Transparent Pricing Breakdown */}
          <div className="pricing-highlight-box">
            <div>
              <div className="pricing-title">Fair Market Wholesale Range</div>
              <div style={{ fontSize: '0.75rem', color: '#065F46' }}>
                100% direct remuneration to rural artisan
              </div>
            </div>
            <div className="pricing-range">
              ₹{product.suggested_price_min} - ₹{product.suggested_price_max}
            </div>
          </div>

          {/* Primary Action Button */}
          <button
            className="btn-primary-large"
            style={{ background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)', boxShadow: '0 8px 20px rgba(15, 23, 42, 0.4)' }}
            onClick={() => setIsBulkModalOpen(true)}
          >
            <ShoppingBag size={20} />
            <span>Request Bulk Order (e.g. 100 units)</span>
          </button>
        </div>
      </div>

      {/* Bulk Order Modal */}
      {isBulkModalOpen && (
        <BulkOrderModal
          product={product}
          onClose={() => setIsBulkModalOpen(false)}
        />
      )}
    </div>
  );
}
