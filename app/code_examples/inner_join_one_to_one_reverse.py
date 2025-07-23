# one_to_one_joins.py

# Usage:
# docker compose up --build -d
# docker exec -it django_app sh -c "clear && python manage.py shell_plus"
# from inventory.one_to_one_joins import ex1, ex2, ex3, etc.


import os

from django.db import connection, reset_queries
from inventory.models import Product


def cls():
    os.system("clear")


def pretty_all():
    from sqlparse import format

    for q in connection.queries:
        print("→")
        print(format(q["sql"], reindent=True, keyword_case="upper"))


def show_queries():
    print("Queries run:", len(connection.queries))


# 🔁 Reverse: Product → Stock
def ex15():
    """Access StockManagement from Product using .stock (reverse)"""
    reset_queries()
    product = Product.objects.select_related("stock").filter(is_active=True).first()
    print(product.name, "→", product.stock.quantity)
    show_queries()
    pretty_all()


# 🔍 Filter Products by Stock Quantity
def ex16():
    """Filter Products by conditions in their StockManagement record"""
    reset_queries()
    qs = Product.objects.select_related("stock").filter(stock__quantity__gte=100)
    for p in qs:
        print(p.name, "-", p.stock.quantity)
    show_queries()
    pretty_all()


# 🔄 Order Products by Stock Quantity
def ex17():
    """Order Products by stock quantity using reverse one-to-one"""
    reset_queries()
    qs = Product.objects.select_related("stock").order_by("stock__quantity")
    for p in qs:
        print(p.name, "→", p.stock.quantity)
    show_queries()
    pretty_all()


# 🧠 Prefetch-safe: Check for products with stock records
def ex18():
    """Find products that have stock (exclude missing one-to-one)"""
    reset_queries()
    qs = Product.objects.filter(stock__isnull=False)
    for p in qs:
        print(p.name)
    show_queries()
    pretty_all()
