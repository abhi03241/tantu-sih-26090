// Craft Categories matching SIH 26090 Artisan Handicraft classification
export const CRAFT_CATEGORIES = [
  {
    id: 'all',
    nameEn: 'All Crafts',
    nameHi: 'सभी शिल्प',
    icon: 'Sparkles'
  },
  {
    id: 'Bamboo & Cane Craft',
    nameEn: 'Bamboo & Cane',
    nameHi: 'बांस और बेंत',
    icon: 'Trees',
    desc: 'Sustainable natural fiber crafts from North-East & Central India'
  },
  {
    id: 'Textiles & Handloom',
    nameEn: 'Textiles & Handloom',
    nameHi: 'हथकरघा और वस्त्र',
    icon: 'Shirt',
    desc: 'Pure silk, cotton weaves, Chanderi, Banarasi & Khadi'
  },
  {
    id: 'Woodcraft',
    nameEn: 'Woodcraft & Carving',
    nameHi: 'काष्ठशिल्प व नक्काशी',
    icon: 'Hammer',
    desc: 'Saharanpur Sheesham, Rosewood carving, and lacquerware'
  },
  {
    id: 'Pottery & Ceramics',
    nameEn: 'Pottery & Ceramics',
    nameHi: 'मिट्टी के बर्तन व पॉटरी',
    icon: 'Flame',
    desc: 'Jaipur Blue Pottery, terracotta clay utensils and vases'
  },
  {
    id: 'Metalcraft & Dhokra',
    nameEn: 'Metalcraft & Dhokra',
    nameHi: 'धातु शिल्प व ढोकरा',
    icon: 'Shield',
    desc: 'Ancient lost-wax brass casting from Bastar & Odisha'
  },
  {
    id: 'Tribal Folk Art',
    nameEn: 'Tribal Folk Art',
    nameHi: 'जनजातीय लोक चित्रकला',
    icon: 'Palette',
    desc: 'Madhubani, Warli, Gond and Pattachitra hand-paintings'
  }
];

// Sample demo artisan craft profiles for 1-click photo & voice test in hackathon
export const DEMO_SAMPLE_CRAFTS = [
  {
    id: 'sample-bamboo',
    title: 'Handcrafted North-East Bamboo Utility Basket',
    category: 'Bamboo & Cane Craft',
    material: 'Natural Assam Bamboo',
    imageUrl: 'https://images.unsplash.com/photo-1590736969955-71cc94801759?auto=format&fit=crop&w=800&q=80',
    enhancedImageUrl: 'https://images.unsplash.com/photo-1590736969955-71cc94801759?auto=format&fit=crop&w=1200&q=90',
    voiceTranscriptHi: 'यह असम के सिलचर में प्राकृतिक बांस से हाथ से बुनी गई टोकरी है। हमारे परिवार में चार पीढ़ियों से यह काम होता है। इसे बनाने में तीन दिन लगते हैं। फल रखने और सजावट के लिए बहुत मजबूत है।',
    voiceTranscriptEn: 'This is a handcrafted bamboo utility basket woven sustainably from natural bamboo groves in Silchar, Assam. Handcrafted across 3 days.',
    dimensions: '30cm x 30cm x 20cm',
    productionTime: '3 days',
    suggestedMin: 650,
    suggestedMax: 950,
    story: 'Passed down through four generations in Silchar groves using sustainable harvest bamboo.',
    sentiment: 'Warm, authentic, heritage-focused',
    narrativeType: 'Cultural Heritage',
    tags: ['bamboo', 'eco-friendly', 'handicraft', 'home-decor', 'northeast-art']
  },
  {
    id: 'sample-chanderi',
    title: 'Chanderi Handwoven Silk Cotton Dupatta with Zari Border',
    category: 'Textiles & Handloom',
    material: 'Chanderi Silk Cotton',
    imageUrl: 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80',
    enhancedImageUrl: 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=1200&q=90',
    voiceTranscriptHi: 'यह मध्य प्रदेश के चंदेरी में हथकरघे पर बुनी गई शुद्ध रेशम और सूती दुपट्टा है। किनारों पर सुनहरी जरी का काम है। इसे एक सप्ताह में तैयार किया गया है।',
    voiceTranscriptEn: 'Traditional handwoven Chanderi silk cotton dupatta featuring regal golden zari border woven on handlooms over 7 days in Madhya Pradesh.',
    dimensions: '2.5m x 0.9m',
    productionTime: '7 days',
    suggestedMin: 1800,
    suggestedMax: 2400,
    story: 'Handwoven on traditional pit looms in Chanderi village reflecting royal court heritage.',
    sentiment: 'Elegant, luxury, traditional craftsmanship',
    narrativeType: 'Artisanal Mastery',
    tags: ['handloom', 'chanderi', 'silk', 'ethnic-wear', 'zari']
  },
  {
    id: 'sample-wood',
    title: 'Saharanpur Carved Wooden Royal Elephant Figurine',
    category: 'Woodcraft',
    material: 'Sheesham Wood (Indian Rosewood)',
    imageUrl: 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=800&q=80',
    enhancedImageUrl: 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1200&q=90',
    voiceTranscriptHi: 'सहारनपुर के प्रसिद्ध शीशम की लकड़ी से हाथ की छेनी से तराशी गई हाथी की प्रतिमा है। इसमें पीतल के बारीक काम की जड़ाई की गई है। पांच दिन का कठिन श्रम लगा है।',
    voiceTranscriptEn: 'Hand-carved royal elephant sculpture crafted in Saharanpur using seasoned Sheesham wood and brass inlay, made without machine tools across 5 days.',
    dimensions: '15cm x 10cm x 22cm',
    productionTime: '5 days',
    suggestedMin: 1200,
    suggestedMax: 1650,
    story: 'Carved painstakingly by Saharanpur master woodworkers using heirloom chisel tools.',
    sentiment: 'Regal, durable, classic art',
    narrativeType: 'Heritage Craftsmanship',
    tags: ['woodcraft', 'carved', 'sheesham', 'elephant', 'brass-inlay']
  },
  {
    id: 'sample-pottery',
    title: 'Traditional Jaipur Blue Pottery Floral Ceramic Vase',
    category: 'Pottery & Ceramics',
    material: 'Jaipur Blue Quartz Powder & Natural Pigments',
    imageUrl: 'https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=800&q=80',
    enhancedImageUrl: 'https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=1200&q=90',
    voiceTranscriptHi: 'यह जयपुर की प्रसिद्ध नीली मिट्टी की कलाकारी है जिसमें बिना मिट्टी के केवल क्वार्ट्ज पत्थर और प्राकृतिक रंगों से फूलदान बनाया गया है। छह दिन में हाथ से चित्रकारी हुई है।',
    voiceTranscriptEn: 'Authentic Jaipur Blue Pottery decorative vase crafted without clay from quartz stone powder, handpainted with traditional Mughal floral motifs.',
    dimensions: '18cm height x 12cm diameter',
    productionTime: '6 days',
    suggestedMin: 950,
    suggestedMax: 1400,
    story: 'Crafted in Jaipur using low-fire quartz and Egyptian glaze techniques brought to Rajasthan.',
    sentiment: 'Vibrant, historic, artistic excellence',
    narrativeType: 'Royal Heritage',
    tags: ['blue-pottery', 'jaipur', 'ceramic', 'vase', 'handpainted']
  }
];
