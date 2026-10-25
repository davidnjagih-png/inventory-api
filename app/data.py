"""
Simulated data storage.

The inventory lives in a plain Python list (the "database array").
Each item has a unique integer ``id`` and its fields are modelled on what
the OpenFoodFacts API returns (product_name, brands, ingredients_text, ...)
plus store-specific fields (price, stock).
"""

import copy

SEED_INVENTORY = [
    {
        "id": 1,
        "barcode": "0025293600232",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
        "categories": "Plant-based milks",
        "quantity": "1.89 L",
        "nutriscore_grade": "c",
        "image_url": None,
        "price": 4.99,
        "stock": 25,
    },
    {
        "id": 2,
        "barcode": "3017620422003",
        "product_name": "Nutella",
        "brands": "Ferrero",
        "ingredients_text": "Sugar, palm oil, hazelnuts 13%, skimmed milk powder, cocoa",
        "categories": "Spreads, Sweet spreads",
        "quantity": "400 g",
        "nutriscore_grade": "e",
        "image_url": None,
        "price": 5.49,
        "stock": 40,
    },
    {
        "id": 3,
        "barcode": "5449000000996",
        "product_name": "Coca-Cola Original Taste",
        "brands": "Coca-Cola",
        "ingredients_text": "Carbonated water, sugar, colour (caramel E150d), acid (phosphoric acid)",
        "categories": "Beverages, Sodas",
        "quantity": "330 ml",
        "nutriscore_grade": "e",
        "image_url": None,
        "price": 1.25,
        "stock": 120,
    },
]

# The live "database" the API reads from and writes to.
inventory = copy.deepcopy(SEED_INVENTORY)


def reset_inventory():
    """Restore the inventory to its seed state (used by tests)."""
    inventory.clear()
    inventory.extend(copy.deepcopy(SEED_INVENTORY))


def next_id():
    """Return the next available id."""
    return max((item["id"] for item in inventory), default=0) + 1


def find_item(item_id):
    """Return the item with the given id, or None."""
    return next((item for item in inventory if item["id"] == item_id), None)
