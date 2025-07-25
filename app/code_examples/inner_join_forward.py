# pretty_sql.py

# docker compose up --build -d
# docker exec -it django_app sh
# python manage.py shell_plus
# docker exec -it django_app sh -c "clear && python manage.py shell_plus"

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


# 🔎 Example 1: Products in the "Electronics" category
def ex1():
    reset_queries()
    qs = Product.objects.filter(category_id__name="Electronics")
    for p in qs:
        print(p.name)
        print(p.category_id.name)
    show_queries()
    pretty_all()


def ex1_values():
    reset_queries()
    qs = Product.objects.filter(category_id__name="Electronics").values(
        "name", "category__name"
    )
    for row in qs:
        print(row)
    show_queries()
    pretty_all()


def ex1_only():
    qs = Product.objects.only("name", "category__name").filter(
        category_id__name="Electronics"
    )
    for p in qs:
        print(p.name, p.category.name)
    pretty_all()


# 🔎 Example 2: Active products in the "Books" category
def ex2():
    reset_queries()
    qs = Product.objects.filter(category_id__name="Books", is_active=True)
    for p in qs:
        print(p.name)
    show_queries()
    pretty_all()


def ex2_values():
    qs = Product.objects.filter(category_id__name="Books", is_active=True).values(
        "name", "price"
    )
    for row in qs:
        print(row)
    pretty_all()


def ex2_only():
    qs = Product.objects.only("name", "price", "category__name").filter(
        category_id__name="Books", is_active=True
    )
    for p in qs:
        print(p.name, p.price)
    pretty_all()


# 🔎 Example 3: Products in any active category
def ex3():
    reset_queries()
    qs = Product.objects.filter(category_id__is_active=True)
    for p in qs:
        print(p.name)
    show_queries()
    pretty_all()


def ex3_values():
    qs = Product.objects.filter(category_id__is_active=True).values_list("id", flat=True)
    for pid in qs:
        print(pid)
    pretty_all()


def ex3_only():
    qs = Product.objects.only("name", "category__is_active").filter(
        category_id__is_active=True
    )
    for p in qs:
        print(p.name)
    pretty_all()


# 🔎 Example 4: Products in categories starting with "Home"
def ex4():
    reset_queries()
    qs = Product.objects.filter(category_id__name__startswith="Home")
    for p in qs:
        print(p.name)
    show_queries()
    pretty_all()


def ex4_values():
    qs = Product.objects.filter(category_id__name__startswith="Home").values(
        "name", "category__slug"
    )
    for row in qs:
        print(row)
    pretty_all()


def ex4_only():
    qs = Product.objects.only("name", "category_id__slug").filter(
        category__name__startswith="Home"
    )
    for p in qs:
        print(p.name, p.category_id.slug)
    pretty_all()


# 🔎 Example 5: Products in a specific category by slug
def ex5():
    reset_queries()
    qs = Product.objects.filter(category_id__slug="clothing-men")
    for p in qs:
        print(p.name)
    show_queries()
    pretty_all()


def ex5_values():
    qs = Product.objects.filter(category_id__slug="clothing-men").values_list(
        "slug", flat=True
    )
    for slug in qs:
        print(slug)
    pretty_all()


def ex5_only():
    qs = Product.objects.only("name", "slug", "category_id__slug").filter(
        category_id__slug="clothing-men"
    )
    for p in qs:
        print(p.name, p.slug)
    pretty_all()


# 🔎 Example 6: Products ordered by category name (with select_related)
def ex6():
    reset_queries()
    qs = Product.objects.select_related("category_id").order_by("category_id__name")
    for p in qs:
        print(p.name, "->", p.category_id.name)
    show_queries()
    pretty_all()


def ex6_values():
    qs = (
        Product.objects.select_related("category_id")
        .order_by("category_id__name")
        .values("name", "category_id__name")
    )
    for row in qs:
        print(row)
    pretty_all()


def ex6_only():
    qs = (
        Product.objects.only("name", "category_id__name")
        .select_related("category_id")
        .order_by("category_id__name")
    )
    for p in qs:
        print(p.name, p.category_id.name)
    show_queries()
    pretty_all()


# 🔎 Example 7: Products where category level = 2
def ex7():
    reset_queries()
    qs = Product.objects.filter(category_id__level=2)
    for p in qs:
        print(p.name)
    show_queries()
    pretty_all()


def ex7_values():
    qs = Product.objects.filter(category_id__level=2).values("name", "category_id__level")
    for row in qs:
        print(row)
    pretty_all()


def ex7_only():
    qs = Product.objects.only("name", "category_id__level").filter(category_id__level=2)
    for p in qs:
        print(p.name, p.category_id.level)
    pretty_all()
