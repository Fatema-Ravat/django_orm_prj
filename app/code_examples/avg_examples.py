# reverse_joins.py

# Usage:
# docker compose up --build -d
# docker exec -it django_app sh -c "clear && python manage.py shell_plus"


import os

from django.db import connection, reset_queries
from django.db.models import Avg, Q
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


# 🧮 ex18 – Global average of category levels
def ex18():
    """Aggregate average level of all categories"""
    reset_queries()
    result = Category.objects.aggregate(avg_level=Avg("level"))
    print(result)
    show_queries()
    pretty_all()


# 🧮 ex19 – Average level grouped by parent category
def ex119():
    """Average level per parent category"""
    reset_queries()
    qs = Category.objects.values("parent__name").annotate(avg_level=Avg("level"))
    for row in qs:
        print(f"{row['parent__name']}: {row['avg_level']}")
    show_queries()
    pretty_all()


# 🧮 ex20 – Average level for active categories only
def ex120():
    """Average level of only active categories"""
    reset_queries()
    result = Category.objects.filter(is_active=True).aggregate(
        avg_active_level=Avg("level")
    )
    print(result)
    show_queries()
    pretty_all()


# 🧮 ex21 – Average level by parent (active only)
def ex121():
    """Grouped average for active categories only"""
    reset_queries()
    qs = Category.objects.values("parent__name").annotate(
        avg_level=Avg("level", filter=Q(is_active=True))
    )
    for row in qs:
        print(f"{row['parent__name']}: {row['avg_level']} (active only)")
    show_queries()
    pretty_all()


# 🧮 ex22 – Aliased average field in annotate
def ex122():
    """Use alias for annotated average"""
    reset_queries()
    qs = Category.objects.annotate(mean_level=Avg("level"))
    for c in qs:
        print(f"{c.name}: {c.mean_level}")
    show_queries()
    pretty_all()


# 🧮 ex23 – Handle categories with no level values (optional)
def ex123():
    """Demonstrate null handling in averages"""
    reset_queries()
    qs = Category.objects.aggregate(avg_level=Avg("level"))
    print("Average level (includes nulls as ignored):", qs)
    show_queries()
    pretty_all()
