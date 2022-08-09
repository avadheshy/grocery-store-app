
from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query,FastAPI
from fastapi.encoders import jsonable_encoder
from typing import List
from fastapi_pagination import Page,LimitOffsetPage,paginate,add_pagination
from typing import Optional
from models import Product, ProductUpdate, Variants
from fastapi import File, UploadFile
router = APIRouter()

@router.post("/", response_description="Create a new product", status_code=status.HTTP_201_CREATED, response_model=Product)
def create_prod(request: Request, item: Product = Body(...)):
    item = jsonable_encoder(item)
    item['is_active'] = True
    new_product = request.app.database["trial_prod"].insert_one(item)
    created_product = request.app.database["trial_prod"].find_one(
        {"_id": new_product.inserted_id}
    )
    if created_product is not None:
        return created_product
@router.post("/variant", response_description="Create a new product", status_code=status.HTTP_201_CREATED, response_model=Variants)
def add_variant(request: Request, item: Variants = Body(...)):
    item = jsonable_encoder(item)

    new_product = request.app.database["varients"].insert_one(item)
    created_product = request.app.database["varients"].find_one(
        {"_id": new_product.inserted_id}
    )
    if created_product is not None:
        return created_product


@router.get("/", response_description="List all products", status_code=status.HTTP_200_OK, response_model=list[Product])
def list_products(request: Request, Categotry: list[str] = Query(None),
                  Brand: list[str] = Query(None), min_range: Optional[int] = None,
                  max_range: Optional[int] = None, Sort: list[str] = Query(None)):
    sort_list = []
    if Sort is not None:
        for i in range(len(Sort)):
            sort_list.append((Sort[i], 1))
    ans = []
    category_list = []
    if Categotry is not None:
        for i in Categotry:
            if i is not None:
                category_list.append({'category': i})
        if len(category_list) > 0:
            ans.append({"$or": category_list})
    brand_list = []
    if Brand is not None:
        for i in Brand:
            if i is not None:
                brand_list.append({'brand': i})

        if len(brand_list) > 0:
            ans.append({"$or": brand_list})
    if min_range != None and max_range != None:
        ans.append(
            {"$and": [{'mrp': {'$gt': min_range}}, {'mrp': {'$lt': max_range}}]})
    ans.append({'is_active':True})
    print(ans)
    if Sort != None:
        if len(ans) >= 1:
            prod = list(request.app.database["trial_prod"].find(
                {'$and': ans}).sort(sort_list))
            return prod
        else:
            prod = list(request.app.database["trial_prod"].find(
                {}).sort(sort_list))
            return prod
    else:
        if len(ans) >= 1:
            prod = list(request.app.database["trial_prod"].find({'$and': ans}))
            return prod
        else:
            prod = list(request.app.database["trial_prod"].find({}))
            return prod


@router.get("/search", response_description="List all products", status_code=status.HTTP_200_OK,response_model=List[Product])
def search(request: Request, search_char: str):
    prod = list(request.app.database["trial_prod"].find({"$or": [{'title': {'$regex': search_char, '$options': "i"}},
            {'brand': {
            '$regex': search_char, '$options': "i"}},
            {'category': {'$regex': search_char, '$options': "i"}}]}))
    return prod


@router.get("/{id}", response_description="Get a single product by product_id",status_code=status.HTTP_200_OK, response_model=Product)
def find_product(id: int, request: Request):
    if (prod := request.app.database["trial_prod"].find_one({"product_id": id,'is_active':True})) is not None:
        return prod
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product with ID {id} not found")

# #@router.get("/products",response_model=Page[Product])
# @router.get("/products/limit-offset",response_model=LimitOffsetPage[Product])
# def find(request: Request):
#     prod=paginate(list(request.app.database["trial_prod"].find({})))
#     return prod


@router.put("/{id}", response_description="Update a product", status_code=status.HTTP_205_RESET_CONTENT, response_model=Product)
def update_product(id: int, request: Request, prod: ProductUpdate = Body(...)):
    item = {k: v for k, v in prod.dict().items() if v is not None}

    if len(item) >= 1:
        update_result = request.app.database["trial_prod"].update_one(
            {"product_id": id}, {"$set": item}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with ID {id} not found")

    if (
        existing_product := request.app.database["trial_prod"].find_one({"product_id": id})
    ) is not None:
        return existing_product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"prodoct with ID {id} not found")


@router.put("/delete/{id}", response_description="Soft delete a product",status_code=status.HTTP_202_ACCEPTED, response_model=Product)
def delete_product(id: int, request: Request):

    update_result = request.app.database["trial_prod"].update_one(
        {"product_id": id}, {"$set": {'is_active': False}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with ID {id} not found")

    if (
        existing_product := request.app.database["trial_prod"].find_one({"product_id": id})
    ) is not None:
        return existing_product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"prodoct with ID {id} not found")
