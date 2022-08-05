from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from typing import Optional
from models import Product,ProductUpdate

router = APIRouter()

@router.post("/", response_description="Create a new product", status_code=status.HTTP_201_CREATED, response_model=Product)
def create_book(request: Request, item: Product = Body(...)):
    item = jsonable_encoder(item)
    item['is_active']=True
    new_product = request.app.database["trial_prod"].insert_one(item)
    created_product = request.app.database["trial_prod"].find_one(
        {"_id": new_product.inserted_id}
    )

    return created_product


@router.get("/", response_description="List all products", response_model=List[Product])
def list_products(request: Request,categotry:Optional[str]=None,
    brand:Optional[str]=None,min_range:Optional[int]=None,
    max_range:Optional[int]=None):

    ans=[]
    if categotry!=None:
        ans.append({'category':categotry})
    if brand!=None:
        ans.append({'brand':brand})
    if min_range!=None and max_range!=None:
        ans.append({ "$and": [ { 'mrp': { '$gt': min_range } }, { 'mrp': { '$lt': max_range } } ] })
    
    if len(ans)>=1:
        prod=list(request.app.database["trial_prod"].find({'$and':ans}))
        return prod
    else:
        prod =list(request.app.database["trial_prod"].find())
        return prod
    


@router.get("/{id}", response_description="Get a single product by product_id", response_model=Product)
def find_book(id: int, request: Request):
    if (prod := request.app.database["trial_prod"].find_one({"product_id": id})) is not None:
        return prod
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found")


@router.put("/{id}", response_description="Update a product", response_model=Product)
def update_product(id: int, request: Request, prod: ProductUpdate = Body(...)):
    item = {k: v for k, v in prod.dict().items() if v is not None}

    if len(item) >= 1:
        update_result = request.app.database["trial_prod"].update_one(
            {"product_id": id}, {"$set": item}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

    if (
        existing_product := request.app.database["trial_prod"].find_one({"product_id": id})
    ) is not None:
        return existing_product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"prodoct with ID {id} not found")


@router.put("/delete/{id}", response_description="Soft delete a product", response_model=Product)
def delete_product(id: int, request: Request):


    update_result = request.app.database["trial_prod"].update_one(
            {"product_id": id}, {"$set": {'is_active':False}}
        )

    if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

    if (
        existing_product := request.app.database["trial_prod"].find_one({"product_id": id})
    ) is not None:
        return existing_product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"prodoct with ID {id} not found")



