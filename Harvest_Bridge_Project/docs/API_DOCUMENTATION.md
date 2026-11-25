# Harvest Bridge API

Interactive OpenAPI documentation: `GET /docs`. Routes are under `/api`.

## Authentication

- `POST /api/auth/register`: farmer/buyer only; accepts name, 10+ character password, optional email/phone, language and location.
- `POST /api/auth/login`: `{ "username": "email or phone", "password": "..." }`; returns bearer JWT and role.
- `POST /api/auth/logout`: stateless-token acknowledgement; client clears token locally.
- `POST /api/auth/refresh`: valid access JWT to fresh JWT.
- `POST /api/auth/forgot-password`: safe generic response; message delivery is not configured.
- `GET /api/me`: current account.

Send `Authorization: Bearer <access_token>` for protected operations. Tokens expire per `ACCESS_TOKEN_MINUTES` (default 60). Admin is configured/seeded, never publicly registered.

## Marketplace and farmer

- `GET /api/products?q=&crop=&district=&organic=&urgent=&sort=&page=&limit=`; sort supports `urgent` (default), `price`, `risk`, `newest`, `priority`.
- `GET /api/products/{id}`, `/urgent`, `/organic`.
- `GET/POST /api/farmer/products`; `PUT/DELETE /api/farmer/products/{id}`.
- `POST /api/farmer/products/{id}/status`: `active`, `paused`, `sold`.
- `POST /api/uploads/image`: authenticated JPG/PNG/WebP, up to 5 MB; local disk fallback.
- `GET /api/products/{id}/risk`, `POST .../risk/calculate`.
- `GET /api/storage/{crop}`: general guidance with source limitations.

## Buyer and matching

- `POST/GET /api/buyer/requirements`, `PUT/DELETE /api/buyer/requirements/{id}`.
- `GET /api/matches`, `POST /api/matches/calculate?requirement_id=`: deterministic score out of 100 and reason list.
- `POST /api/enquiries`: buyer enquiry with product, quantity, optional offer and message.
- `GET /api/enquiries`: own records; admin can inspect all.
- `PUT /api/enquiries/{id}/status`: participant/admin update. `deal confirmed` records an unpaid deal amount; it does not process payment.
- `GET /api/notifications`: current account notifications.

## Prices and admin

- `GET /api/prices?crop=`, `/api/prices/crop/{name}`, `/api/prices/nearby?state=` return stored records with source, market date, unit and sample flag.
- `POST /api/admin/prices/import`: admin dated record entry; verifies minimum ≤ modal ≤ maximum.
- `GET /api/admin/dashboard`, `/users`, `/products`; `PUT /api/admin/users/{id}/status`; `PUT /api/admin/products/{id}/priority`; `POST /api/admin/organic/verify?product_id=&status=`.
- `GET /api/health`: DB and optional integration config status. `GET /api/weather?location=` reports unavailable until live adapter is enabled.

Asking prices are INR/kg entered by sellers. Mandi prices preserve the source unit (default INR/quintal); the app does not silently compare unlike units. Demo prices are seller-entered, never official mandi rates. Pydantic validates request data and SQLAlchemy parameterizes database queries.
