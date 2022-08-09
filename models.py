from typing import Union
import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Set, Union
from fastapi import File, UploadFile


class Product(BaseModel):
    product_id: int = Field(gte=0 ,title="product id must be greater than or equal to zero")
    slug: str = Field(default=None, max_length=100)
    title: str= Field(default=None, max_length=100)
    mrp: int = Field(gt=0,title="mrp must be grater than zero")
    discount_id: int = Field(gte=0,title="discount must be grater or equal than zero")
    description: str = Field(default=None,max_length=100)
    rating: int = Field(gte=0,title="rating must be less than or equal to 5")
    tag:str = Field(default=None,max_length=100)
    category: str= Field(default=None,max_length=100)
    sub_category: str = Field(default=None,max_length=100)
    brand: str = Field(default=None,max_length=100)
    score: int = Field(gte=0,lte=20,title="score must be range of 0 to 20")
    #img: bytes  =File(...)
    #rating: int= Field(...)
    # date_created:datetime=Field()
    is_active: bool = Field(...)

    class config:
        orm_mode = True


class ProductUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    category: Optional[str]
    mrp: Optional[int]
    is_active:Optional[bool]


# class Image(BaseModel):
#     url: str
#     name: str

class Variants(BaseModel):
    id: int = Field(gte=0 )
    product_id: int = Field(gte=0)
    color: str = Field(default=None, title="The description of the item", max_length=100)
    size: int = Field(gte=0,title="size must be grater or equal than zero")
    quantity: int = Field(gte=0,title="quantity must be grater or equal than zero")
    sku: int = Field(gte=0,title="sku must be grater or equal than zero")
    is_available: bool = Field(...)
    class Config:
    	orm_mode=True


class sku(BaseModel):
    id: int = Field(...)
    varient_id: int = Field(...)
    quantity: int = Field(...)
    suplier_id: str = Field(...)


class discount(BaseModel):
    discount_type: str = Field(...)
    discount: int = Field(...)
    tax: int = Field(...)


class inventry(BaseModel):
    id: int = Field(...)
    varient_id: int = Field(...)
    sku: int = Field(...)
    address: str = Field(...)
    quantity: int = Field(...)
