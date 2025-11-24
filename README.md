# FastAPI Clean Architecture Demo

A **production-style FastAPI backend** that demonstrates:

- Clean, layered architecture (API → Service → Repository → Database)
- Domain‑driven models and Pydantic schemas
- Alembic migrations for database versioning
- PostgreSQL integration
- A mini **AI content pipeline** for products (generate + store + fetch)

This repo is intentionally small but **architecturally realistic** – the same patterns scale to much larger systems.

---

## ✨ Key Features

- **FastAPI** with type‑safe endpoints and automatic OpenAPI/Swagger docs
- **Service Layer pattern** to keep business logic out of the API layer
- **Repository pattern** to encapsulate all data access
- **SQLAlchemy ORM** models with clear relationships
- **Alembic** migrations for schema evolution
- **PostgreSQL** as the primary database
- **Product module** with full CRUD
- **AIContent module** that stores AI‑generated content per product & channel
- Extensible design for future AI providers (OpenAI, etc.)

---

## 🧱 Architecture Overview

The project follows a simple but powerful layered architecture:

```text
[ HTTP / FastAPI Router ]
          ↓
[ Service Layer (business rules) ]
          ↓
[ Repository Layer (SQLAlchemy) ]
          ↓
[ PostgreSQL (via Alembic migrations) ]
```

### 1. API Layer (Routers)

- Defines HTTP routes and request/response models.
- Delegates all logic to the **Service Layer**.
- Returns clean Pydantic DTOs to the client.

Example: `app/api/v1/products.py`

- `GET  /api/v1/products/` – list products
- `POST /api/v1/products/` – create product
- `GET  /api/v1/products/{id}` – get product by ID
- `POST /api/v1/products/{id}/generate/ebay` – generate AI content for eBay (demo)
- `GET  /api/v1/products/{id}/ai-contents` – list all AI contents for a product

### 2. Service Layer

- Contains the **business logic**.
- Coordinates work across repositories and external services (e.g., AI providers).
- Isolated from HTTP and database details.

Example responsibilities:

- Validate that a product exists before generating AI content
- Call the AI generation function, then persist the result as `AIContent`
- Implement pagination and error handling

### 3. Repository Layer

- Encapsulates all data access for each aggregate.
- Uses SQLAlchemy sessions, but callers only see simple Python functions.

Example:

- `product_repository.get_product(db, product_id)`
- `product_repository.get_products(db, skip, limit)`
- `ai_content_repository.get_ai_contents_by_product(db, product_id, channel, content_type)`

This keeps the rest of the codebase **decoupled from ORM details**.

### 4. Database & Migrations

- **PostgreSQL** is used as the primary database.
- **Alembic** tracks schema versions and upgrades.

Example migrations:

- `create products table` – base product catalog
- `add ai_contents table` – AI content storage linked to products

Each migration is a small, explicit step forward in the schema.

---

## 🧩 Domain Model

### Product

Represents an item in the catalog. Minimal but realistic fields (id, name, sku, price, flags, timestamps, etc.).

### AIContent

Represents **AI‑generated content** attached to a Product.

Key ideas:

- `product_id` – foreign key to Product
- `channel` – e.g., `ebay`, `shopify`, `instagram`
- `content_type` – e.g., `full_listing`, `title`, `caption`
- `payload` – JSONB to store flexible AI output (title, body, SEO keywords, etc.)
- `approved` – whether a human has reviewed/approved this AI content
- `last_model_used` – which AI model generated it
- `created_at` – audit timestamp

This design allows you to:

- Store multiple AI versions per product
- Separate AI outputs per channel
- Evolve the payload structure without changing the schema every time

---

## 🚀 Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/mohamaddakhiliuad/fastapi-clean-architecture-demo.git
cd fastapi-clean-architecture-demo
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# یا در ویندوز:
# .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Set your PostgreSQL connection URL in `alembic.ini` and in your settings (e.g. `DATABASE_URL`). For example:

```ini
sqlalchemy.url = postgresql+psycopg2://postgres:password@localhost:5432/fastapi_demo
```

### 5. Run Alembic Migrations

```bash
alembic upgrade head
```

This will create the `products` and `ai_contents` tables.

### 6. Run the API Server

```bash
uvicorn app.main:app --reload
```

Then open:

- Swagger UI: `http://127.0.0.1:8000/docs`

---

## ✅ Example Workflows

### 1) Create a Product

`POST /api/v1/products/`

Example JSON:

```json
{
  "name": "Test Product",
  "sku": "SKU-123",
  "price": 49.99
}
```

### 2) Generate eBay Listing (AI Demo)

`POST /api/v1/products/{product_id}/generate/ebay`

Current implementation uses a **demo AI payload** (no external calls) to:

- Build a fake eBay listing
- Store it as an `AIContent` row
- Return it via the API

Later, this can be swapped with a real OpenAI integration without changing the API contract.

### 3) List AI Contents for a Product

`GET /api/v1/products/{product_id}/ai-contents`

Supports optional filters:

- `channel`
- `content_type`

Returns the full history of AI‑generated content for that product.

---

## 🧪 Testing Strategy (Conceptual)

This project is structured to support three levels of testing:

1. **Unit Tests**
   - On Service Layer (business rules)
   - On Repository functions (with a test DB or mocked session)

2. **Integration Tests**
   - Using FastAPI `TestClient`
   - Testing the full request → service → repository → DB → response flow

3. **Manual / Exploratory Testing**
   - Using Swagger UI or Postman
   - Quick validation of new endpoints and flows

You can add `pytest` tests under a `tests/` folder using this structure.

---

## 🧭 Why This Project Matters

This repo is designed as a **portfolio‑grade example** of how to build a scalable backend with FastAPI:

- Shows you understand **architecture**, نه فقط syntax
- Demonstrates clear separation of concerns
- Provides a realistic blueprint for AI‑enhanced backends
- Easy to extend:
  - more product fields
  - more AI channels (`/generate/shopify`, `/generate/instagram`, ...)
  - real AI integrations (OpenAI, local models, etc.)

If you’re evaluating this code as a recruiter, teammate, or client, focus on:

- The structure of layers (API → Service → Repository)
- How the domain models are separated from transport & persistence
- How AI is treated as an infrastructure concern, not hard‑coded into the API layer

---

## 📌 Roadmap Ideas

- [ ] Add real OpenAI integration for eBay listings
- [ ] Add more channels (Shopify descriptions, Instagram captions)
- [ ] Implement authentication & authorization
- [ ] Add background tasks (e.g., batch AI generation)
- [ ] Add pytest test suite and CI pipeline

---

## 🧑‍💻 Author

Built as a **clean architecture demo** for FastAPI, showcasing real‑world patterns for:

- API design
- Backend architecture
- AI‑augmented data flows

Feel free to fork, experiment, and adapt this structure to your own projects.

