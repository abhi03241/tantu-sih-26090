import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { orderService } from '../../services/orders';
import { Inbox, CheckCircle2, Clock, Phone, Mail, FileText, Check, ChevronRight } from 'lucide-react';

export default function ArtisanOrdersList() {
  const { orders, artisanProfile, refreshData, showToast, speakText, t } = useApp();
  const [filter, setFilter] = useState('all'); // 'all' | 'pending' | 'accepted'

  const myOrders = orders.filter(o => !o.artisan_id || o.artisan_id === artisanProfile.id);

  const filteredOrders = myOrders.filter(o => {
    if (filter === 'pending') return o.status === 'pending';
    if (filter === 'accepted') return o.status === 'accepted';
    return true;
  });

  const handleAcceptOrder = async (orderId) => {
    try {
      await orderService.updateOrderStatus(orderId, 'accepted');
      refreshData();
      showToast("ऑर्डर स्वीकार कर लिया गया है!", "success");
      speakText("ऑर्डर स्वीकार कर लिया गया है। खरीदार को सूचना भेज दी गई है।");
    } catch (e) {
      showToast("त्रुटि हुई", "error");
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '16px' }}>
        <h2 className="section-title" style={{ fontSize: '1.4rem' }}>{t('orders')}</h2>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
          शहरी खरीदारों व B2B कंपनियों से सीधे थोक ऑर्डर अनुरोध
        </p>
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '18px' }}>
        <button
          className={`category-chip ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          <span>सभी ({myOrders.length})</span>
        </button>
        <button
          className={`category-chip ${filter === 'pending' ? 'active' : ''}`}
          onClick={() => setFilter('pending')}
        >
          <span>लंबित ({myOrders.filter(o => o.status === 'pending').length})</span>
        </button>
        <button
          className={`category-chip ${filter === 'accepted' ? 'active' : ''}`}
          onClick={() => setFilter('accepted')}
        >
          <span>स्वीकृत ({myOrders.filter(o => o.status === 'accepted').length})</span>
        </button>
      </div>

      {/* Orders List */}
      {filteredOrders.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px 16px', background: '#FFFFFF', borderRadius: '20px', border: '1px solid var(--border-light)' }}>
          <Inbox size={40} color="#94A3B8" style={{ marginBottom: '10px' }} />
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '6px' }}>कोई ऑर्डर अनुरोध नहीं मिला</h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            जैसे ही खरीदार आपके शिल्प के लिए थोक अनुरोध भेजेंगे, वे यहाँ दिखाई देंगे।
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {filteredOrders.map((order) => {
            const isPending = order.status === 'pending';
            const totalValue = (order.quantity || 1) * (order.price_offered || 800);

            return (
              <div
                key={order.id}
                style={{
                  background: '#FFFFFF',
                  border: isPending ? '1.5px solid #FED7AA' : '1px solid var(--border-light)',
                  borderRadius: '18px',
                  padding: '16px 18px',
                  boxShadow: 'var(--shadow-sm)',
                  position: 'relative'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                  <div>
                    <span
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px',
                        fontSize: '0.72rem',
                        fontWeight: 700,
                        padding: '3px 10px',
                        borderRadius: '999px',
                        background: isPending ? '#FEF3C7' : '#D1FAE5',
                        color: isPending ? '#B45309' : '#065F46',
                        marginBottom: '6px'
                      }}
                    >
                      {isPending ? <Clock size={12} /> : <CheckCircle2 size={12} />}
                      <span>{isPending ? 'लंबित अनुरोध (Pending)' : 'स्वीकृत (Accepted)'}</span>
                    </span>
                    <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-main)', lineHeight: 1.3 }}>
                      {order.product_title}
                    </h3>
                  </div>

                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '1.15rem', fontWeight: 800, color: '#059669' }}>
                      ₹{totalValue.toLocaleString('en-IN')}
                    </div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-light)' }}>
                      कुल मूल्य
                    </div>
                  </div>
                </div>

                <div
                  style={{
                    background: 'var(--bg-sand)',
                    borderRadius: '12px',
                    padding: '10px 14px',
                    fontSize: '0.82rem',
                    marginBottom: '12px'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>खरीदार (Buyer):</span>
                    <span style={{ fontWeight: 700, color: 'var(--text-main)' }}>{order.buyer_name}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>मात्रा (Quantity):</span>
                    <span style={{ fontWeight: 700, color: 'var(--text-main)' }}>{order.quantity} इकाइयाँ (Units)</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>प्रस्तावित दर:</span>
                    <span style={{ fontWeight: 700, color: 'var(--primary-700)' }}>₹{order.price_offered} प्रति इकाई</span>
                  </div>
                  {order.notes && (
                    <div style={{ marginTop: '6px', paddingTop: '6px', borderTop: '1px dashed var(--border-light)', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                      "{order.notes}"
                    </div>
                  )}
                </div>

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-light)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Phone size={13} />
                    <span>{order.buyer_contact}</span>
                  </div>

                  {isPending && (
                    <button
                      className="btn-primary-large"
                      style={{ minHeight: '40px', padding: '6px 16px', width: 'auto', fontSize: '0.85rem', margin: 0 }}
                      onClick={() => handleAcceptOrder(order.id)}
                    >
                      <Check size={16} strokeWidth={2.8} />
                      <span>स्वीकार करें (Accept)</span>
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
