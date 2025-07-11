# Django Shell Tutorial: Using `.values()` with the Category Model

This tutorial shows how to interact with the `Category` model using Django's `.values()` method inside the Django shell. You'll learn how to retrieve selected fields, return dictionaries instead of model instances, and chain `values()` with other query methods.

## 🐚 Step 1: Access the Django Shell

Use the following commands to bring up your Django app and enter the shell environment.

```bash
docker compose up --build -d
docker exec -it django_app sh
python3 manage.py shell
```

## 📥 Step 2: Insert Sample Category Records

Before running `.values()` queries, create some test data.

### ✅ Create a Category Using `.save()` (Step-by-Step)

```python
from inventory.models import Category
from django.utils.text import slugify

category = Category(
    name="Electronics",
    slug=slugify("Electronics"),
    is_active=True,
    level=0
)
category.save()
```

### ✅ Create a Category Using `.create()` (One-Liner)

```python
from inventory.models import Category
from django.utils.text import slugify

Category.objects.create(
    name="Computers",
    slug=slugify("Computers"),
    is_active=True,
    level=1
)
```

## 🔍 Step 3: Query with `.values()`

### ✅ Example 1: Return Selected Fields as Dictionaries

```python
from inventory.models import Category

# Return only 'name' and 'slug'
categories = Category.objects.values("name", "slug")
for cat in categories:
    print(cat)
```

### ✅ Example 2: Access Dictionary Values

```python
rows = Category.objects.values("id", "name")
for row in rows:
    print(row["id"], row["name"])
```

### ✅ Example 3: Chain with `filter()`

```python
# Only active categories, return 'name' and 'is_active'
active_cats = Category.objects.filter(is_active=True).values("name", "is_active")
for cat in active_cats:
    print(cat)
```

### ✅ Example 4: Use with `order_by()`

```python
# Sorted by level
sorted_cats = Category.objects.order_by("level").values("name", "level")
for cat in sorted_cats:
    print(cat)
```

### ✅ Example 5: Convert to List

```python
# Materialize the queryset into a list
category_list = list(Category.objects.values("name"))
print(category_list)
```

### ✅ Example 6: Use `.values()` with `count()`

```python
# Count how many rows have been returned
total = Category.objects.values("name").count()
print(f"Total records with name field: {total}")
```
