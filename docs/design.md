# Design Notes

## Task 1 – Problem

Store employees need an admin portal to add, view, edit and delete inventory items, and to pull product details (name, brand, ingredients, etc.) from OpenFoodFacts so they don't have to type them by hand.

Pieces:

| Piece | File | Role |
|---|---|---|
| Data storage | `app/data.py` | Python list of dicts, each with a unique `id` |
| REST API | `app/routes.py` | Flask endpoints; the only code that changes the list |
| External API | `app/external_api.py` | Calls OpenFoodFacts by barcode or name |
| User interface | `cli.py` | Command line + interactive menu; talks to the API over HTTP |
| Tests | `tests/` | pytest + `unittest.mock` |

```
 CLI (cli.py) ──HTTP──▶ Flask API (routes.py) ──▶ inventory list (data.py)
                                │
                                └──▶ external_api.py ──HTTP──▶ OpenFoodFacts
```

## Task 2 – Route design

| Route | Input | Output | Effect on data | Triggered by CLI |
|---|---|---|---|---|
| `GET /inventory` | optional `?q=` | 200, list of items | none | `list` / menu 1 |
| `GET /inventory/<id>` | id in URL | 200 item, 404 | none | `view` / menu 2 |
| `POST /inventory` | JSON, `product_name` required | 201 new item, 400 | appends item with next id | `add` / menu 3 |
| `PATCH /inventory/<id>` | JSON with any editable field | 200 item, 400, 404 | updates fields in place | `update` / menu 4 |
| `DELETE /inventory/<id>` | id in URL | 200 deleted item, 404 | removes item | `delete` / menu 5 |
| `GET /external/barcode/<code>` | barcode | 200 product, 404, 502 | none | `find --barcode` / menu 6 |
| `GET /external/search?name=` | name | 200 list, 400, 502 | none | `find --name` / menu 6 |
| `POST /inventory/import` | `{barcode, price?, stock?}` | 201 item, 400, 404, 409, 502 | appends product fetched from OpenFoodFacts | `import` / menu 7 |
| `POST /inventory/<id>/enrich` | id in URL | 200 item + filled fields, 400, 404, 502 | fills blank product fields from OpenFoodFacts | `enrich` / menu 8 |
| `GET /health` | – | 200 status + item count | none | – |

## Data model

Modelled on the OpenFoodFacts `product` object, plus store fields:

```json
{
  "id": 1,
  "barcode": "0025293600232",
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
  "categories": "Plant-based milks",
  "quantity": "1.89 L",
  "nutriscore_grade": "c",
  "image_url": null,
  "price": 4.99,
  "stock": 25
}
```

Rules: `id` is assigned by the server and cannot be set by clients; `price` is a non-negative number; `stock` is a non-negative whole number; unknown fields are rejected.

## Error handling

- Invalid input → 400 with `{"error": "..."}`
- Missing item → 404
- Duplicate barcode on import → 409
- OpenFoodFacts down, timed out, or bad JSON → 502 (the API keeps running)
- CLI shows `Error: <message>` and exits with code 1; menu mode re-prompts on bad input
