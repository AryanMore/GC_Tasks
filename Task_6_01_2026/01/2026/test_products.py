from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ---------- CREATE ----------
def test_create_product():
    response = client.post(
        "/products",
        json={
            "brand": "TestBrand",
            "name": "TestMilk",
            "quantity": {
                "value": 1,
                "unit": "L"
            },
            "price": 50
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["brand"] == "TestBrand"
    assert data["name"] == "TestMilk"
    assert data["quantity"]["unit"] == "L"


# ---------- SEARCH ----------
def test_search_product():
    response = client.get("/products/search?brand=TestBrand")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


# ---------- UPDATE ----------
def test_update_product():
    response = client.put(
        "/products/update-by-filter?brand=TestBrand",
        json={
            "price": 60
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["matched"] >= 1
    assert data["updated"] >= 1


# ---------- VERIFY UPDATE ----------
def test_verify_update():
    response = client.get("/products/search?brand=TestBrand")

    assert response.status_code == 200
    assert response.json()[0]["price"] == 60


# ---------- DELETE ----------
def test_delete_product():
    response = client.delete(
        "/products/delete-by-filter?brand=TestBrand"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["deleted"] >= 1


# ---------- VERIFY DELETE ----------
def test_verify_delete():
    response = client.get("/products/search?brand=TestBrand")

    assert response.status_code == 200
    assert len(response.json()) == 0
