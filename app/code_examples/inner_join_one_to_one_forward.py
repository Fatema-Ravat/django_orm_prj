# one_to_one_joins.py

# Usage:
# docker compose up --build -d
# docker exec -it django_app sh -c "clear && python manage.py shell_plus"
# from inventory.one_to_one_joins import ex1, ex2, ex3, etc.


import os

from django.db import connection, reset_queries
from inventory.models import StockManagement


def cls():
    os.system("clear")


def pretty_all():
    from sqlparse import format

    for q in connection.queries:
        print("→")
        print(format(q["sql"], reindent=True, keyword_case="upper"))


def show_queries():
    print("Queries run:", len(connection.queries))


# 🔁 Forward: Stock → Product
def ex12():
    """Access Product from StockManagement using .product (forward)"""
    reset_queries()
    qs = StockManagement.objects.select_related("product")
    for s in qs:
        print(f"{s.quantity} – {s.product.name}")
    show_queries()
    pretty_all()


# 🔍 Filter Stock by Product Attributes
def ex13():
    """Filter StockManagement records by product fields"""
    reset_queries()
    qs = StockManagement.objects.filter(
        product__is_digital=False, product__price__gt=100
    )
    for s in qs:
        print(s.product.name, "-", s.quantity)
    show_queries()
    pretty_all()


# 🔍 Filter Stock by Product Attributes
def ex14():
    """Filter StockManagement records by product fields"""
    reset_queries()
    qs = StockManagement.objects.select_related("product").filter(
        product__is_digital=False, product__price__gt=100
    )
    for s in qs:
        print(s.product.name, "-", s.quantity)
    show_queries()
    pretty_all()
