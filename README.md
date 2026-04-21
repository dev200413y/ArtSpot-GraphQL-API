# ArtSpot — Shop GraphQL API

A GraphQL API built with **Python**, **Django**, and **Graphene-Django** for performing CRUD operations on `Shop` entities.

---

## Tech Stack

| Layer      | Technology                    |
|------------|-------------------------------|
| Language   | Python 3.10+                  |
| Framework  | Django 4.2                    |
| GraphQL    | Graphene-Django 3.x           |
| Database   | SQLite (dev) / PostgreSQL (prod) |

---

## Shop Model

| Field       | Type              | Description                          |
|-------------|-------------------|--------------------------------------|
| `id`        | Integer (auto PK) | Auto-generated primary key           |
| `name`      | String            | Name of the shop                     |
| `email`     | Array (JSON)      | One or more email addresses          |
| `phone`     | Array (JSON)      | One or more phone numbers            |
| `address`   | Text              | Physical address                     |
| `created_at`| DateTime          | Timestamp of creation (auto)         |
| `updated_at`| DateTime          | Timestamp of last update (auto)      |

---

## Setup & Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd artspot_graphql

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Run the development server
python manage.py runserver
```

GraphiQL IDE will be available at: **http://127.0.0.1:8000/graphql/**

---

## GraphQL API Reference

### Query — List All Shops

```graphql
query {
  allShops {
    id
    name
    email
    phone
    address
    createdAt
    updatedAt
  }
}
```

### Query — Single Shop by ID

```graphql
query {
  shop(id: 1) {
    id
    name
    email
    phone
    address
  }
}
```

### Mutation — Create Shop

```graphql
mutation {
  createShop(
    name: "The Art Corner"
    email: ["hello@artcorner.com", "support@artcorner.com"]
    phone: ["9876543210", "9000011122"]
    address: "12 Gallery Road, Connaught Place, New Delhi"
  ) {
    shop {
      id
      name
      email
      phone
      address
    }
  }
}
```

### Mutation — Update Shop

All fields except `id` are optional. Only provided fields are updated.

```graphql
mutation {
  updateShop(
    id: 1
    name: "The Art Corner — Revised"
    email: ["newemail@artcorner.com"]
  ) {
    shop {
      id
      name
      email
    }
  }
}
```

### Mutation — Delete Shop

```graphql
mutation {
  deleteShop(id: 1) {
    success
    message
  }
}
```

---

## Running Tests

```bash
python manage.py test shops --verbosity=2
```

**9 test cases** covering:
- Create shop
- Query all shops
- Query single shop by ID
- Query nonexistent shop (returns null)
- Update shop (full fields)
- Update shop (partial fields — unchanged fields preserved)
- Update nonexistent shop (raises error)
- Delete shop
- Delete nonexistent shop (graceful failure)

---

## Project Structure

```
artspot_graphql/
├── artspot_graphql/
│   ├── settings.py          # Django settings (Graphene schema configured here)
│   ├── urls.py              # URL routing — exposes /graphql/ endpoint
│   └── wsgi.py
├── shops/
│   ├── models.py            # Shop model definition
│   ├── schema.py            # GraphQL types, queries, and mutations
│   ├── admin.py             # Django admin registration
│   ├── tests.py             # 9 CRUD test cases
│   └── migrations/
│       └── 0001_initial.py
├── manage.py
├── requirements.txt
└── README.md
```

---

## Notes on Array Fields

- In **development** (SQLite), `email` and `phone` are stored as `JSONField` (native JSON arrays).
- In **production** (PostgreSQL), these can be changed to `django.contrib.postgres.fields.ArrayField` for stricter type enforcement. The `settings.py` file includes the PostgreSQL configuration as a commented block.

---

## Author

Dev Varshney — ArtSpot Python Internship Assignment
