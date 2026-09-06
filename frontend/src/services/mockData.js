// Initial mock data adhering 100% to docs/API_CONTRACTS.md

export const PRODUCT_STATUSES = Object.freeze({
  DRAFT: 'draft',
  PROCESSING: 'processing',
  READY: 'ready',
  PUBLISHED: 'published',
  FAILED: 'failed',
});

export const INITIAL_PRODUCTS = [
  {
    id: "prod-bamboo-001",
    title: "Handcrafted North-East Bamboo Utility Basket",
    description_english: "Elegantly woven natural bamboo basket crafted by master artisans from Assam. Lightweight, durable, and eco-friendly storage container ideal for home decor and fruit display.",
    description_hindi: "असम के कुशल कारीगरों द्वारा निर्मित सुंदर प्राकृतिक बांस की टोकरी। हल्का, टिकाऊ और पर्यावरण के अनुकूल होम डेकोर सामान।",
    category: "Bamboo & Cane Craft",
    material: "Natural Assam Bamboo",
    dimensions: "30cm x 30cm x 20cm",
    production_time: "3 days",
    tags: ["bamboo", "eco-friendly", "handicraft", "home-decor", "northeast-art"],
    story: "Passed down through four generations, this basket weaving technique utilizes sustainably harvested bamboo shoots from local village groves in Silchar, Assam.",
    sentiment: "Warm, authentic, heritage-focused",
    narrative_type: "Cultural Heritage",
    image_url: "https://images.unsplash.com/photo-1590736969955-71cc94801759?auto=format&fit=crop&w=800&q=80",
    enhanced_image_url: "https://images.unsplash.com/photo-1590736969955-71cc94801759?auto=format&fit=crop&w=1200&q=90",
    suggested_price_min: 650.0,
    suggested_price_max: 950.0,
    artisan_id: "art-001",
    artisan_name: "Lakshmi Devi",
    location: "Silchar, Assam",
    created_at: "2026-09-03T17:00:00.000000"
  },
  {
    id: "prod-dupatta-002",
    title: "Chanderi Handwoven Silk Cotton Dupatta with Zari Border",
    description_english: "Exquisite Chanderi silk-cotton dupatta featuring traditional handwoven motif patterns and pure golden zari borders. Soft texture with regal lustre.",
    description_hindi: "पारंपरिक हथकरघा बुनाई और सुनहरे जरी बॉर्डर वाली प्रामाणिक चंदेरी सिल्क-कॉटन दुपट्टा। शाही रूप और रेशमी अहसास।",
    category: "Textiles & Handloom",
    material: "Chanderi Silk Cotton",
    dimensions: "2.5m x 0.9m",
    production_time: "7 days",
    tags: ["handloom", "chanderi", "silk", "ethnic-wear", "zari"],
    story: "Handwoven on traditional pit looms in Chanderi, Madhya Pradesh. Each motif represents regional flora and royal patronage traditions.",
    sentiment: "Elegant, luxury, traditional craftsmanship",
    narrative_type: "Artisanal Mastery",
    image_url: "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80",
    enhanced_image_url: "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=1200&q=90",
    suggested_price_min: 1800.0,
    suggested_price_max: 2400.0,
    artisan_id: "art-002",
    artisan_name: "Ramesh Ansari",
    location: "Chanderi, Madhya Pradesh",
    created_at: "2026-09-03T18:30:00.000000"
  },
  {
    id: "prod-wooden-003",
    title: "Saharanpur Carved Wooden Royal Elephant Figurine",
    description_english: "Intricately hand-carved Sheesham wood elephant sculpture with brass inlay motifs. Perfect centerpiece for living spaces reflecting royal Indian heritage.",
    description_hindi: "पीतल के काम से सजाई गई हाथ से नक्काशीदार शीशम की लकड़ी की हाथी की मूर्ति। सहारनपुर के प्रसिद्ध काष्ठशिल्प का प्रतीक।",
    category: "Woodcraft",
    material: "Sheesham Wood (Indian Rosewood)",
    dimensions: "15cm x 10cm x 22cm",
    production_time: "5 days",
    tags: ["woodcraft", "carved", "sheesham", "elephant", "brass-inlay"],
    story: "Carved painstakingly by Saharanpur artisans using traditional chisel tools without modern machinery, showcasing intricate floral engravings.",
    sentiment: "Regal, durable, classic art",
    narrative_type: "Heritage Craftsmanship",
    image_url: "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=800&q=80",
    enhanced_image_url: "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1200&q=90",
    suggested_price_min: 1200.0,
    suggested_price_max: 1650.0,
    artisan_id: "art-003",
    artisan_name: "Suresh Sharma",
    location: "Saharanpur, Uttar Pradesh",
    created_at: "2026-09-04T09:15:00.000000"
  },
  {
    id: "prod-pottery-004",
    title: "Traditional Jaipur Blue Pottery Floral Ceramic Vase",
    description_english: "Authentic handpainted Jaipur Blue Pottery vase crafted from quartz stone powder and natural oxide pigments. Features iconic Mughal floral artwork.",
    description_hindi: "क्वार्ट्ज पत्थर पाउडर और प्राकृतिक रंगों से निर्मित प्रामाणिक जयपुर ब्लू पॉटरी फूलदान। मुगलकालीन पारंपरिक चित्रकारी।",
    category: "Pottery & Ceramics",
    material: "Jaipur Blue Quartz Powder & Natural Pigments",
    dimensions: "18cm height x 12cm diameter",
    production_time: "6 days",
    tags: ["blue-pottery", "jaipur", "ceramic", "vase", "handpainted"],
    story: "Jaipur Blue Pottery is unique because it uses no clay; instead, local craftsmen knead quartz stone and glass powder before firing at low heat.",
    sentiment: "Vibrant, historic, artistic excellence",
    narrative_type: "Royal Heritage",
    image_url: "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=800&q=80",
    enhanced_image_url: "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=1200&q=90",
    suggested_price_min: 950.0,
    suggested_price_max: 1400.0,
    artisan_id: "art-004",
    artisan_name: "Pinki Kumawat",
    location: "Jaipur, Rajasthan",
    created_at: "2026-09-04T10:00:00.000000"
  }
];

export const INITIAL_ORDERS = [
  {
    id: "ord-fb9102",
    product_id: "prod-bamboo-001",
    product_title: "Handcrafted North-East Bamboo Utility Basket",
    artisan_id: "art-001",
    buyer_name: "FabIndia Procurement Team",
    buyer_contact: "procurement@fabindia.com / +91-9876543210",
    quantity: 100,
    notes: "Urgent procurement for Diwali festive eco-friendly gifting catalogue.",
    price_offered: 850.0,
    status: "pending",
    created_at: "2026-09-04T11:20:00.000000"
  },
  {
    id: "ord-tr7741",
    product_id: "prod-bamboo-001",
    product_title: "Handcrafted North-East Bamboo Utility Basket",
    artisan_id: "art-001",
    buyer_name: "Tribes India (TRIFED)",
    buyer_contact: "bulk@tribesindia.gov.in / +91-11-23345678",
    quantity: 50,
    notes: "National artisan fair showcase in New Delhi.",
    price_offered: 900.0,
    status: "accepted",
    created_at: "2026-09-03T14:45:00.000000"
  },
  {
    id: "ord-jp3302",
    product_id: "prod-dupatta-002",
    product_title: "Chanderi Handwoven Silk Cotton Dupatta with Zari Border",
    artisan_id: "art-002",
    buyer_name: "Jaypore Artisanal Retail",
    buyer_contact: "sourcing@jaypore.com / +91-9811223344",
    quantity: 40,
    notes: "Autumn handloom festive curation.",
    price_offered: 2150.0,
    status: "pending",
    created_at: "2026-09-04T08:10:00.000000"
  }
];

const PRODUCTS_STORAGE_KEY = 'tantu_products_db';
const ORDERS_STORAGE_KEY = 'tantu_orders_db';

export const getStoredProducts = () => {
  try {
    const raw = localStorage.getItem(PRODUCTS_STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed) && parsed.length > 0) return parsed;
    }
  } catch (e) {
    console.warn("Could not read local storage products", e);
  }
  return INITIAL_PRODUCTS;
};

export const setStoredProducts = (products) => {
  try {
    localStorage.setItem(PRODUCTS_STORAGE_KEY, JSON.stringify(products));
  } catch (e) {
    console.warn("Could not write local storage products", e);
  }
};

export const getStoredOrders = () => {
  try {
    const raw = localStorage.getItem(ORDERS_STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed) && parsed.length > 0) return parsed;
    }
  } catch (e) {
    console.warn("Could not read local storage orders", e);
  }
  return INITIAL_ORDERS;
};

export const setStoredOrders = (orders) => {
  try {
    localStorage.setItem(ORDERS_STORAGE_KEY, JSON.stringify(orders));
  } catch (e) {
    console.warn("Could not write local storage orders", e);
  }
};
