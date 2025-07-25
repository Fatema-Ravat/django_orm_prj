# reverse_joins.py

# Usage:
# docker compose up --build -d
# docker exec -it django_app sh -c "clear && python manage.py shell_plus"


import os

from django.db import connection, reset_queries
from django.db.models import Count, Q
from inventory.models import Category, Order, Product


def cls():
    os.system("clear")


def pretty_all():
    from sqlparse import format

    for q in connection.queries:
        print("→")
        print(format(q["sql"], reindent=True, keyword_case="upper"))


def show_queries():
    print("Queries run:", len(connection.queries))


# 🔢 ex1 – Simple count of categories
def ex101():
    """Count total number of Category records"""
    reset_queries()
    print("Total categories:", Category.objects.all().count())
    show_queries()
    pretty_all()


# 🔢 ex2 – Annotate categories with product counts
def ex102():
    """Each category with number of related products"""
    reset_queries()
    qs = Category.objects.annotate(num_products=Count("products"))
    for c in qs:
        print(f"{c.name}: {c.num_products} products")
    show_queries()
    pretty_all()


# 🔢 ex3 – Filter categories by product count
def ex103():
    """Categories with more than 2 products"""
    reset_queries()
    qs = Category.objects.annotate(num_products=Count("products")).filter(
        num_products__gt=2
    )
    for c in qs:
        print(f"{c.name}: {c.num_products} products")
    show_queries()
    pretty_all()


# 🔢 ex4 – Count distinct category levels
def ex104():
    """Count how many distinct levels exist across categories"""
    reset_queries()
    result = Category.objects.aggregate(level_count=Count("level", distinct=True))
    print(result)
    show_queries()
    pretty_all()


# 🔢 ex5 – Count products in each category that are active
def ex105():
    """Count only active products per category"""
    reset_queries()
    qs = Category.objects.annotate(
        active_product_count=Count("products", filter=Q(products__is_active=True))
    )
    for c in qs:
        print(f"{c.name}: {c.active_product_count} active products")
    show_queries()
    pretty_all()


# 🔢 ex6 – Count number of orders per user
def ex106():
    """Show how many orders each user has placed"""
    reset_queries()
    from inventory.models import User

    qs = User.objects.annotate(order_count=Count("order"))
    for u in qs:
        print(f"{u.username}: {u.order_count} orders")
    show_queries()
    pretty_all()


# 🔢 ex7 – Products ordered more than 5 times
def ex107():
    """Products that appear in >5 order lines"""
    reset_queries()
    qs = Product.objects.annotate(order_count=Count("orderproduct")).filter(
        order_count__gt=5
    )
    for p in qs:
        print(f"{p.name}: {p.order_count} orders")
    show_queries()
    pretty_all()


# 🔢 ex8 – How many products per promotion event
def ex108():
    """Count how many products are in each promotion"""
    from inventory.models import PromotionEvent

    reset_queries()
    qs = PromotionEvent.objects.annotate(num_products=Count("productpromotionevent"))
    for event in qs:
        print(f"{event.name}: {event.num_products} products")
    show_queries()
    pretty_all()


# 🔢 ex9 – Orders with multiple product lines
def ex109():
    """Find orders that contain more than 2 different products"""
    reset_queries()
    qs = Order.objects.annotate(product_count=Count("orderproduct")).filter(
        product_count__gt=2
    )
    for o in qs:
        print(f"Order {o.id}: {o.product_count} line items")
    show_queries()
    pretty_all()


# ex10 – Top 5 Most Ordered Products
def ex110():
    """Find top 5 most frequently ordered products"""
    reset_queries()
    qs = Product.objects.annotate(times_ordered=Count("orderproduct")).order_by(
        "-times_ordered"
    )[:5]
    for p in qs:
        print(f"{p.name}: {p.times_ordered} times ordered")
    show_queries()
    pretty_all()


# ex11 – Users with no orders
def ex111():
    """List users who have not placed any orders"""
    from inventory.models import User

    reset_queries()
    qs = User.objects.annotate(order_count=Count("order")).filter(order_count=0)
    for u in qs:
        print(f"{u.username} — No orders")
    show_queries()
    pretty_all()


# ex12 – Count digital vs physical products
def ex112():
    """Count digital vs non-digital products"""
    reset_queries()
    digital = Product.objects.filter(is_digital=True).count()
    physical = Product.objects.filter(is_digital=False).count()
    print(f"Digital: {digital}, Physical: {physical}")
    show_queries()
    pretty_all()
