from typing import List

from ninja import Router, Schema

from .models import Category

router = Router()

########################################
# 7. Category Model: Get first active category by name (ASC)
########################################


class CategoryNameSlugOut(Schema):
    name: str
    slug: str


class ErrorResponse(Schema):
    detail: str


@router.get(
    "/category/first-active",
    tags=["module5"],
    summary="Retrieve the first active category by name ASC",
    response={200: CategoryNameSlugOut, 404: ErrorResponse},
)
def get_first_active_category_by_name(request):
    category = (
        Category.objects.only("name", "slug")
        .filter(is_active=True)
        .order_by("name")
        .first()
    )

    if category is None:
        return 404, {"detail": "No active categories found."}

    return {"name": category.name, "slug": category.slug}


########################################
# 6. Category Model: Sort active categories by name (ASC)
########################################


class CategoryNameSlugOut(Schema):
    name: str
    slug: str

class ErrorResponse(Schema):
    detail: str

@router.get(
    "/category/active-sorted-name",
    tags=["module5"],
    summary="Retrieve active categories sorted by name ASC",
    response={200: List[CategoryNameSlugOut], 404: ErrorResponse},
)
def get_active_categories_sorted_by_name(request):
    queryset = (
        Category.objects.only("name", "slug").filter(is_active=True).order_by("-name")
    )

    if not queryset.exists():
        return 404, {"detail": "No active categories found to sort."}

    results = [{"name": category.name, "slug": category.slug} for category in queryset]

    return results


########################################
# 5. Category Model: Exclude archived categories, return name & slug
########################################


class CategoryNameSlugOut(Schema):
    name: str
    slug: str


class ErrorResponse(Schema):
    detail: str


@router.get(
    "/category/active-excluding-archived",
    tags=["module5"],
    summary="Retrieve active categories excluding 'Archived'",
    response={200: List[CategoryNameSlugOut], 404: ErrorResponse},
)
def get_active_non_archived_categories(request):
    queryset = (
        Category.objects.only("name", "slug")
        .filter(is_active=True)
        .exclude(name="Clothes")
    )

    if not queryset.exists():
        return 404, {"detail": "No active categories found excluding 'Archived'."}

    results = [{"name": category.name, "slug": category.slug} for category in queryset]

    return results


########################################
# 4. Category Model: Return name & slug for inactive categories using only()
########################################


class CategoryNameSlugOut(Schema):
    name: str
    slug: str

class ErrorResponse(Schema):
    detail: str

@router.get(
    "/category/inactive-names",
    tags=["module5"],
    summary="Retrieve inactive category names and slugs using only()",
    response={200: List[CategoryNameSlugOut], 404: ErrorResponse},#multiple response
)
def get_inactive_category_names(request):
    queryset = Category.objects.only("name", "slug").filter(name="Electronics")

    if not queryset.exists():
        return 404, {"detail": "No inactive categories found with that name."}

    # Prepare data manually from model instances
    results = [{"name": category.name, "slug": category.slug} for category in queryset]

    return results


########################################
# 3. Category Model: Return name & slug using only()
########################################


class CategoryNameSlugOut(Schema):
    name: str
    slug: str


@router.get(
    "/category/names-optimized",
    tags=["module5"],
    summary="Retrieve category names and slugs using only()",
    response=List[CategoryNameSlugOut],
)
def get_category_names_optimized(request):
    queryset = Category.objects.only("name", "slug")

    # Prepare data manually from model instances
    results = [{"name": category.name, "slug": category.slug} for category in queryset]

    return results


########################################
# 2. Category Model: Return name & slug only
########################################


class CategoryNameSlugOut(Schema):
    name: str
    slug: str


@router.get(
    "/category/names",
    tags=["module5"],
    summary="Retrieve category names and slugs only",
    response=List[CategoryNameSlugOut],
)
def get_category_names(request):
    queryset = Category.objects.values("name", "slug")

    # Optional: modify or preprocess data
    results = [
        {"name": item["name"].upper(), "slug": item["slug"]} for item in queryset
    ]

    #results = list(queryset)
    return results


########################################
# 1. Category Model: Get all categories
########################################


class CategoryOut(Schema):
    id: int
    name: str
    slug: str
    is_active: bool
    level: int
    parent_id: int | None = None


@router.get(
    "/category/all",
    tags=["module5"],
    summary="Retrieve all categories",
    response=List[CategoryOut],
)
def get_all_categories(request):
    return Category.objects.all()
