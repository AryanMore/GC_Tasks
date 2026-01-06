from fastapi import FastAPI, HTTPException
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from connection import collection
from models import Product, UpdateProduct
from typing import List
from pymongo.errors import BulkWriteError

app = FastAPI(title="Product CRUD API")

def product_helper(p):
    return {
        "id": str(p["_id"]),
        "brand": p["brand"],
        "name": p["name"],
        "quantity": p["quantity"],
        "price": p["price"]
    }


# ---------------- CREATE ----------------
@app.post("/products")
def add_product(product: Product):
    try:
        result = collection.insert_one(product.dict())
        new_product = collection.find_one({"_id": result.inserted_id})
        return product_helper(new_product)
    except DuplicateKeyError:
        raise HTTPException(400, "Product already exists")
    
# ---------------- BULK CREATE ----------------

@app.post("/products/bulk")
def add_products_bulk(products: list[Product]):
    try:
        collection.insert_many(
            [p.dict() for p in products],
            ordered=False
        )
        return {"message": f"{len(products)} products processed"}
    except BulkWriteError as e:
        return {
            "inserted": e.details["nInserted"],
            "duplicates_skipped": len(e.details["writeErrors"])
        }

# ---------------- READ ALL ----------------
@app.get("/products")
def get_products():
    return [product_helper(p) for p in collection.find()]


# ---------------- SEARCH ----------------

@app.get("/products/search")
def search_products(
    brand: str | None = None,
    name: str | None = None,
    price: float | None = None,
    qty_value: float | None = None,
    qty_unit: str | None = None
):
    query = {}

    if brand:
        query["brand"] = {"$regex": brand, "$options": "i"}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    if price is not None:
        query["price"] = price

    if qty_value is not None:
        query["quantity.value"] = qty_value

    if qty_unit:
        query["quantity.unit"] = {"$regex": f"^{qty_unit}$", "$options": "i"}

    products = collection.find(query)
    return [product_helper(p) for p in products]


# ---------------- READ ONE ----------------
@app.get("/products/{product_id}")
def get_product(product_id: str):
    product = collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(404, "Product not found")
    return product_helper(product)

# ---------------- UPDATE ----------------
@app.put("/products/update-by-filter")
def update_products_by_filter(
    brand: str | None = None,
    name: str | None = None,
    price: float | None = None,
    qty_value: float | None = None,
    qty_unit: str | None = None,
    update_data: UpdateProduct = ...
):
    query = {}

    if brand:
        query["brand"] = {"$regex": brand, "$options": "i"}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    if price is not None:
        query["price"] = price

    if qty_value is not None:
        query["quantity.value"] = qty_value

    if qty_unit:
        query["quantity.unit"] = {"$regex": f"^{qty_unit}$", "$options": "i"}

    if not query:
        raise HTTPException(400, "At least one filter is required")

    update_dict = {}

    if update_data.brand:
        update_dict["brand"] = update_data.brand
    if update_data.name:
        update_dict["name"] = update_data.name
    if update_data.price is not None:
        update_dict["price"] = update_data.price

    if update_data.quantity:
        if update_data.quantity.value is not None:
            update_dict["quantity.value"] = update_data.quantity.value
        if update_data.quantity.unit:
            update_dict["quantity.unit"] = update_data.quantity.unit

    if not update_dict:
        raise HTTPException(400, "No update fields provided")

    result = collection.update_many(query, {"$set": update_dict})

    return {
        "matched": result.matched_count,
        "updated": result.modified_count
    }


# ---------------- DELETE ----------------
@app.delete("/products/delete-by-filter")
def delete_products_by_filter(
    brand: str | None = None,
    name: str | None = None,
    price: float | None = None,
    qty_value: float | None = None,
    qty_unit: str | None = None
):
    query = {}

    if brand:
        query["brand"] = {"$regex": brand, "$options": "i"}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    if price is not None:
        query["price"] = price

    if qty_value is not None:
        query["quantity.value"] = qty_value

    if qty_unit:
        query["quantity.unit"] = {"$regex": f"^{qty_unit}$", "$options": "i"}

    if not query:
        raise HTTPException(400, "At least one filter is required")

    result = collection.delete_many(query)
    return {"deleted": result.deleted_count}

