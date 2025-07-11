#Challenges

## ch1_1 Retrieve all active products

```python

Product.objects.filter(is_active=True)

```

## ch1_2 Select product name and price only

```python
Product.objects.only('name','price')
```

## ch1_3 Get first product created

```python
Product.objects.order_by('created_at').first()
```

## ch1_4 Get most recently added product

```python
Product.objects.order_by(-'created_at').first()
```

## ch1_5 Retrieve all exclude active products

```python
Product.objects.exclude(is_active=True)
```

## ch1_6 Filter products by price and category

```python
Product.objects.filter(price=200,category_id=1)
```
