# TANTU (तंतु) — Frontend & Mobile UI Module

**Maintained by Team Member P (Frontend/Mobile UI Lead)**  
**SIH Problem Statement 26090**: *AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans*

---

## Overview

The TANTU frontend is a modern, tactile, voice-first mobile web application designed specifically for rural Indian artisans with low digital literacy, alongside a streamlined B2B wholesale marketplace for urban retail buyers and institutional purchasers (FabIndia, Tribes India TRIFED, Jaypore, etc.).

---

## Key Screens & Flows Implemented

### 1. Artisan Persona Flow
- **Language Selection**: Large touch cards in 9 regional languages (हिन्दी, English, বাংলা, অসমীया, ଓଡ଼ିଆ, मराठी, ગુજરાતી, తెలుగు, தமிழ்) with instant native audio greetings.
- **Artisan Home**: Personalized artisan dashboard (Lakshmi Devi, Silchar Assam) displaying listed crafts, active orders, estimated earnings, audio guidance button, and recent listings.
- **Add Product Wizard**:
  1. **Photo Capture / Upload**: High-resolution camera/gallery upload + 1-click sample craft picker for instant demo test.
  2. **Voice Narrative Recording**: Large pulsing microphone button, Web Speech API speech-to-text recognition, live waveform visualizer, audio playback, and transcript editor.
  3. **Multimodal AI Processing Pipeline**: Sequential animated progress screen demonstrating:
     - 🎙️ *Understanding your voice* (Voice transcript NLP & translation)
     - 🔍 *Identifying product & craft category* (Craft taxonomy)
     - ✍️ *Creating bilingual catalogue & story* (English & Hindi marketing descriptions + heritage storytelling)
     - ✨ *Enhancing image with AI studio lighting* (Background noise removal & softbox lighting)
     - 💰 *Estimating fair market price range* (Fair trade margin calculation)
  4. **Smart Catalogue Review**: Interactive Before/After image comparison toggle (Raw vs AI Studio Enhanced), bilingual titles & descriptions, extracted specifications (Material, Dimensions, Production Time, Tags), heritage narrative & sentiment badge, and suggested price range.
  5. **Edit Catalogue Modal**: Touch-friendly form to refine dimensions, title, story, or pricing prior to publishing.
  6. **Approve & Publish Celebration**: Confetti animation (`canvas-confetti`), celebration badge, and instant synchronization to the marketplace.
- **My Products**: Filterable catalogue list by craft category and search keyword.
- **Product Details**: Full specification view, before/after studio lighting toggle, order inquiry history, and link copying.
- **Order Requests**: Inbound B2B buyer inquiries with quantity, offered price, and 1-tap "Accept Order (स्वीकार करें)" workflow.

### 2. Buyer Persona Flow
- **Buyer Home / Marketplace Feed**: High-contrast search bar, craft category pills (Bamboo, Silk, Woodcraft, Blue Pottery, etc.), verified rural artisan badge, and product cards.
- **Buyer Product Detail**: Studio-grade product showcase, artisan background card with village heritage story, fair trade price transparency, and primary action: **Request Bulk Order**.
- **Bulk Order Modal**: Quantity stepper with presets (25, 50, 100, 250, 500 units), custom price per unit input, real-time total order value calculation, and inquiry submission.
- **My Order Inquiries**: Live status tracking (`pending`, `accepted`) for placed bulk orders.

### 3. Accessibility & Presentation Features
- **Voice-First Assist**: Built-in Web Speech synthesis TTS reader (`speakText`) allowing any screen or card to be read aloud in regional accents.
- **Device Frame Simulator**: 1-click toggle in the header between responsive web view and an iPhone/Android mobile container for hackathon presentations.
- **Dual API Architecture**: Seamless communication with the FastAPI backend (`http://localhost:8000`), with transparent automatic fallback to persistent `localStorage` mock data if the backend is offline.

---

## How to Run

### Prerequisites
- Node.js 18+ and npm installed

### Setup & Launch
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
The app will be live at `http://localhost:5173/`.

### Build for Production
```bash
npm run build
npm run preview
```

---

## Architecture & File Structure

```
frontend/
├── index.html                  # Mobile-first viewport, Google Fonts (Outfit, Noto Sans Devanagari)
├── package.json                # React 18, Vite 6, Lucide React, Canvas Confetti
├── vite.config.js              # Vite config with /api proxy to localhost:8000
├── public/
│   └── favicon.svg             # Stylized Indian loom shuttle & thread emblem
└── src/
    ├── main.jsx                # React DOM root entrypoint
    ├── App.jsx                 # App shell, router, and modal coordinator
    ├── index.css               # Rich Indian artisanal design tokens & animations
    ├── constants/
    │   ├── languages.js        # 9 regional languages & UI string dictionaries
    │   └── categories.js       # Craft taxonomies & demo sample craft profiles
    ├── context/
    │   └── AppContext.jsx      # Global state (role, language, active craft, TTS, orders)
    ├── services/
    │   ├── api.js              # Base fetch client with backend health checking
    │   ├── mockData.js         # Fallback mock database conforming to API contracts
    │   ├── products.js         # Product CRUD & AI endpoints (/voice, /enhance-image, /price)
    │   └── orders.js           # B2B order request endpoints
    └── components/
        ├── common/
        │   ├── Header.jsx      # Brand, role switcher, language picker, device frame toggle
        │   ├── BottomNav.jsx   # Mobile bottom navigation bar with pending order badges
        │   └── Toast.jsx       # Floating notifications
        ├── artisan/
        │   ├── LanguageSelection.jsx
        │   ├── ArtisanHome.jsx
        │   ├── AddProductWizard.jsx
        │   ├── MyProductsList.jsx
        │   ├── ArtisanProductDetail.jsx
        │   └── ArtisanOrdersList.jsx
        └── buyer/
            ├── BuyerHome.jsx
            ├── BuyerProductDetail.jsx
            ├── BulkOrderModal.jsx
            └── BuyerOrdersList.jsx
```

---

## API Contract Compliance

All product and order schemas strictly mirror `docs/API_CONTRACTS.md`:
- Product model: `id`, `title`, `description_english`, `description_hindi`, `category`, `material`, `dimensions`, `production_time`, `tags`, `story`, `sentiment`, `narrative_type`, `image_url`, `enhanced_image_url`, `suggested_price_min`, `suggested_price_max`, `artisan_id`, `artisan_name`, `location`, `created_at`.
- Order model: `id`, `product_id`, `product_title`, `artisan_id`, `buyer_name`, `buyer_contact`, `quantity`, `notes`, `price_offered`, `status`, `created_at`.
