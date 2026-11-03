import React from 'react';
import { useApp } from '../../context/AppContext';
import { Home, Plus, Package, Inbox, ShoppingBag, Clock, Sparkles } from 'lucide-react';

export default function BottomNav() {
  const { role, currentScreen, navigateTo, orders, switchRole, t } = useApp();

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
          aria-label="Add new craft"
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
        >
          <div className="nav-icon-wrap">
            <Inbox size={20} />
          </div>
          <span>{t('orders')}</span>
          {pendingOrdersCount > 0 && (
            <span className="nav-badge">{pendingOrdersCount}</span>
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
        onClick={() => switchRole('artisan')}
      >
        <div className="nav-icon-wrap">
          <Sparkles size={20} />
        </div>
        <span>{t('artisanRole').split(' ')[0]}</span>
      </button>
    </nav>
  );
}