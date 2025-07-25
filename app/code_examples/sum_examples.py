# reverse_joins.py

# Usage:
# docker compose up --build -d
# docker exec -it django_app sh -c "clear && python manage.py shell_plus"


import os

from django.db import connection, reset_queries
from django.db.models import Q, Sum
from inventory.models import Category, Product


def cls():
    os.system("clear")


def pretty_all():
    from sqlparse import format

    for q in connection.queries:
        print("→")
        print(format(q["sql"], reindent=True, keyword_case="upper"))


def show_queries():
    print("Queries run:", len(connection.queries))


# 🧮 ex13 – Total price of all products
def ex113():
    """Aggregate total of all product prices"""
    reset_queries()
    print(Product.objects.aggregate(total_price=Sum("price")))
    show_queries()
    pretty_all()


# 🧮 ex14 – Sum of product prices per category
def ex114():
    """Annotate categories with total product value"""
    reset_queries()
    qs = Category.objects.annotate(total_value=Sum("products__price"))
    for c in qs:
        print(f"{c.name}: {c.total_value} total value")
    show_queries()
    pretty_all()


# 🧮 ex15 – Filter categories by total product value
def ex115():
    """Categories with total product value > 500"""
    reset_queries()
    qs = Category.objects.annotate(total_value=Sum("products__price")).filter(
        total_value__gt=500
    )
    for c in qs:
        print(f"{c.name}: {c.total_value}")
    show_queries()
    pretty_all()


# 🧮 ex16 – Sum only active product prices per category
def ex116():
    """Sum active product prices using conditional filter"""
    reset_queries()
    qs = Category.objects.annotate(
        active_value=Sum("products__price", filter=Q(products__is_active=True))
    )
    for c in qs:
        print(f"{c.name}: {c.active_value} (active only)")
    show_queries()
    pretty_all()


# 🧮 ex17 – Sum distinct category levels
def ex117():
    """Sum distinct levels — mostly illustrative"""
    reset_queries()
    result = Category.objects.aggregate(distinct_levels=Sum("level", distinct=True))
    print(result)
    show_queries()
    pretty_all()
