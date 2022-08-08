from itertools import product
from fastapi import APIRouter, Body, Request, Response, HTTPException, status,Query
from fastapi.encoders import jsonable_encoder
from typing import List
from fastapi_pagination import Page
from typing import Optional
from models import Product,ProductUpdate, Varients
from fastapi import File,UploadFile
router = APIRouter()

@router.post("/", response_description="Create a new product", status_code=status.HTTP_201_CREATED, response_model=Product)
def create_prod(request: Request, item: Product = Body(...)):
    item = jsonable_encoder(item)
    item['is_active']=True
    new_product = request.app.database["trial_prod"].insert_one(item)
    created_product = request.app.database["trial_prod"].find_one(
        {"_id": new_product.inserted_id}
    )
    if created_product is not None:
        return created_product
    

# @router.post("/{id}/varient/", response_description="Create a new product", status_code=status.HTTP_201_CREATED, response_model=Product)
# def create_var(request: Request, item: Varients = Body(...)):
#     item = jsonable_encoder(item)
#     item['is_active']=True
#     new_var = request.app.database["trial_var"].insert_one(item)
#     created_var = request.app.database["trial_var"].find_one(
#         {"_id": new_product.inserted_id}
#     )

#     return created_var


@router.get("/", response_description="List all products",status_code=status.HTTP_200_OK, response_model=List[Product])
def list_products(request: Request,categotry:List[str] = Query(None),
    brand:List[str] = Query(None),min_range:Optional[int]=None,
    max_range:Optional[int]=None,Sort: List[str] = Query(None)):
    ans=[]
    list_cate=[]
    list_brand=[]
    if categotry is not None:
        for i in categotry:
            list_cate.append({'category':i})
    if brand is not None:
        for i in brand:
            list_brand.append({'brand':i})
    print(list_brand)
    print(list_cate)
    sort_query={}
    if Sort is not None:
        for i in Sort:
            sort_query[i]=1
    ans=[]

    

    if list_cate is not None:
        ans.append({'$or':list_cate})
    if list_brand is not None:
        ans.append({'$or':list_brand})
    if min_range!=None and max_range!=None:
        ans.append({ "$and": [ { 'mrp': { '$gt': min_range } }, { 'mrp': { '$lt': max_range } } ] })
    if len(ans)>=1:
        prod =list(request.app.database["trial_prod"].aggregate([
            { '$match' : { '$and' : ans } },
            #{ '$sort' : sort_query}
        ]))
        return prod
    # else:
    #     print('hello')
    #     print('hello')
    #     print('hello')
    #     prod =list(request.app.database["trial_prod"].aggregate([
    #         { '$match' : {  }}
    #     ]))
    #     return prod





# @router.get("/search", response_description="List all products", response_model=List[Product])
# def search(request:Request, search_char:str):
#     prod =list(request.app.database["trial_prod"].find({ '$text':{'$search' :search_char}}))
#     return prod

@router.get("/search", response_description="List all products", response_model=List[Product])
def search(request:Request, search_char:str):
    prod =list(request.app.database["trial_prod"].find({"$or" : [{ 'title':{'$regex' :search_char, '$options': "i"}},
     {'brand':{'$regex' :search_char, '$options': "i"}},
     {'category':{'$regex' :search_char, '$options': "i"}}]}))
    return prod
    


@router.get("/{id}", response_description="Get a single product by product_id", response_model=Product)
def find_product(id: int, request: Request):
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found")

    if (
        existing_product := request.app.database["trial_prod"].find_one({"product_id": id})
    ) is not None:
        return existing_product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"prodoct with ID {id} not found")



