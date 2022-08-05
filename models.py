from pydoc import describe
import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Set, Union


class Product(BaseModel):
    product_id: int = Field(...)
    slug: str = Field(...)
    title: str = Field(...)
    mrp: int = Field(...)
    discount_id: int = Field(...)
    description: str = Field(...)
    rating: int = Field(...)
    tag: str = Field(...)
    category: str = Field(...)
    sub_category: str = Field(...)
    brand: str = Field(...)
    score: int = Field(...)
    #image: Union[Image, None] = None
    #rating: int= Field(...)
    #date_created:datetime=Field() 
    is_active:bool=Field(...)
    

class ProductUpdate(BaseModel):
    title:Optional[str]
    description:Optional[str]
    category:Optional[str]
    mrp:Optional[int]


# class Image(BaseModel):
#     url: str
#     name: str 

class Varients(BaseModel):
    id: int = Field(...)
    product_id: int = Field(...)
    color:str = Field(...)
    size:int = Field(...)
    quantity:int = Field(...)
    #child_image:Union[Image, None] = None
    sku:int = Field(...)
    is_available:bool=Field(...)   


class sku(BaseModel):
    id: int = Field(...)
    verient_id: int = Field(...)
    quantity:int=Field(...)
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
    quantity:int = Field(...)
