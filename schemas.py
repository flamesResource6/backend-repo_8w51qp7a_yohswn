"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Advisor(BaseModel):
    """
    Spiritual advisor profile
    Collection name: "advisor"
    """
    name: str = Field(..., description="Advisor name")
    specialties: List[str] = Field(default_factory=list, description="Areas of focus")
    bio: Optional[str] = Field(None, description="Short biography")
    rating: Optional[float] = Field(4.8, ge=0, le=5)
    photo: Optional[str] = Field(None, description="Avatar URL")

class Booking(BaseModel):
    """
    Booking requests for spiritual advice
    Collection name: "booking"
    """
    name: str = Field(..., description="Client full name")
    email: EmailStr = Field(..., description="Client email")
    topic: str = Field(..., description="What do you seek guidance on?")
    preferred_time: Optional[str] = Field(None, description="Preferred date/time or timezone")
    advisor_id: Optional[str] = Field(None, description="Chosen advisor ID")
    notes: Optional[str] = Field(None, description="Additional context")
    status: str = Field("pending", description="Booking status: pending, confirmed, completed, cancelled")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
