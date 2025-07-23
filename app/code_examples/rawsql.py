# reverse_joins.py

# Usage:
# docker compose up --build -d
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


def ex26():
    """Get products in active categories using raw()"""
    reset_queries()
    qs = Product.objects.raw("""
        SELECT id, name
        FROM inventory_product
        INNER JOIN inventory_category ON inventory_product.category_id = inventory_category.id
        WHERE inventory_category.is_active = TRUE
    """)
    for p in qs:
        print(p.name)
    show_queries()
    pretty_all()


def ex27():
    """Raw join with non-model fields using cursor"""
    reset_queries()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT p.name AS product_name, c.name AS category_name
            FROM inventory_product p
            INNER JOIN inventory_category c ON p.category_id = c.id
            WHERE c.level = %s
        """,
            [1],
        )
        rows = cursor.fetchall()
        for name, category in rows:
            print(f"{name} — {category}")
    show_queries()
    pretty_all()


def ex28():
    """Raw query using parameter substitution"""
    reset_queries()
    category_slug = "electronics"
    qs = Product.objects.raw(
        """
        SELECT p.*
        FROM inventory_product p
        INNER JOIN inventory_category c ON p.category_id = c.id
        WHERE c.slug = %s
    """,
        [category_slug],
    )
    for p in qs:
        print(p.name)
    show_queries()
    pretty_all()
