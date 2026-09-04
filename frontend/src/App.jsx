import React from 'react';
import { AppProvider, useApp } from './context/AppContext';
import Header from './components/common/Header';
import BottomNav from './components/common/BottomNav';
import Toast from './components/common/Toast';
import LanguageSelection from './components/artisan/LanguageSelection';
import ArtisanHome from './components/artisan/ArtisanHome';
import AddProductWizard from './components/artisan/AddProductWizard';
import MyProductsList from './components/artisan/MyProductsList';
import ArtisanProductDetail from './components/artisan/ArtisanProductDetail';
import ArtisanOrdersList from './components/artisan/ArtisanOrdersList';
import BuyerHome from './components/buyer/BuyerHome';
import BuyerProductDetail from './components/buyer/BuyerProductDetail';
import BuyerOrdersList from './components/buyer/BuyerOrdersList';

function MainAppShell() {
  const {
    hasChosenLanguage,
    setHasChosenLanguage,
    role,
    currentScreen,
    navigateTo,
    activeProductId,
    deviceFrame
  } = useApp();

  // If user has not chosen language on first run, show Language Selection Screen
  if (!hasChosenLanguage) {
    return (
      <div className={`app-viewport-wrapper ${deviceFrame ? 'device-mode' : ''}`}>
        <div className="app-container">
          <main className="app-main-content" style={{ paddingBottom: '20px' }}>
            <LanguageSelection onComplete={() => setHasChosenLanguage(true)} />
          </main>
          <Toast />
        </div>
      </div>
    );
  }

  return (
    <div className={`app-viewport-wrapper ${deviceFrame ? 'device-mode' : ''}`}>
      <div className="app-container">
        {/* Persistent App Header */}
        <Header />

        {/* Dynamic Screen Routing */}
        <main className="app-main-content">
          {/* ARTISAN FLOW */}
          {role === 'artisan' && (
            <>
              {currentScreen === 'home' && <ArtisanHome />}
              {currentScreen === 'add-wizard' && <AddProductWizard />}
              {currentScreen === 'my-products' && <MyProductsList />}
              {currentScreen === 'orders' && <ArtisanOrdersList />}
              {currentScreen === 'product-detail' && (
                <ArtisanProductDetail
                  productId={activeProductId}
                  onBack={() => navigateTo('my-products')}
                />
              )}
            </>
          )}

          {/* BUYER FLOW */}
          {role === 'buyer' && (
            <>
              {currentScreen === 'marketplace' && <BuyerHome />}
              {currentScreen === 'buyer-product-detail' && (
                <BuyerProductDetail
                  productId={activeProductId}
                  onBack={() => navigateTo('marketplace')}
                />
              )}
              {currentScreen === 'buyer-orders' && <BuyerOrdersList />}
            </>
          )}
        </main>

        {/* Bottom Navigation */}
        <BottomNav />

        {/* Global Toast */}
        <Toast />
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AppProvider>
      <MainAppShell />
    </AppProvider>
  );
}
