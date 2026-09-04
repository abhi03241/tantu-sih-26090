from pydantic import BaseModel, Field
from typing import List, Optional


# ==========================================
# COMMON PRODUCT CONTRACT (M, R, S & Frontend)
# ==========================================
class ProductBase(BaseModel):
    title: str = Field(..., example="Handcrafted North-East Bamboo Utility Basket")
    description_english: Optional[str] = Field("", example="Woven natural bamboo basket crafted by master artisans.")
    description_hindi: Optional[str] = Field("", example="असम के कुशल कारीगरों द्वारा निर्मित बांस की टोकरी।")
    category: str = Field(..., example="Bamboo & Cane Craft")
    material: str = Field(..., example="Natural Bamboo")
    dimensions: Optional[str] = Field(None, example="30cm x 30cm x 20cm")
    production_time: Optional[str] = Field(None, example="3 days")
    tags: List[str] = Field(default_factory=list, example=["bamboo", "eco-friendly", "handicraft"])
    story: Optional[str] = Field(None, example="Heritage technique passed down through 4 generations.")
    sentiment: Optional[str] = Field(None, example="Authentic, heritage-focused")
    narrative_type: Optional[str] = Field(None, example="Cultural Heritage")
    image_url: Optional[str] = Field("", example="https://images.unsplash.com/photo-1590736969955-71cc94801759")
    enhanced_image_url: Optional[str] = Field(None, example="https://images.unsplash.com/photo-1590736969955-71cc94801759?w=1200")
    suggested_price_min: Optional[float] = Field(None, example=650.0)
    suggested_price_max: Optional[float] = Field(None, example=950.0)


    # Extra helper fields for artisan context
    artisan_id: Optional[str] = Field("art-001", example="art-001")
    artisan_name: Optional[str] = Field(None, example="Lakshmi Devi")
    location: Optional[str] = Field(None, example="Silchar, Assam")
    status: Optional[str] = Field("draft", example="ready")  # draft, processing, ready, published, failed


class ProductCreate(BaseModel):
    title: Optional[str] = Field("Artisan Product", example="Handcrafted North-East Bamboo Utility Basket")
    description_english: Optional[str] = Field(None, example="Woven natural bamboo basket crafted by master artisans.")
    description_hindi: Optional[str] = Field(None, example="असम के कुशल कारीगरों द्वारा निर्मित बांस की टोकरी।")
    category: Optional[str] = Field("Handicraft", example="Bamboo & Cane Craft")
    material: Optional[str] = Field("Natural Material", example="Natural Bamboo")
    dimensions: Optional[str] = Field(None, example="30cm x 30cm x 20cm")
    production_time: Optional[str] = Field(None, example="3 days")
    tags: Optional[List[str]] = Field(default_factory=list, example=["bamboo", "eco-friendly"])
    story: Optional[str] = Field(None, example="Heritage technique passed down through 4 generations.")
    sentiment: Optional[str] = Field(None, example="Authentic, heritage-focused")
    narrative_type: Optional[str] = Field(None, example="Cultural Heritage")
    image_url: Optional[str] = Field(None, example="https://images.unsplash.com/photo-1590736969955-71cc94801759")
    enhanced_image_url: Optional[str] = Field(None, example="https://images.unsplash.com/photo-1590736969955-71cc94801759?w=1200")
    suggested_price_min: Optional[float] = Field(None, example=650.0)
    suggested_price_max: Optional[float] = Field(None, example=950.0)
    artisan_id: Optional[str] = Field("art-001", example="art-001")
    artisan_name: Optional[str] = Field(None, example="Lakshmi Devi")
    location: Optional[str] = Field(None, example="Silchar, Assam")
    status: Optional[str] = Field("draft", example="draft")


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description_english: Optional[str] = None
    description_hindi: Optional[str] = None
    category: Optional[str] = None
    material: Optional[str] = None
    dimensions: Optional[str] = None
    production_time: Optional[str] = None
    tags: Optional[List[str]] = None
    story: Optional[str] = None
    sentiment: Optional[str] = None
    narrative_type: Optional[str] = None
    image_url: Optional[str] = None
    enhanced_image_url: Optional[str] = None
    suggested_price_min: Optional[float] = None
    suggested_price_max: Optional[float] = None
    artisan_id: Optional[str] = None
    status: Optional[str] = None


class ProductResponse(ProductBase):
    id: str = Field(..., example="prod-bamboo-001")
    created_at: Optional[str] = None


# ==========================================
# USER & ARTISAN & BUYER MODELS
# ==========================================
class UserBase(BaseModel):
    name: str = Field(..., example="Lakshmi Devi")
    phone: str = Field(..., example="+91-9876543210")
    role: str = Field(..., example="artisan")  # artisan or buyer
    region: Optional[str] = Field(None, example="Assam")


class UserResponse(UserBase):
    id: str


class ArtisanProfileBase(BaseModel):
    user_id: str
    artisan_name: str
    craft_type: str
    location: str
    bio: Optional[str] = None
    phone: Optional[str] = None
    story_style: Optional[str] = "Cultural Heritage"


class ArtisanProfileResponse(ArtisanProfileBase):
    id: str


class BuyerBase(BaseModel):
    user_id: str
    buyer_name: str
    organization: Optional[str] = None
    buyer_type: str = "B2B"  # B2B, B2C, Wholesaler
    contact_email: str


class BuyerResponse(BuyerBase):
    id: str


# ==========================================
# ORDER REQUEST CONTRACT
# ==========================================
class OrderRequestCreate(BaseModel):
    product_id: str = Field(..., example="prod-bamboo-001")
    buyer_name: str = Field(..., example="Kraft Emporium Retailers")
    buyer_contact: str = Field(..., example="procurement@kraftemporium.com / +91-9988776655")
    quantity: int = Field(..., example=50)
    notes: Optional[str] = Field(None, example="Need custom eco-friendly packaging for export order.")
    price_offered: Optional[float] = Field(None, example=850.0)


class OrderRequestResponse(OrderRequestCreate):
    id: str
    product_title: Optional[str] = None
    artisan_id: Optional[str] = None
    status: str = Field("pending", example="pending")  # pending, accepted, fulfilled
    created_at: str


# ==========================================
# AI ACTION PAYLOADS & RESPONSES
# ==========================================
class VoiceProcessingRequest(BaseModel):
    audio_transcript: Optional[str] = Field(None, example="यह बांस की टोकरी है जो असम में बनाई गई है। यह 3 दिन में बनती है।")
    language: Optional[str] = Field("hi", example="hi")


class EnhanceImageRequest(BaseModel):
    image_url: Optional[str] = Field(None, example="https://images.unsplash.com/photo-1590736969955-71cc94801759")
    prompt: Optional[str] = Field(None, example="Clean white studio background with soft lighting")


class GenerateCatalogueRequest(BaseModel):
    raw_notes: Optional[str] = Field(None, example="Handwoven silk dupatta from Chanderi with golden zari work.")


class PricingRequest(BaseModel):
    raw_material_cost: Optional[float] = Field(None, example=250.0)
    labor_hours: Optional[int] = Field(None, example=16)


class ProcessProductRequest(BaseModel):
    audio_transcript: Optional[str] = Field(None, example="Ye bamboo ki tokri hai. Isko banane mein do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha.")
    image_url: Optional[str] = Field(None, example="https://images.unsplash.com/photo-1590736969955-71cc94801759")
    prompt: Optional[str] = Field(None, example="Clean white studio background with soft lighting")
    raw_material_cost: Optional[float] = Field(None, example=250.0)
    language: Optional[str] = Field("hi", example="hi")
    artisan_id: Optional[str] = Field("art-001", example="art-001")


class ProcessProductResponse(BaseModel):
    id: str = Field(..., example="prod-001")
    status: str = Field("ready", example="ready")
    product: ProductResponse
    errors: Optional[dict] = Field(None, example=None)


class ProductStatusResponse(BaseModel):
    id: str = Field(..., example="prod-001")
    status: str = Field("ready", example="ready")


