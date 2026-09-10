import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { orderService } from '../../services/orders';
import { ShoppingBag, CheckCircle, Plus, Minus, Send, X, ShieldCheck } from 'lucide-react';

export default function BulkOrderModal({ product, onClose }) {
  const { buyerProfile, refreshData, showToast, navigateTo } = useApp();

  const [quantity, setQuantity] = useState(100); // Default to prompt example "Request 100 units"
  const [priceOffered, setPriceOffered] = useState(product.suggested_price_min || 850);
  const [buyerName, setBuyerName] = useState(buyerProfile.name || 'FabIndia Procurement Team');
  const [buyerContact, setBuyerContact] = useState(buyerProfile.email || 'procurement@fabindia.com / +91-9876543210');
  const [notes, setNotes] = useState('Bulk purchase inquiry for festive season catalog.');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const presets = [25, 50, 100, 250, 500];

  const estimatedTotal = quantity * priceOffered;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (quantity <= 0) {
      showToast("कृपया वैध मात्रा दर्ज करें", "error");
      return;
    }

    setIsSubmitting(true);
    try {
      const orderPayload = {
        product_id: product.id,
        buyer_name: buyerName,
        buyer_contact: buyerContact,
        quantity: Number(quantity),
        notes: notes,
        price_offered: Number(priceOffered)
      };

      const result = await orderService.createOrderRequest(orderPayload);
      refreshData();
      showToast(`ऑर्डर अनुरोध सफलतापूर्वक भेजा गया! (ID: ${result.id})`, 'success');
      onClose();
      navigateTo('buyer-orders');
    } catch (err) {
      showToast("ऑर्डर अनुरोध भेजने में त्रुटि", "error");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content-sheet" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header-row">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ width: 34, height: 34, borderRadius: '10px', background: 'var(--primary-100)', color: 'var(--primary-700)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <ShoppingBag size={18} />
            </div>
            <div>
              <h3 className="modal-title" style={{ fontSize: '1.1rem' }}>Bulk Purchase Request</h3>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-light)' }}>Direct B2B Order Linkage</div>
            </div>
          </div>
          <button className="modal-close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        {/* Product mini summary */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            background: 'var(--bg-sand)',
            borderRadius: '14px',
            padding: '10px 12px',
            marginBottom: '16px'
          }}
        >
          <img
            src={product.enhanced_image_url || product.image_url}
            alt={product.title}
            style={{ width: '48px', height: '48px', borderRadius: '10px', objectFit: 'cover' }}
          />
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: '0.88rem', fontWeight: 700, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {product.title}
            </div>
            <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>
              Artisan: {product.artisan_name || 'Lakshmi Devi'} ({product.location || 'Assam'})
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {/* Quantity Stepper & Presets */}
          <div>
            <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>
              Order Quantity (Units)
            </label>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <button
                type="button"
                className="pill-btn"
                style={{ width: '42px', height: '42px', justifyContent: 'center', padding: 0 }}
                onClick={() => setQuantity(prev => Math.max(1, prev - 10))}
              >
                <Minus size={16} />
              </button>
              <input
                type="number"
                min="1"
                value={quantity}
                onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                style={{
                  flex: 1,
                  height: '42px',
                  textAlign: 'center',
                  fontSize: '1.2rem',
                  fontWeight: 800,
                  borderRadius: '12px',
                  border: '1.5px solid var(--border-light)'
                }}
              />
              <button
                type="button"
                className="pill-btn"
                style={{ width: '42px', height: '42px', justifyContent: 'center', padding: 0 }}
                onClick={() => setQuantity(prev => prev + 10)}
              >
                <Plus size={16} />
              </button>
            </div>

            {/* Quick Presets */}
            <div style={{ display: 'flex', gap: '6px' }}>
              {presets.map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => setQuantity(p)}
                  style={{
                    flex: 1,
                    padding: '6px 4px',
                    borderRadius: '8px',
                    fontSize: '0.75rem',
                    fontWeight: quantity === p ? 800 : 600,
                    background: quantity === p ? 'var(--primary-100)' : '#FFFFFF',
                    color: quantity === p ? 'var(--primary-800)' : 'var(--text-muted)',
                    border: quantity === p ? '1.5px solid var(--primary-500)' : '1px solid var(--border-light)'
                  }}
                >
                  {p} units
                </button>
              ))}
            </div>
          </div>

          {/* Price Offered per Unit */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
              <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)' }}>
                Target Price per Unit (₹)
              </label>
              <span style={{ fontSize: '0.72rem', color: 'var(--text-light)' }}>
                Fair Range: ₹{product.suggested_price_min} - ₹{product.suggested_price_max}
              </span>
            </div>
            <input
              type="number"
              value={priceOffered}
              onChange={(e) => setPriceOffered(Number(e.target.value) || 0)}
              style={{
                width: '100%',
                height: '42px',
                padding: '8px 14px',
                borderRadius: '12px',
                border: '1.5px solid var(--border-light)',
                fontWeight: 700
              }}
            />
          </div>

          {/* Buyer Name & Contact */}
          <div className="buyer-contact-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
            <div>
              <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>
                Buyer / Organization
              </label>
              <input
                type="text"
                required
                value={buyerName}
                onChange={(e) => setBuyerName(e.target.value)}
                style={{ width: '100%', padding: '8px 12px', borderRadius: '12px', border: '1.5px solid var(--border-light)', fontSize: '0.85rem' }}
              />
            </div>
            <div>
              <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>
                Contact / Phone
              </label>
              <input
                type="text"
                required
                value={buyerContact}
                onChange={(e) => setBuyerContact(e.target.value)}
                style={{ width: '100%', padding: '8px 12px', borderRadius: '12px', border: '1.5px solid var(--border-light)', fontSize: '0.85rem' }}
              />
            </div>
          </div>

          {/* Delivery Timeline / Notes */}
          <div>
            <label style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>
              Procurement Notes & Delivery Requirement
            </label>
            <textarea
              rows={2}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="e.g. Festival gifting timeline, custom tags..."
              style={{ width: '100%', padding: '8px 12px', borderRadius: '12px', border: '1.5px solid var(--border-light)', fontSize: '0.85rem' }}
            />
          </div>

          {/* Valuation Summary Box */}
          <div
            style={{
              background: '#F8FAFC',
              border: '1px solid #E2E8F0',
              borderRadius: '14px',
              padding: '12px 16px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}
          >
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-light)', fontWeight: 600 }}>Total Inquiry Value</div>
              <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--indigo-dark)' }}>
                ₹{estimatedTotal.toLocaleString('en-IN')}
              </div>
            </div>
            <div style={{ fontSize: '0.72rem', color: '#059669', display: 'flex', alignItems: 'center', gap: '4px', fontWeight: 700 }}>
              <ShieldCheck size={14} />
              <span>Direct to Artisan</span>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="btn-primary-large"
            style={{
              background: 'linear-gradient(135deg, var(--indigo-dark) 0%, #1E293B 100%)',
              marginTop: '6px',
              opacity: isSubmitting ? 0.7 : 1
            }}
          >
            <Send size={18} />
            <span>{isSubmitting ? 'Sending Request...' : `Submit Request (${quantity} units)`}</span>
          </button>
        </form>
      </div>
    </div>
  );
}
