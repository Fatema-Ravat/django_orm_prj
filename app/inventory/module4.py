from typing import List, Optional
from django.utils.text import slugify
from ninja import Router, Schema

from inventory.models import Category

router = Router()

class CategoryIn(Schema):
    name: str
    slug: str
    is_active: bool
    parent_id : str = None

@router.post(
    "/category/create",
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
    "/category/bulk_create",
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
    "category/update/{category_id}",
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
    "category/upsert",
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
    "/category/bulk-update",
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
    "/category/update/activate",
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

