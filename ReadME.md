# 🏪 Inventory Management System – FastAPI & MongoDB

This project is a **RESTful Inventory Management API** built using **FastAPI** and **MongoDB**.  
It supports **CRUD operations using filters** instead of MongoDB `_id`, allowing real-world search, update and delete by product attributes.

---

## 🚀 Tech Stack
- FastAPI
- MongoDB
- Pydantic
- PyMongo

---

## 📦 Product Schema

```json
{
  "brand": "Amul",
  "name": "Milk",
  "quantity": {
    "value": 1,
    "unit": "L"
  },
  "price": 60
}
```

---

## ▶️ Start Server

```bash
uvicorn main:app --reload
```

Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## 🔹 CREATE Product

**POST** `/products`

```json
{
  "brand": "Amul",
  "name": "Milk",
  "quantity": {
    "value": 1,
    "unit": "L"
  },
  "price": 60
}
```

---

## 🔹 BULK INSERT

**POST** `/products/bulk`

```json
[
  {
    "brand": "Amul",
    "name": "Butter",
    "quantity": { "value": 500, "unit": "gm" },
    "price": 250
  },
  {
    "brand": "Nestle",
    "name": "Milk",
    "quantity": { "value": 1, "unit": "L" },
    "price": 65
  }
]
```

---

## 🔍 SEARCH Products

| Request | Description |
|-------|-------------|
| `/products/search?brand=amul` | All Amul products |
| `/products/search?name=milk` | All milk items |
| `/products/search?qty_value=1&qty_unit=L` | All 1L products |
| `/products/search?price=60` | All products priced ₹60 |

---

## ✏ UPDATE Products by Filter

### Update price of all 1L Amul Milk

**PUT**  
`/products/update-by-filter?brand=amul&name=milk&qty_value=1&qty_unit=L`

```json
{
  "price": 70
}
```

---

### Convert 500gm Butter packs to 1kg

**PUT**  
`/products/update-by-filter?name=butter&qty_value=500&qty_unit=gm`

```json
{
  "quantity": {
    "value": 1,
    "unit": "kg"
  }
}
```

---

## ❌ DELETE Products by Filter

### Delete all expired zero-stock products

**DELETE**  
`/products/delete-by-filter?qty_value=0&qty_unit=L`

---

### Delete all discontinued brand products

**DELETE**  
`/products/delete-by-filter?brand=oldbrand`

---

## 🧠 Features

- No dependency on MongoDB `_id`
- Case-insensitive search
- Quantity stored with **value + unit**
- Bulk insert with duplicate skip
- Filter-based update & delete
- Postman & Swagger friendly APIs

---

## 📮 Author

Aryan More – Inventory Management System using FastAPI & MongoDB
