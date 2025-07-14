from typing import List, Optional
from ninja import Router,Schema, Query
from .models import Product , Category

from django.db.models import Q

router = Router()

class ParentCategoryOut(Schema):
    id :int
    name :str
    slug :str

class CategorySchemaOut(Schema):
    id:int
    name :str
    slug : str
    is_active :bool
    level : int
    #parent_id :Optional[ParentCategoryOut] -- one way
    parent_id : Optional[int]

    @staticmethod
    def resolve_parent_id(obj):
        return obj.parent_id.id if obj.parent_id else None

@router.get(
    "/categories/",
    tags=['module6'],
    summary="Retrieve categories with given input user conditions.",
    response=List[CategorySchemaOut],
)
def get_categories(request,name:str=None,min_level:int=None,max_level:int=None,has_parent:bool=None):
    qs = Category.objects.all()

    if name is not None:
        qs =qs.filter(name__iexact=name)
    if min_level is not None:
        qs = qs.filter(level__gte=min_level)
    if max_level is not None:
        qs = qs.filter(level__lte=max_level)
    if has_parent is not None:
        if has_parent:
            qs = qs.filter(parent_id__isnull = False)
        else:
            qs = qs.filter(parent_id__isnull = True)

    return qs



@router.get(
    "/categories/q/",
    tags=['module6'],
    summary="Retrieve categories with given input user conditions using Q and level between parameter True indicates using OR clause on level",
    response=List[CategorySchemaOut],
)
def get_categories_using_Q(request,
                            active:bool =None,
                            level_between:bool = False,
                            min_level:int = None,
                            max_level:int = None):
    qs = Category.objects.all()

    filters = Q()
    if active is not None:
        filters &= Q(is_active=True)
    
    level_filter =Q()
    
    if min_level is not None:
        level_filter &= Q(level__gte=min_level)
    if max_level is not None:
        level_filter &= Q(level__lte = max_level)

    if level_between:
        filters |= level_filter
    else:
        filters &= level_filter

    print(filters)
    qs = qs.filter(filters)

    return qs

class ProductOutSchema(Schema):
    id :int
    name :str
    slug :str
    is_digital :bool
    is_active : bool
    price : float

@router.get(
    "/products/",
    tags=["module6"],
    summary = "Filter products based on input conditions using q",
    response = List[ProductOutSchema],
)
def get_products(request,
                active:bool =None,
                digital:bool = None,
                min_price:float =None,
                max_price:float = None,
                price_match:bool = True,
                name_or_slug:str = None):
    filter = Q()
    if active is not None:
        filter &= Q(is_active=active)
    if digital is not None:
        filter &= Q(is_digital=digital)

    price_filter =Q()
    if price_match: #in range on min, max price
        if min_price is not None:
            price_filter &= Q(price__gte =min_price)
        if max_price is not None:
            price_filter &= Q(price__lte = max_price)
    else: #outside range of min,max price
        if min_price is not None:
            price_filter |= Q(price__lt = min_price)
        if max_price is not None:
            price_filter |= Q(price__gt = max_price)

    filter &= price_filter
    if name_or_slug is not None:
        filter &= (Q(name=name_or_slug) | Q(slug =name_or_slug))
    
    qs = Product.objects.filter(filter)
    return qs

@router.get(
    "/products/negate/",
    tags=["module6"],
    summary = "Filter products based on input conditions using negate for exclude_keyword",
    response = List[ProductOutSchema],
)
def get_products_negate(request,
                active:bool =None,
                min_price:float =None,
                max_price:float = None,
                price_match:bool = True,
                exclude_keyword :bool = False, 
                name_or_slug:str = None):
    filter = Q()
    if active is not None:
        filter &= Q(is_active=active)
    
    price_filter =Q()
    if price_match: #in range on min, max price
        if min_price is not None:
            price_filter &= Q(price__gte =min_price)
        if max_price is not None:
            price_filter &= Q(price__lte = max_price)
    else: #outside range of min,max price
        if min_price is not None:
            price_filter |= Q(price__lt = min_price)
        if max_price is not None:
            price_filter |= Q(price__gt = max_price)

    filter &= price_filter

    '''
    if exclude_keyword:
        if name_or_slug is not None:
            filter &= (~Q(name__icontains=name_or_slug) & ~Q(slug__icontains =name_or_slug))
    else:
        if name_or_slug is not None:
            filter &= (Q(name__icontains=name_or_slug) | Q(slug__icontains =name_or_slug))
    '''

    keyword_filter = Q()
    if name_or_slug is not None:
        keyword_filter &= Q(name__icontains=name_or_slug) | Q(slug__icontains =name_or_slug)

    filter &= ~keyword_filter if exclude_keyword else keyword_filter

    qs = Product.objects.filter(filter)
    return qs

class ProductOutPatternSearch(Schema):
    id: int
    name: str
    slug: str
    is_digital: bool
    is_active: bool
    price: float

@router.get(
    "/products/name_pattern/",
    tags=["module6"],
    summary="Filter products by name/slug with selectable pattern matching",
    response=List[ProductOutPatternSearch],
)
def get_product_name_pattern(request,
                        search_string:str,
                         search_type:str='all'):
    filter=Q()

    if search_type =='starts':
        filter &= Q(name__istartswith=search_string) | Q(slug__istartswith=search_string)
    elif search_type == 'ends':
        filter &= Q(name__iendswith=search_string) | Q(slug__iendswith=search_string)
    else:
        filter &= Q(name__icontains=search_string) | Q(slug__icontains=search_string)

    qs = Product.objects.filter(filter)
    return qs


class ProductOutByIdList(Schema):
    id: int
    name: str
    slug: str
    is_digital: bool
    is_active: bool
    price: float

@router.get(
    "/products/by-ids/",
    tags=["module6"],
    summary="Get all the products of given ids",
    response = list[ProductOutByIdList],
)
def get_product_by_id_list(request,
                        ids:List[int] = Query(...)
                    ):
    filter =Q()
    if ids:
        filter &= Q(id__in=ids)
    else:
        return []

    qs = Product.objects.filter(filter)
    return qs

class ProductOutByPriceRange(Schema):
    id: int
    name: str
    slug: str
    is_digital: bool
    is_active: bool
    price: float

@router.get(
    "/products/by-price-range/",
    tags=["module6"],
    summary="Get all the products of given price range",
    response = list[ProductOutByPriceRange],
)
def get_products_by_price_range(request,min_price:float,max_price:float,active:Optional[bool]=None):
    filters = Q()
    if active is not None:
        filters &= Q(is_active=active)

    filters &= Q(price__range=(min_price,max_price))

    qs = Product.objects.filter(filters)
    return qs

class ProductOutBySlice(Schema):
    id: int
    name: str
    slug: str
    is_digital: bool
    is_active: bool
    price: float
@router.get(
    "/products/get_by_slice",
    tags=["module6"],
    summary="Get all the products of given slice range",
    response = list[ProductOutBySlice],
)
def get_product_by_slice_range(request,
                                start:int = Query(0,ge=0,description="Start index(inclusive)"),
                                end:int = Query(10,gt=0,description="End index")):

        qs = Product.objects.all().order_by("-created_at")[start:end]
        return qs


class PaginatedResponse(Schema):
    total: int
    page: int
    page_size: int
    items: List[CategorySchemaOut]


@router.get(
    "/categories/paginated",
    tags=["module6"],
    summary="Paginate filtered categories by page number",
    response=PaginatedResponse,
)
def paginate_categories_by_page(
    request,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = Query(None),
):
    filters = Q()
    if is_active is not None:
        filters &= Q(is_active=is_active)

    qs = Category.objects.filter(filters).order_by("name")
    total = qs.count()

    # Calculate offset from page number
    start = (page - 1) * page_size
    end = start + page_size
    items = qs[start:end]

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


class CategoryOut(Schema):
    id: int
    name: str
    slug: str
    is_active: bool
    level: int


@router.get(
    "/categories/active",
    tags=["module6"],
    summary="Return all active categories using custom manager",
    response=List[CategoryOut],
)
def get_active_categories(request):
    return Category.objects.active().order_by("name")
    



