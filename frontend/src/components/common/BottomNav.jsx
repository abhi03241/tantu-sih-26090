import React from 'react';
import { useApp } from '../../context/AppContext';
import { Home, Plus, Package, Inbox, ShoppingBag, Clock, Sparkles } from 'lucide-react';

export default function BottomNav() {
  const { role, currentScreen, navigateTo, orders, t } = useApp();

  const pendingOrdersCount = orders.filter(o => o.status === 'pending').length;

  if (role === 'artisan') {
    return (
      <nav className="bottom-nav">
        <button
          className={`nav-item ${currentScreen === 'home' ? 'active' : ''}`}
          onClick={() => navigateTo('home')}
        >
          <div className="nav-icon-wrap">
            <Home size={20} />
          </div>
          <span>{t('home')}</span>
        </button>

        <button
          className="nav-center-action"
          onClick={() => navigateTo('add-wizard')}
          title="Add New Craft via AI"
        >
          <Plus size={28} strokeWidth={2.8} />
        </button>

        <button
          className={`nav-item ${currentScreen === 'my-products' ? 'active' : ''}`}
          onClick={() => navigateTo('my-products')}
        >
          <div className="nav-icon-wrap">
            <Package size={20} />
          </div>
          <span>{t('myProducts')}</span>
        </button>

        <button
          className={`nav-item ${currentScreen === 'orders' ? 'active' : ''}`}
          onClick={() => navigateTo('orders')}
          style={{ position: 'relative' }}
        >
          <div className="nav-icon-wrap">
            <Inbox size={20} />
          </div>
          <span>{t('orders')}</span>
          {pendingOrdersCount > 0 && (
            <span
              style={{
                position: 'absolute',
                top: 4,
                right: 14,
                background: '#DC2626',
                color: '#FFFFFF',
                borderRadius: '999px',
                fontSize: '0.65rem',
                fontWeight: 800,
                width: 18,
                height: 18,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                border: '2px solid #FFFFFF'
              }}
            >
              {pendingOrdersCount}
            </span>
          )}
        </button>
      </nav>
    );
  }

  // Buyer navigation
  return (
    <nav className="bottom-nav">
      <button
        className={`nav-item ${currentScreen === 'marketplace' ? 'active' : ''}`}
        onClick={() => navigateTo('marketplace')}
      >
        <div className="nav-icon-wrap">
          <ShoppingBag size={20} />
        </div>
        <span>{t('marketplace')}</span>
      </button>

      <button
        className={`nav-item ${currentScreen === 'buyer-orders' ? 'active' : ''}`}
        onClick={() => navigateTo('buyer-orders')}
      >
        <div className="nav-icon-wrap">
          <Clock size={20} />
        </div>
        <span>{t('orders')}</span>
      </button>

      <button
        className="nav-item"
        onClick={() => navigateTo('home')}
      >
        <div className="nav-icon-wrap">
          <Sparkles size={20} />
        </div>
        <span>{t('artisanRole').split(' ')[0]}</span>
      </button>
    </nav>
  );
}
