# 🧺 LaundroMate: MVP SaaS for Full-Service Laundromats

**LaundroMate** is a modern, API-first SaaS platform designed for full-service, multi-location laundromats. It enables online ordering, in-store POS for Wash & Fold, and account management — optimized for mobile and built with modular architecture to support rapid iteration and intelligent agent integration in future phases.

---

## 🚀 MVP Scope

### 1. Online Pickup & Delivery (P&D)

- Address validation
- Service + preference selection
- Pickup/delivery time slot selection
- Order summary + estimate
- Customer login/registration
- Admin order dashboard (view, confirm)

### 2. Wash & Fold POS (In-Store)

- Customer lookup + creation
- Laundry weight input
- Status tracking: Received → Washing → Drying → Folding → Ready → Completed
- Manual payment logging
- Printable ticket (PDF with barcode)

### 3. Customer Account & Notifications

- Login / profile management
- View all orders + statuses
- SMS/email notifications for order events

---

## 🧠 Long-Term Vision: LaundroAgent (Coming Soon)

- Auto-scheduling & rescheduling
- Order issue triage
- Summarization of daily ops
- Staff alerts & workflow automation

### Integrations & Analytics (Post‑MVP)

- Business analytics dashboards (orders, AOV, retention, route efficiency)
- Accounting integrations (QuickBooks, Xero) for revenue and reconciliation
- POS/e‑commerce integrations (Square, Shopify) for unified catalog and payments
- Webhooks + Zapier/Make for workflow automation

### AI Voice Assistant (Post‑MVP)

- Voice‑powered customer service (status, scheduling, FAQs)
- Intelligent call summaries and follow‑ups
- Agent escalation and issue classification

---

## 🧱 Tech Stack

| Layer         | Tech                            |
| ------------- | ------------------------------- |
| Frontend      | Next.js + Tailwind CSS          |
| Backend       | FastAPI (Python) OR NestJS (TS) |
| Auth          | Clerk (IdP) + JWT for invitation |
| DB            | PostgreSQL                      |
| Async Queue   | Celery (Python) / BullMQ (TS)   |
| Notifications | Twilio (SMS), SendGrid (Email)  |
| DevOps        | GitHub Actions + AWS (Fargate)  |

---

## 📁 Folder Structure

/apps
/web # Next.js frontend
/api # FastAPI or NestJS backend

/packages
/ui # Shared UI components (buttons, inputs)
/types # Shared TypeScript types/interfaces
/utils # Shared utilities (validators, formatters)

.env # Environment variables
docker-compose.yml

---

## 🧩 Core API Modules

| Module          | Endpoint Group | Description                      |
| --------------- | -------------- | -------------------------------- |
| `auth`          | `/auth/*`      | Login, register, session mgmt    |
| `orders`        | `/orders/*`    | Create + track W&F + P&D orders  |
| `customers`     | `/customers/*` | Profiles, addresses, preferences |
| `notifications` | `/notify/*`    | Triggers SMS/email               |

---

## 🧱 Component Breakdown

### `/web/components`

| Component                  | Description                   |
| -------------------------- | ----------------------------- |
| `OrderFormWizard.tsx`      | Step-by-step P&D order flow   |
| `PickupTimeSelector.tsx`   | Date + time slot picker       |
| `OrderSummaryCard.tsx`     | Final order review            |
| `OrderTable.tsx`           | Admin view of W&F/P&D orders  |
| `StatusBadge.tsx`          | Status label for orders       |
| `CustomerPortalLayout.tsx` | Authenticated portal UI shell |

---

## ⚙️ Setup Instructions

### 1. Clone & Install

```bash
git remote add origin https://github.com/Dansong00/laundromate.git
cd laundroMate
pnpm install
```
