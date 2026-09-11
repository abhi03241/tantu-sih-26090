import { request } from './api';
import { getStoredProducts, setStoredProducts, PRODUCT_STATUSES } from './mockData';

// Generate simulated AI processing for mock fallback
function simulateVoiceAI(product, transcript, language = 'hi') {
  const lower = (transcript || '').toLowerCase();
  
  let category = product.category || 'Handicraft';
  let material = product.material || 'Natural Fiber';
  let dimensions = product.dimensions || 'Standard Size';
  let productionTime = product.production_time || '3-5 days';
  let story = product.story || 'Passed down through multiple generations of rural artisans.';
  let sentiment = 'Warm, authentic, heritage-focused';
  let narrativeType = 'Cultural Heritage';

  if (
    lower.includes('बांस') || lower.includes('bamboo') || lower.includes('टोकरी') || lower.includes('basket') ||
    lower.includes('বাঁশ') || lower.includes('ঝুড়ি') || lower.includes('বাঁহ') || lower.includes('খৰাহী') ||
    lower.includes('बांबू') || lower.includes('टोपली') || lower.includes('மூங்கில்') || lower.includes('கூடை') ||
    lower.includes('వెదురు') || lower.includes('బుట్ట')
  ) {
    category = 'Bamboo & Cane Craft';
    material = 'Natural Assam Bamboo';
    dimensions = '30cm x 30cm x 20cm';
    productionTime = '3 days';
    story = 'Passed down through four generations in Silchar groves using sustainable harvest bamboo.';
    sentiment = 'Warm, authentic, eco-conscious';
    narrativeType = 'Cultural Heritage';
  } else if (
    lower.includes('रेशम') || lower.includes('silk') || lower.includes('दुपट्टा') || lower.includes('chanderi') || lower.includes('हथकरघ') ||
    lower.includes('রেশম') || lower.includes('মুগা') || lower.includes('रेशीम') || lower.includes('பட்டு') || lower.includes('చేనేత') || lower.includes('పట్టు')
  ) {
    category = 'Textiles & Handloom';
    material = 'Chanderi Silk Cotton';
    dimensions = '2.5m x 0.9m';
    productionTime = '7 days';
    story = 'Handwoven on traditional pit looms in Chanderi village reflecting royal court heritage.';
    sentiment = 'Elegant, luxury, traditional craftsmanship';
    narrativeType = 'Artisanal Mastery';
  } else if (
    lower.includes('लकड़ी') || lower.includes('wood') || lower.includes('हाथी') || lower.includes('elephant') || lower.includes('शीशम') ||
    lower.includes('কাঠ') || lower.includes('হাতি') || lower.includes('लाकूड') || lower.includes('हत्ती') || lower.includes('மரம்') || lower.includes('யானை') || lower.includes('చెక్క') || lower.includes('ఏనుగు')
  ) {
    category = 'Woodcraft';
    material = 'Sheesham Wood (Indian Rosewood)';
    dimensions = '15cm x 10cm x 22cm';
    productionTime = '5 days';
    story = 'Carved painstakingly by Saharanpur artisans using traditional chisel tools without modern machinery.';
    sentiment = 'Regal, durable, classic art';
    narrativeType = 'Heritage Craftsmanship';
  } else if (
    lower.includes('मिट्टी') || lower.includes('pottery') || lower.includes('blue') || lower.includes('फूलदान') || lower.includes('vase') ||
    lower.includes('মাটি') || lower.includes('মাটিৰ') || lower.includes('माती') || lower.includes('களிமண்') || lower.includes('మట్టి')
  ) {
    category = 'Pottery & Ceramics';
    material = 'Jaipur Blue Quartz Powder & Natural Pigments';
    dimensions = '18cm height x 12cm diameter';
    productionTime = '6 days';
    story = 'Jaipur Blue Pottery is crafted from quartz stone powder and glazed at low temperatures.';
    sentiment = 'Vibrant, historic, artistic excellence';
    narrativeType = 'Royal Heritage';
  }

  const title = product.title && product.title !== 'Handcrafted Artisan Craft' 
    ? product.title 
    : `Handcrafted ${material} ${category.split(' ')[0]}`;
  const description_english = `${title}. Elegantly shaped and detailed by master artisans. ${story}`;
  const description_hindi = `कुशल कारीगरों द्वारा निर्मित सुंदर और प्रामाणिक ${category}। ${story}`;
  const tags = Array.from(new Set([
    ...(product.tags || []),
    category.toLowerCase().replace(/[^a-z0-9]/g, '-'),
    'handicraft',
    'authentic',
    'vocal-for-local'
  ]));

  return {
    ...product,
    title,
    description_english,
    description_hindi,
    category,
    material,
    dimensions,
    production_time: productionTime,
    tags,
    story,
    sentiment,
    narrative_type: narrativeType,
    status: PRODUCT_STATUSES.READY
  };
}

function simulateEnhanceImage(product) {
  const currentImg = product.image_url;
  const enhanced = currentImg ? `${currentImg}${currentImg.includes('?') ? '&' : '?'}auto=format&fit=crop&w=1200&q=95&sat=10&con=5` : currentImg;
  return {
    ...product,
    enhanced_image_url: enhanced
  };
}

function simulatePricing(product) {
  let minPrice = 650;
  let maxPrice = 950;

  if (product.category === 'Textiles & Handloom') {
    minPrice = 1800;
    maxPrice = 2400;
  } else if (product.category === 'Woodcraft') {
    minPrice = 1200;
    maxPrice = 1650;
  } else if (product.category === 'Pottery & Ceramics') {
    minPrice = 950;
    maxPrice = 1400;
  }

  return {
    ...product,
    suggested_price_min: minPrice,
    suggested_price_max: maxPrice
  };
}

export const productService = {
  // Create Product
  async createProduct(productData) {
    const payload = {
      ...productData,
      status: productData.status || PRODUCT_STATUSES.PUBLISHED
    };
    try {
      return await request('/api/products', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
    } catch (e) {
      console.warn("Backend unavailable, saving product locally", e);
      const items = getStoredProducts();
      const newProduct = {
        ...payload,
        id: payload.id || `prod-${Date.now().toString(16)}`,
        created_at: new Date().toISOString(),
        suggested_price_min: payload.suggested_price_min || 500,
        suggested_price_max: payload.suggested_price_max || 1000
      };
      items.unshift(newProduct);
      setStoredProducts(items);
      return newProduct;
    }
  },

  // Save Draft
  async saveDraft(productData) {
    return await this.createProduct({
      ...productData,
      status: PRODUCT_STATUSES.DRAFT
    });
  },

  // Upload/Take Product Image (Checkpoint 3)
  async uploadProductImage(id, imageDataUrlOrFile) {
    try {
      // Try backend upload endpoint if supported
      return await request(`/api/products/${id}/upload-image`, {
        method: 'POST',
        body: JSON.stringify({ image_url: imageDataUrlOrFile })
      });
    } catch (e) {
      console.warn("Backend upload endpoint offline, updating local product image", e);
      const items = getStoredProducts();
      const index = items.findIndex(p => p.id === id);
      if (index !== -1) {
        items[index].image_url = imageDataUrlOrFile;
        setStoredProducts(items);
        return items[index];
      }
      return { id, image_url: imageDataUrlOrFile };
    }
  },

  // List all products with optional filters
  async listProducts({ category, artisan_id, status, q } = {}) {
    const params = new URLSearchParams();
    if (category && category !== 'all') params.append('category', category);
    if (artisan_id) params.append('artisan_id', artisan_id);
    if (q) params.append('q', q);

    try {
      let items = await request(`/api/products?${params.toString()}`);
      if (status && status !== 'all') {
        items = items.filter(p => (p.status || 'published').toLowerCase() === status.toLowerCase());
      }
      return items;
    } catch (e) {
      console.warn("Backend unavailable, using stored products", e);
      let items = getStoredProducts();
      if (category && category !== 'all') {
        items = items.filter(p => p.category?.toLowerCase() === category.toLowerCase());
      }
      if (artisan_id) {
        items = items.filter(p => p.artisan_id === artisan_id);
      }
      if (status && status !== 'all') {
        items = items.filter(p => (p.status || 'published').toLowerCase() === status.toLowerCase());
      }
      if (q) {
        const query = q.toLowerCase();
        items = items.filter(p => 
          p.title?.toLowerCase().includes(query) ||
          p.description_english?.toLowerCase().includes(query) ||
          p.description_hindi?.toLowerCase().includes(query) ||
          p.material?.toLowerCase().includes(query) ||
          p.category?.toLowerCase().includes(query) ||
          p.location?.toLowerCase().includes(query) ||
          p.tags?.some(t => t.toLowerCase().includes(query))
        );
      }
      return items;
    }
  },

  // Get product by ID
  async getProductById(id) {
    try {
      return await request(`/api/products/${id}`);
    } catch (e) {
      const items = getStoredProducts();
      const found = items.find(p => p.id === id);
      if (!found) throw new Error(`Product ${id} not found in local store`);
      return found;
    }
  },

  // Update existing product
  async updateProduct(id, updateData) {
    try {
      return await request(`/api/products/${id}`, {
        method: 'PUT',
        body: JSON.stringify(updateData)
      });
    } catch (e) {
      const items = getStoredProducts();
      const index = items.findIndex(p => p.id === id);
      if (index !== -1) {
        items[index] = { ...items[index], ...updateData };
        setStoredProducts(items);
        return items[index];
      }
      return updateData;
    }
  },

  // Update product status
  async updateProductStatus(id, status) {
    return await this.updateProduct(id, { status });
  },

  // Voice processing AI endpoint
  async processVoice(id, { audio_transcript, language = 'hi' }) {
    try {
      return await request(`/api/products/${id}/voice`, {
        method: 'POST',
        body: JSON.stringify({ audio_transcript, language })
      });
    } catch (e) {
      console.warn("Backend AI voice endpoint offline, simulating NLP extraction", e);
      const items = getStoredProducts();
      const index = items.findIndex(p => p.id === id);
      const current = index !== -1 ? items[index] : { id };
      const updated = simulateVoiceAI(current, audio_transcript, language);
      if (index !== -1) {
        items[index] = updated;
        setStoredProducts(items);
      }
      return updated;
    }
  },

  // Image Enhancement AI endpoint
  async enhanceImage(id, { image_url, prompt } = {}) {
    try {
      return await request(`/api/products/${id}/enhance-image`, {
        method: 'POST',
        body: JSON.stringify({ image_url, prompt })
      });
    } catch (e) {
      console.warn("Backend AI vision endpoint offline, simulating studio enhancement", e);
      const items = getStoredProducts();
      const index = items.findIndex(p => p.id === id);
      const current = index !== -1 ? items[index] : { id, image_url };
      const updated = simulateEnhanceImage({ ...current, image_url: image_url || current.image_url });
      if (index !== -1) {
        items[index] = updated;
        setStoredProducts(items);
      }
      return updated;
    }
  },

  // Generate Catalogue AI endpoint
  async generateCatalogue(id, { raw_notes } = {}) {
    try {
      return await request(`/api/products/${id}/generate-catalogue`, {
        method: 'POST',
        body: JSON.stringify({ raw_notes })
      });
    } catch (e) {
      console.warn("Backend AI catalogue endpoint offline, synthesizing catalogue", e);
      const items = getStoredProducts();
      const index = items.findIndex(p => p.id === id);
      const current = index !== -1 ? items[index] : { id };
      const updated = simulateVoiceAI(current, raw_notes || current.description_english || '');
      if (index !== -1) {
        items[index] = updated;
        setStoredProducts(items);
      }
      return updated;
    }
  },

  // Smart Pricing Calculation AI endpoint
  async calculatePrice(id, { raw_material_cost, labor_hours } = {}) {
    try {
      return await request(`/api/products/${id}/price`, {
        method: 'POST',
        body: JSON.stringify({ raw_material_cost, labor_hours })
      });
    } catch (e) {
      console.warn("Backend AI pricing endpoint offline, computing smart price", e);
      const items = getStoredProducts();
      const index = items.findIndex(p => p.id === id);
      const current = index !== -1 ? items[index] : { id };
      const updated = simulatePricing(current);
      if (index !== -1) {
        items[index] = updated;
        setStoredProducts(items);
      }
      return updated;
    }
  },

  // Artisan products feed
  async getArtisanProducts(artisan_id = 'art-001') {
    try {
      return await request(`/api/artisan/products?artisan_id=${artisan_id}`);
    } catch (e) {
      const items = getStoredProducts();
      return items.filter(p => !p.artisan_id || p.artisan_id === artisan_id);
    }
  },

  // Buyer products feed
  async getBuyerProducts({ category, q } = {}) {
    const params = new URLSearchParams();
    if (category && category !== 'all') params.append('category', category);
    if (q) params.append('q', q);

    try {
      return await request(`/api/buyer/products?${params.toString()}`);
    } catch (e) {
      return await this.listProducts({ category, q, status: 'published' });
    }
  }
};
