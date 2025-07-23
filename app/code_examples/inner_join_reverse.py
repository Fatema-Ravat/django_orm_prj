# reverse_joins.py

# Usage:
# docker compose up --build -d
# docker exec -it django_app sh -c "clear && python manage.py shell_plus"


import os

from django.db import connection, reset_queries
from inventory.models import Category


def cls():
    os.system("clear")


def pretty_all():
    from sqlparse import format

    for q in connection.queries:
        print("→")
        print(format(q["sql"], reindent=True, keyword_case="upper"))


def show_queries():
    print("Queries run:", len(connection.queries))


# 🔁 Reverse Access: Using default product_set
def ex1():
    """Category → Products using default reverse accessor: product_set"""
    reset_queries()
    category = Category.objects.get(name="Books")
    for p in category.product_set.all():
        print(p.name)
    show_queries()
    pretty_all()


# 🔁 Reverse Access: Using custom related_name="products"
def ex2():
    """Category → Products using custom related_name: products"""
    reset_queries()
    category = Category.objects.get(name="Books")
    for p in category.products.all():
        print(p.name)
    show_queries()
    pretty_all()


# 🔎 Reverse Filter: Categories with active products (reverse filter)
def ex8():
    """Find categories that have at least one active product"""
    reset_queries()
    # qs = Category.objects.filter(products__is_active=True).distinct()
    qs = Category.objects.filter(products__isnull=True)
    for c in qs:
        print(c.name)
    show_queries()
    pretty_all()


# 🔎 Reverse Filter: Categories where any product is digital
def ex9():
    """Find categories with at least one digital product"""
    reset_queries()
    qs = Category.objects.filter(products__is_digital=True).distinct()
    for c in qs:
        print(c.name)
    show_queries()
    pretty_all()


# 🔃 Reverse Count: Categories annotated with number of products
from django.db.models import Count


def ex10():
    """Annotate each category with product count"""
    reset_queries()
    qs = Category.objects.annotate(num_products=Count("products")).filter(
        num_products__gt=0
    )
    for c in qs:
        print(f"{c.name}: {c.num_products} products")
    show_queries()
    pretty_all()


# 🧪 Reverse with filtering + ordering
def ex11():
    """Categories with active products, ordered by category name"""
    reset_queries()
    qs = Category.objects.filter(products__is_active=True).distinct().order_by("name")
    for c in qs:
        print(c.name)
    show_queries()
    pretty_all()
