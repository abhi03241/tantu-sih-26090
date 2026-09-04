# TANTU API Contracts & Schema Specification

This document defines the unified API contracts for **TANTU** (SIH 26090). All frontend components (Team Member P) and AI modules (Team Members M, R, S) communicate using these exact REST contracts.

---

## 1. COMMON PRODUCT CONTRACT

Every product entity returned by or passed to the TANTU backend conforms to this standard JSON contract:

```json
{
  "id": "prod-bamboo-001",
  "title": "Handcrafted North-East Bamboo Utility Basket",
  "description_english": "Elegantly woven natural bamboo basket crafted by master artisans from Assam.",
  "description_hindi": "असम के कुशल कारीगरों द्वारा निर्मित सुंदर प्राकृतिक बांस की टोकरी।",
  "category": "Bamboo & Cane Craft",
  "material": "Natural Assam Bamboo",
  "dimensions": "30cm x 30cm x 20cm",
  "production_time": "3 days",
  "tags": ["bamboo", "eco-friendly", "handicraft", "home-decor"],
  "story": "Passed down through four generations in Silchar groves.",
  "sentiment": "Warm, authentic, heritage-focused",
  "narrative_type": "Cultural Heritage",
  "image_url": "https://images.unsplash.com/photo-1590736969955-71cc94801759",
  "enhanced_image_url": "https://images.unsplash.com/photo-1590736969955-71cc94801759?w=1200",
  "suggested_price_min": 650.0,
  "suggested_price_max": 950.0,
  "artisan_id": "art-001",
  "artisan_name": "Lakshmi Devi",
  "location": "Silchar, Assam",
  "created_at": "2026-09-03T17:00:00.000000"
}
```

---

## 2. API ENDPOINTS REFERENCE

### A. Core Product Endpoints

#### 1. Create Product
* **Endpoint**: `POST /api/products`
* **Request Body**:
```json
{
  "title": "Handwoven Silk Dupatta",
  "description_english": "Handloom silk dupatta with zari border.",
  "description_hindi": "जरी बॉर्डर वाली हाथ से बुनी सिल्क दुपट्टा।",
  "category": "Textiles & Handloom",
  "material": "Chanderi Silk",
  "dimensions": "2.5m x 0.9m",
  "production_time": "5 days",
  "tags": ["handloom", "silk"],
  "story": "Woven in Chanderi village.",
  "image_url": "https://images.unsplash.com/photo-1610030469983-98e550d6193c",
  "artisan_id": "art-002"
}
```
* **Response Status**: `201 Created`
* **Response Body**: Full Product Object with generated `id` and `created_at`.

---

#### 2. List Products
* **Endpoint**: `GET /api/products`
* **Query Parameters**:
  * `category` (optional, string): Filter by craft category
  * `artisan_id` (optional, string): Filter by artisan
  * `q` (optional, string): Search query across title, description, material
* **Response Status**: `200 OK`
* **Response Body**: Array of Product Objects.

---

#### 3. Get Product by ID
* **Endpoint**: `GET /api/products/{id}`
* **Response Status**: `200 OK` (or `404 Not Found`)
* **Response Body**: Single Product Object.

---

### B. AI Modules Integration Endpoints

#### 4. Voice Processing (NLP Module - Team Member M)
* **Endpoint**: `POST /api/products/{id}/voice`
* **Request Body**:
```json
{
  "audio_transcript": "यह हाथ से बना बांस का झूला है जो असम के सिलचर में 3 दिन में बनता है।",
  "language": "hi"
}
```
* **Response Status**: `200 OK`
* **Response Body**: Updated Product Object (with extracted title, Hindi/English descriptions, tags, sentiment, story).

---

#### 5. Image Enhancement (Vision Module - Team Member R)
* **Endpoint**: `POST /api/products/{id}/enhance-image`
* **Request Body** (optional):
```json
{
  "image_url": "https://images.unsplash.com/photo-1590736969955-71cc94801759",
  "prompt": "Clean studio backdrop with soft warm lighting"
}
```
* **Response Status**: `200 OK`
* **Response Body**: Updated Product Object containing generated `enhanced_image_url`.

---

#### 6. Generate Catalogue (NLP Module - Team Member M)
* **Endpoint**: `POST /api/products/{id}/generate-catalogue`
* **Request Body** (optional):
```json
{
  "raw_notes": "Handcrafted bamboo basket made by Assam villagers."
}
```
* **Response Status**: `200 OK`
* **Response Body**: Updated Product Object with regenerated marketing text and storytelling tags.

---

#### 7. Smart Pricing Calculation (Pricing Module - Team Member S)
* **Endpoint**: `POST /api/products/{id}/price`
* **Request Body** (optional):
```json
{
  "raw_material_cost": 250.0,
  "labor_hours": 16
}
```
* **Response Status**: `200 OK`
* **Response Body**: Updated Product Object with calculated `suggested_price_min` and `suggested_price_max`.

---

#### 8. End-to-End AI Orchestration Pipeline (SIH Demo Endpoint)
* **Endpoint**: `POST /api/products/{id}/process`
* **Description**: Orchestrates the complete cataloging pipeline in a single request: Voice/Text Input -> NLP Processing -> Studio Vision Enhancement -> Dynamic Fair Pricing -> Database Persistence. Pass `{id}` as an existing product ID or `"new"` to create a new product dynamically.
* **Request Body**:
```json
{
  "audio_transcript": "Ye bamboo ki tokri hai. Isko banane mein do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha.",
  "image_url": "https://images.unsplash.com/photo-1590736969955-71cc94801759",
  "prompt": "Clean studio background with warm lighting",
  "raw_material_cost": 250.0,
  "language": "hi",
  "artisan_id": "art-001"
}
```
* **Response Status**: `200 OK`
* **Response Body**: Complete `Product` JSON Object with extracted attributes, bilingual copy, enhanced image reference, and suggested price bounds.


---

### C. Dashboard & Marketplace Feeds

#### 8. Artisan Product Feed
* **Endpoint**: `GET /api/artisan/products?artisan_id={artisan_id}`
* **Response Status**: `200 OK`
* **Response Body**: Array of products cataloged by the given artisan.

---

#### 9. Buyer Product Feed
* **Endpoint**: `GET /api/buyer/products?category={category}&q={search}`
* **Response Status**: `200 OK`
* **Response Body**: Array of products formatted for B2B/B2C marketplace showcase.

---

### D. B2B Order Linkage Endpoints

#### 10. Create Order Request
* **Endpoint**: `POST /api/orders/request`
* **Request Body**:
```json
{
  "product_id": "prod-bamboo-001",
  "buyer_name": "FabIndia Procurement Team",
  "buyer_contact": "procurement@fabindia.com / +91-9876543210",
  "quantity": 100,
  "notes": "Bulk order for festival season.",
  "price_offered": 850.0
}
```
* **Response Status**: `201 Created`
* **Response Body**:
```json
{
  "id": "ord-a1b2c3d4",
  "product_id": "prod-bamboo-001",
  "product_title": "Handcrafted North-East Bamboo Utility Basket",
  "artisan_id": "art-001",
  "buyer_name": "FabIndia Procurement Team",
  "buyer_contact": "procurement@fabindia.com / +91-9876543210",
  "quantity": 100,
  "notes": "Bulk order for festival season.",
  "price_offered": 850.0,
  "status": "pending",
  "created_at": "2026-09-03T17:20:00.000000"
}
```

---

#### 11. List Orders
* **Endpoint**: `GET /api/orders`
* **Query Parameters**: `product_id`, `artisan_id`
* **Response Status**: `200 OK`
* **Response Body**: Array of Order Request Objects.

---

#### 12. Update Order Status
* **Endpoint**: `PATCH /api/orders/{id}/status?new_status={status}`
* **Query Parameters**: `new_status` (`pending`, `accepted`, `fulfilled`, `rejected`)
* **Response Status**: `200 OK`
* **Response Body**: Updated Order Request Object.

---

### E. Profile & User Management

#### 13. Create or Update Artisan Profile
* **Endpoint**: `POST /api/artisan/profile`
* **Request Body**:
```json
{
  "user_id": "art-001",
  "artisan_name": "Lakshmi Devi",
  "craft_type": "Bamboo & Natural Fiber Crafting",
  "location": "Silchar, Assam",
  "bio": "Master artisan with 20+ years of experience.",
  "phone": "+91-9876543210",
  "story_style": "Cultural Heritage"
}
```
* **Response Status**: `201 Created`

---

#### 14. Create or Update Buyer Profile
* **Endpoint**: `POST /api/buyer/profile`
* **Request Body**:
```json
{
  "user_id": "user-buyer-001",
  "buyer_name": "FabIndia Procurement Team",
  "organization": "FabIndia Overseas Pvt Ltd",
  "buyer_type": "B2B Retailer",
  "contact_email": "procurement@fabindia.com"
}
```
* **Response Status**: `201 Created`

