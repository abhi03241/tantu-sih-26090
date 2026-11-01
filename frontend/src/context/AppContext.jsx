import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { LANGUAGES, getTranslation } from '../constants/languages';
import { productService } from '../services/products';
import { orderService } from '../services/orders';
import { checkBackendHealth } from '../services/api';

const AppContext = createContext(null);

export function AppProvider({ children }) {
  // Localization & Persona
  const [language, setLanguage] = useState(() => localStorage.getItem('tantu_language') || 'hi');
  const [hasChosenLanguage, setHasChosenLanguage] = useState(() => !!localStorage.getItem('tantu_language'));
const [role, setRole] = useState(() => {
  const savedRole = localStorage.getItem('tantu_role');
  return savedRole === 'buyer' ? 'buyer' : 'artisan';
});
  // Navigation:
  // Artisan: 'home' | 'add-wizard' | 'my-products' | 'orders' | 'product-detail'
  // Buyer: 'marketplace' | 'buyer-product-detail' | 'buyer-orders'
  // Keep the persisted persona and its entry screen in sync on a page reload.
const [currentScreen, setCurrentScreen] = useState(() => {
  const token = localStorage.getItem('access_token');
  const savedRole = localStorage.getItem('tantu_role');

  if (!token) return 'login';

  return savedRole === 'buyer' ? 'marketplace' : 'home';
});
  const [activeProductId, setActiveProductId] = useState(null);

  // App Data
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [backendOnline, setBackendOnline] = useState(false);

  // UI Enhancements
  const [deviceFrame, setDeviceFrame] = useState(false); // Mobile device simulation frame
  const [toast, setToast] = useState(null);
  const [ttsSpeaking, setTtsSpeaking] = useState(false);

  // Active Artisan Profile (Lakshmi Devi - Silk & Bamboo craftsperson)
  const [artisanProfile] = useState({
    id: 'art-001',
    name: 'Lakshmi Devi',
    craft: 'Bamboo & Natural Fiber Crafting',
    location: 'Silchar, Assam',
    phone: '+91-9876543210',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80',
    experience: '20+ years of generational craft mastery',
    rating: 4.9
  });

  // Active Buyer Profile (FabIndia Procurement)
  const [buyerProfile] = useState({
    name: 'FabIndia Sustainable Procurement Team',
    email: 'procurement@fabindia.com',
    location: 'New Delhi, India',
    type: 'B2B Retail Partner'
  });

  // Translation helper
  const t = useCallback((key) => {
    return getTranslation(language, key);
  }, [language]);

  // Toast notification helper
  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type, id: Date.now() });
    setTimeout(() => {
      setToast((curr) => (curr && curr.id ? null : curr));
    }, 4000);
  }, []);

  // Text-To-Speech audio reader for rural artisans
  const speakText = useCallback((text, langCode = null) => {
    if (!('speechSynthesis' in window)) return;
    try {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      const targetLang = langCode || language;
      const langObj = LANGUAGES.find(l => l.code === targetLang);
      utterance.lang = langObj ? langObj.locale : 'hi-IN';
      utterance.rate = 0.95;
      utterance.pitch = 1.0;

      utterance.onstart = () => setTtsSpeaking(true);
      utterance.onend = () => setTtsSpeaking(false);
      utterance.onerror = () => setTtsSpeaking(false);

      window.speechSynthesis.speak(utterance);
    } catch (err) {
      console.warn("TTS Error:", err);
      setTtsSpeaking(false);
    }
  }, [language]);

  const stopSpeech = useCallback(() => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setTtsSpeaking(false);
    }
  }, []);

  // Load backend health, products and orders
  const refreshData = useCallback(async () => {
    setLoading(true);
    try {
      const isOnline = await checkBackendHealth();
      setBackendOnline(isOnline);

      const [prods, ords] = await Promise.all([
        productService.listProducts(),
        orderService.listOrders()
      ]);
      setProducts(prods || []);
      setOrders(ords || []);
    } catch (err) {
      console.warn("Error loading data:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshData();
  }, [refreshData]);

  // Update language selection
  const selectLanguage = (code) => {
    setLanguage(code);
    localStorage.setItem('tantu_language', code);
    const langObj = LANGUAGES.find(l => l.code === code);
    if (langObj) {
      speakText(langObj.greeting, code);
    }
  };

  // Switch Role
  // Set role only after successful login or signup
const setAuthenticatedRole = (userRole) => {
  if (userRole !== 'artisan' && userRole !== 'buyer') {
    showToast('Invalid account role.', 'error');
    return;
  }

  setRole(userRole);
  localStorage.setItem('tantu_role', userRole);

  if (userRole === 'artisan') {
    setCurrentScreen('home');
  } else {
    setCurrentScreen('marketplace');
  }
};

// Prevent switching to another role without another account
const switchRole = () => {
  showToast(
    'Your account has a fixed role. Please log in with a separate account to access another role.',
    'info'
  );
};
// Logout user
const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('tantu_role');

  setRole('artisan');
  setCurrentScreen('login');

  showToast('You have been logged out successfully.', 'success');
};
  // Navigate to screen
  const navigateTo = (screen, productId = null) => {
    stopSpeech();
    setCurrentScreen(screen);
    if (productId !== undefined) {
      setActiveProductId(productId);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <AppContext.Provider
      value={{
        language,
        setLanguage: selectLanguage,
        hasChosenLanguage,
        setHasChosenLanguage,
        role,
        switchRole,
        setAuthenticatedRole,
        logout,
        currentScreen,
        navigateTo,
        activeProductId,
        setActiveProductId,
        products,
        setProducts,
        orders,
        setOrders,
        loading,
        refreshData,
        backendOnline,
        artisanProfile,
        buyerProfile,
        deviceFrame,
        setDeviceFrame,
        toast,
        showToast,
        t,
        speakText,
        stopSpeech,
        ttsSpeaking
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) throw new Error('useApp must be used within AppProvider');
  return context;
}
