from typing import List, Optional
from django.utils.text import slugify
from ninja import Router, Schema

from inventory.models import Category,Product,StockManagement,Order,OrderProduct,PromotionEvent,ProductPromotionEvent
from django.contrib.auth.models import User

import datetime
from django.utils import dateparse

router = Router()

class CategoryIn(Schema):
    name: str
    slug: str
    is_active: bool
    parent_id : str = None

@router.post(
    "/category/create/",
    tags = ["module4"],
    summary="Create new Category",
    description = "Creates a new category with optional parent name and slug.Slug is autogenrated",
)

def create_category(request, data:CategoryIn):
    slug = data.slug or slugify(data.name)
    parent_id = data.parent_id
    if data.parent_id:
        parent_id = Category.objects.get(name=data.parent_id)

    Category.objects.create(name=data.name,
                            slug=slug,
                            is_active=data.is_active,
                            parent_id=parent_id)
    return

@router.post(
    "/category/bulk_create/",
    tags =["module4"],
    summary = "Create new Categories in bulk",
    description ="Bulk creation of new Categories with bulk_create method"
)
def bulk_create_category(request, data:List[CategoryIn]):
    cats=[
        Category(
            name=item.name,
            slug=item.slug,
            is_active=item.is_active,
            parent_id=Category.objects.filter(name=item.parent_id).first()
       )
        for item in data
    ]
    Category.objects.bulk_create(cats)
    return

class CategoryUpdateIn(Schema):
    name:Optional[str] =None
    slug :Optional[str] =None
    is_active :Optional[bool] =None
    parent_id :Optional[str] =None
    
@router.put(
    "category/update/{category_id}/",
    tags=["module4"],
    summary = "Update data for a category",
    description = "Update data for a given category"
)
def update_category(request, category_id:int, data:CategoryUpdateIn):
    try:
        cat = Category.objects.get(id = category_id)
    except Category.DoesNotExist:
        return {"error" : "Category not found"}
    
    updated_fields =[]
    if data.name is not None:
        cat.name = data.name
        updated_fields.append("name")
    if data.slug is not None:
        cat.slug = data.slug
        updated_fields.append("slug")
    if data.is_active is not None:
        cat.is_active = data.is_active
        updated_fields.append("is_active")
    if data.parent_id is not None:
        cat.parent_id = Category.objects.filter(name=data.parent_id).first()
        updated_fields.append("parent_id")

    
    cat.save(update_fields=updated_fields)
    return {"status":"updated"}

class CategoryUpsertIn(Schema):
    name:str
    slug :Optional[str] =None
    is_active :Optional[bool] =True
    parent_id :Optional[str] =None
@router.put(
    "category/upsert/",
    tags=["module4"],
    summary = "Update/Create data for a category",
    description = "Update/create data for a given category by name using update_or_create"
)
def upsert_category(request, data:CategoryUpsertIn):
    slug = data.slug or slugify(data.name)

    cat,created = Category.objects.update_or_create(name=data.name,
                                      defaults={
                                          "slug":slug,
                                          "is_active":data.is_active,
                                          "parent_id":Category.objects.filter(name=data.parent_id).first()
                                      })
    
    return {"status":"created" if created else "updated",
            "id":cat.id,
            "name": cat.name}

# --- Schema for bulk_update() usage ---
class CategoryBulkUpdateIn(Schema):
    id: int
    level: int
    is_active: Optional[bool] = None


@router.put(
    "/category/bulk-update/",
    tags=["module4"],
    summary="Bulk update status and level using .bulk_update()",
)
def bulk_update_categories(request, data: List[CategoryBulkUpdateIn]):
    ids = [item.id for item in data]
    category_map = {item.id: item for item in data}

    categories = Category.objects.filter(id__in=ids)

    for cat in categories:
        item = category_map.get(cat.id) #easy way to get object with corresponding id
        if item:
            cat.level = item.level
            if item.is_active is not None:
                cat.is_active = item.is_active

    Category.objects.bulk_update(categories, ["level", "is_active"])

    return {
        "status": "bulk_updated",
        "updated_count": len(categories),
    }

# --- Schema for simple update() usage ---
class CategoryActivateFilterIn(Schema):
    level: Optional[int] = None
    is_active: Optional[bool] = False


@router.put(
    "/category/update/activate/",
    tags=["module4"],
    summary="Activate categories using .update() on filtered queryset",
)
def activate_categories(request, data: CategoryActivateFilterIn):
    filters = {"is_active": data.is_active}

    if data.level is not None:
        filters["level"] = data.level

    updated_count = Category.objects.filter(**filters).update(is_active=False)

    return {
        "status": "updated",
        "updated_count": updated_count,
    }

#----Schema for creating a product-----

class ProductCreateIn(Schema):
    name : str
    slug : str
    description : str
    is_digital : Optional[bool] = False
    is_active : Optional[bool] = True
    price : float
    category_id : int #client provides category_id integer

@router.post(
    "/product/create/",
    tags=["module4"],
    summary="Create a New Product",
)
def create_product(request, data:ProductCreateIn):
    try:
        cat = Category.objects.get(id= data.category_id)
    except Category.DoesNotExist:
        return{"error":"No category for given category_id exists"}
    
    
    prod = Product.objects.create(name=data.name,
                                  slug= data.slug,
                                  description = data.description,
                                  price = data.price,
                                  is_digital = data.is_digital,
                                  is_active = data.is_active,
                                  category_id_id = data.category_id)
    
    """ other way to give category object
    prod = Product(name=data.name,
                                  slug= data.slug,
                                  description = data.description,
                                  price = data.price,
                                  is_digital = data.is_digital,
                                  is_active = data.is_active,
                                  category_id = cat)
    prod.save()
    """
    return {"status": "created", "product": data.name}

# ----Schema for stock management of product ----

class ProductCreateWithStockIn(Schema):
    name : str
    slug : str
    description : str
    is_digital : Optional[bool] = False
    is_active : Optional[bool] = True
    price : float
    category_id : int #client provides category_id integer
    stock_quantity: int 

@router.post(
    'create/product_with_stock/',
    tags=["module4"],
    summary="Create a New Product with its stock in StockManagement table",
    
)
def create_product_with_stock(request,data:ProductCreateWithStockIn):
    try:
        cat = Category.objects.get(id= data.category_id)
    except Category.DoesNotExist:
        return{"error":"No category for given category_id exists"}
    
    
    prod = Product.objects.create(name=data.name,
                                  slug= data.slug,
                                  description = data.description,
                                  price = data.price,
                                  is_digital = data.is_digital,
                                  is_active = data.is_active,
                                  category_id_id = data.category_id)
    
    stock = StockManagement.objects.create(product=prod,quantity=data.stock_quantity)
    return{"status":"created",
           "product":prod.name,
           "stock": stock.quantity}

# Order + Products: Using through model
class OrderedProductIn(Schema):
    product_id: int
    quantity: int


class OrderWithProductsIn(Schema):
    user_id: int
    products: List[OrderedProductIn]

@router.post(
    "/order/create/",
    tags=["module4"],
    summary="Create order using .add() and through_defaults",
)
def create_order(request, data: OrderWithProductsIn):
    try:
        user = User.objects.get(id=data.user_id)
    except User.DoesNotExist:
        return {"error": "User not found."}

    order = Order.objects.create(user=user)

    for item in data.products:
        try:
            product = Product.objects.get(id=item.product_id)

            # Check if relation already exists to avoid unique constraint failure
            exists = OrderProduct.objects.filter(order=order, product=product).exists()
            if not exists:
                order.products.add(
                    product, through_defaults={"quantity": item.quantity}
                )
            # optionally: else update the quantity or skip silently
        except Product.DoesNotExist:
            continue

    """
    without products manytomanyfield defined

    for item in data.products:
        try:
            product = Product.objects.get(id=item.product_id)
            OrderProduct.objects.create(order=order,product=product,quantity=item.quantity)
        except Product.DoesNotExist:
            continue
    """


    return {
        "status": "created",
        "order_id": order.id,
        "linked_products": len(data.products),
    }

# product promotion apis

class ProductPromotionIn(Schema):
    product_id: int

class PromotionWithProductsIn(Schema):
    name: str
    start_date : str
    end_date : str
    price_reduction : int
    products: List[ProductPromotionIn]

@router.post(
    "/promotion/create/",
    tags=["module4"],
    summary="Create promotion event. Give date in format yyyy-mm-dd. price reduction from [5,10,20]",
)
def create_promotion(request, data: PromotionWithProductsIn):

    promotion = PromotionEvent.objects.create(name= data.name, 
                                            start_date= dateparse.parse_date(data.start_date),
                                            end_date = dateparse.parse_date(data.end_date),
                                            price_reduction = data.price_reduction)

    for item in data.products:
        try:
            product = Product.objects.get(id=item.product_id)

            # Check if relation already exists to avoid unique constraint failure
            exists = ProductPromotionEvent.objects.filter(promotion_event=promotion, 
                                        product=product).exists()
            if not exists:
                promotion.products.add(
                    product
                )
            # optionally: else update the quantity or skip silently
        except Product.DoesNotExist:
            continue

    return {
        "status": "created",
        "promotion_id": promotion.id,
        "linked_products": len(data.products),
    }


# Delete on models.

class ProductBulkDeleteIn(Schema):
    ids: List[int] # product ids to delete

@router.delete(
    "/product/bulk-delete/",
    tags=["module4"],
    summary="Bulk delete categories by IDs",
)
def bulk_delete_categories(request, data: ProductBulkDeleteIn):
    queryset = Product.objects.filter(id__in=data.ids) 
    # for bulk delete make a queryset then call delete() on queryset
    if not queryset.exists():
        return {"error": "No matching categories found to delete."}

    deleted_count, deleted_detail = queryset.delete()

    return {
        "status": "bulk_deleted",
        "deleted_count": deleted_count,
        "detail": deleted_detail,
    }


@router.delete(
    "/category/delete/{category_id}",
    tags=["module4"],
    summary="Delete a category by ID",
)
def delete_category(request, category_id: int):
    try:
        category = Category.objects.get(id=category_id)
        deleted_count, deleted_detail = category.delete()
        return {
            "status": "deleted",
            "deleted_count": deleted_count,
            "category_id": category_id,
            "detail": deleted_detail,
        }
    except Category.DoesNotExist:
        return {"error": "Category not found."}
