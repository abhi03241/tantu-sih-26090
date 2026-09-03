# TANTU - Frontend & Mobile UI Module

**Maintained by Team Member P (Frontend/Mobile UI Lead)**

This directory contains the user interface components for the **TANTU** Smart India Hackathon (SIH 26090) prototype application.

## API Integration Quickstart

The backend is running at `http://localhost:8000`.

### Key Backend Endpoints for Frontend Integration:

1. **Artisan Cataloging View**:
   - `POST /api/products` (Create product)
   - `POST /api/products/{id}/voice` (Trigger Voice-to-Text AI cataloging)
   - `POST /api/products/{id}/enhance-image` (Trigger AI Studio image enhancement)

2. **Artisan Dashboard**:
   - `GET /api/artisan/products?artisan_id=art-001` (List artisan's uploaded products)

3. **Buyer Marketplace Feed**:
   - `GET /api/buyer/products` (Browse catalog with filter & search)
   - `POST /api/orders/request` (Submit bulk B2B inquiry/order)

### Sample Product Response Format
Refer to [docs/API_CONTRACTS.md](../docs/API_CONTRACTS.md) for full JSON schema details.
