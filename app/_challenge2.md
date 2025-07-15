#Challenge 2

## ch2_1 Get first and last 5 added products.

```python

qs1 = Product.objects.filter(is_active=True).order_by("id")[:5]
qs2 = Product.objects.filter(is_active=True).order_by("-id")[:5]
qs = qs1 | qs2 #performs database level UNION on 2 querysets and removes duplicates
# qs =qs1.union(qs2) #another way to UNION
return qs.order_by("id")

```

## ch2_2 Get all Orders from last 30 days.

```python
from datetime import timedelta
from django.utils import timezone # For timezone-aware datetimes

# Get the current timezone-aware datetime
today_date = timezone.now()
qs = Order.objects.filter(created_at__gte=today_date-timedelta(days=30))
return qs

```

## ch2_3 Find products in multiple categories.

```python

id_list=[2,4,6]
qs = Product.objects.filter(category_id_id__in= ids_list)
return qs

```

## ch2_4 List products priced between 500 to 1000.

```python
qs = Product.objects.filter(price__range=(500,1000))
return qs

```

## ch2_5 Exclude product priced 19.99 and under 100.

```python
qs = Product.objects.exclude(Q(price=19.99)|Q(price__lt=100))
return qs

```


## ch2_6 Find users name janedoe or johndoe.

```python
from django.auth.contrib.models import User

qs = User.objects.filter(Q(username='janedoe')|Q(username='johndoe))
return qs

```
## ch2_7 Find products starting with letter 'W'.

```python
qs = Product.objects.filter(name__istartswith='W')
return qs

```
## ch2_8 Find products ending  with letter 'E'.

```python
qs = Product.objects.filter(name__iendswith='E')
return qs

```

## ch2_9 Find top 10 most expensive active products.

```python
qs = Product.objects.filter(is_active=True).order_by('-price')[:10]
return qs

```

## ch2_10 Find users with email ending with 'example.com'.

```python
from django.auth.contrib.models import User

qs = User.objects.filter(email__endswith='example.com')
return qs

```

## ch2_11 Return 20th most expensive product.

```python
qs = Product.objects.order_by('-price')[19:20]
return qs

```