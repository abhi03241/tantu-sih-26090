import React from 'react';
import { useApp } from '../../context/AppContext';
import { Clock, CheckCircle2, ShoppingBag, ArrowRight, ShieldCheck, MapPin } from 'lucide-react';

export default function BuyerOrdersList() {
  const { orders, navigateTo } = useApp();

  return (
    <div>
      <div style={{ marginBottom: '18px' }}>
        <h2 className="section-title" style={{ fontSize: '1.4rem' }}>My Order Inquiries</h2>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
          Track B2B procurement requests sent directly to rural artisans
        </p>
      </div>

      {orders.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px 16px', background: '#FFFFFF', borderRadius: '20px', border: '1px solid var(--border-light)' }}>
          <ShoppingBag size={40} color="#94A3B8" style={{ marginBottom: '10px' }} />
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '6px' }}>No orders placed yet</h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
            Explore authentic artisan crafts and send your first bulk request.
          </p>
          <button className="btn-primary-large" onClick={() => navigateTo('marketplace')}>
            <span>Browse Catalogue</span>
            <ArrowRight size={18} />
          </button>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {orders.map((order) => {
            const isPending = order.status === 'pending';
            const total = (order.quantity || 1) * (order.price_offered || 850);

            return (
              <div
                key={order.id}
                style={{
                  background: '#FFFFFF',
                  border: isPending ? '1.5px solid #E2E8F0' : '1.5px solid #A7F3D0',
                  borderRadius: '18px',
                  padding: '16px 18px',
                  boxShadow: 'var(--shadow-sm)'
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
                      <span>{isPending ? 'Pending Artisan Review' : 'Accepted by Artisan'}</span>
                    </span>
                    <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-main)' }}>
                      {order.product_title}
                    </h3>
                  </div>

                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--indigo-dark)' }}>
                      ₹{total.toLocaleString('en-IN')}
                    </div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-light)' }}>
                      Estimated Value
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
                    <span style={{ color: 'var(--text-muted)' }}>Order ID:</span>
                    <span style={{ fontWeight: 700, fontFamily: 'monospace' }}>{order.id}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Requested Quantity:</span>
                    <span style={{ fontWeight: 700 }}>{order.quantity} units</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Offered Price:</span>
                    <span style={{ fontWeight: 700, color: '#059669' }}>₹{order.price_offered} / unit</span>
                  </div>
                  {order.notes && (
                    <div style={{ marginTop: '6px', paddingTop: '6px', borderTop: '1px dashed var(--border-light)', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                      Notes: "{order.notes}"
                    </div>
                  )}
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-light)' }}>
                    Created: {new Date(order.created_at || Date.now()).toLocaleDateString()}
                  </span>

                  <button
                    onClick={() => navigateTo('buyer-product-detail', order.product_id)}
                    style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--primary-700)', display: 'flex', alignItems: 'center', gap: '4px' }}
                  >
                    <span>View Product</span>
                    <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
