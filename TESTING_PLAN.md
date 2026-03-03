# Testing Plan: User Story 1 - Super Admin Dashboard

## Overview
This document outlines the testing plan for User Story 1: Organization and Store Onboarding (Super Admin Dashboard).

## Prerequisites
- Docker & Docker Compose installed and running
- Database migrations are up to date
- API and Web services can start successfully

## Step-by-Step Testing Plan

### 1. Start Docker Compose Stack

```bash
# From project root
docker compose up -d
```

This will start:
- PostgreSQL database
- Redis (if needed)
- Any other required services

Verify services are running:
```bash
docker compose ps
```

### 2. Run Database Migrations

```bash
cd apps/api
alembic upgrade head
```

### 3. Create Super Admin User

#### Option A: Using the Script (Recommended)
```bash
cd apps/api
./scripts/create-super-admin.sh "+1234567890" "superadmin@laundromate.com" "Super" "Admin"
```

#### Option B: Manual Database Insert
```bash
docker compose exec postgres psql -U laundromate -d laundromate -c "
INSERT INTO users (id, phone, email, first_name, last_name, is_super_admin, is_admin, is_active, created_at, updated_at)
VALUES (
  gen_random_uuid(),
  '+1234567890',
  'superadmin@laundromate.com',
  'Super',
  'Admin',
  true,
  true,
  true,
  now(),
  now()
);
"
```

### 4. Start API Server

```bash
cd apps/api
uvicorn app.main:app --reload
```

Verify API is running:
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs

### 5. Start Web Server

```bash
cd apps/web
pnpm dev
```

Verify web app is running:
- Frontend: http://localhost:3000

### 6. Sign In as Super Admin

1. Navigate to http://localhost:3000/auth/login
2. Sign-in is via Identity Provider (IdP). OTP login has been removed. Once IdP (Auth0, Clerk, etc.) is integrated, sign in with the super admin email. See `docs/IDP_MIGRATION_PLAN.md`.
3. For local testing without IdP: use the invitation flow to get a token, or call the API with a token created for the super admin user (e.g. via a small script using `create_access_token`).

### 7. Access Super Admin Dashboard

Navigate to:
- Organizations list: http://localhost:3000/super-admin/organizations
- Create organization: http://localhost:3000/super-admin/organizations/new

### 8. Test CRUD Operations

#### A. Create Organization
1. Click "New Organization" or navigate to `/super-admin/organizations/new`
2. Fill in the organization wizard:
   - **Step 1 - Organization Details:**
     - Name: "Test Organization"
     - Billing Address: "123 Main St"
     - City: "New York"
     - State: "NY"
     - Postal Code: "10001"
     - Country: "US"
     - Contact Email: "test@example.com" (optional)
     - Contact Phone: "+1234567890" (optional)
   - **Step 2 - Store Details:**
     - Store Name: "Test Store"
     - Street Address: "456 Store Ave"
     - City: "New York"
     - State: "NY"
     - Postal Code: "10002"
     - Country: "US"
   - **Step 3 - Invite Owner:**
     - Click "Complete & View Organization" (can invite later)

#### B. View Organization List
1. Navigate to `/super-admin/organizations`
2. Verify your created organization appears in the list
3. Check that all fields are displayed correctly

#### C. View Organization Details
1. Click on an organization from the list
2. Verify all organization details are displayed
3. Check that the store list is visible
4. Verify the organization information card shows correct data

#### D. Create Store
1. From organization detail page, click "New Store"
2. Fill in store form:
   - Store Name: "Second Store"
   - Street Address: "789 Another St"
   - City: "New York"
   - State: "NY"
   - Postal Code: "10003"
   - Country: "US"
3. Click "Create Store"
4. Verify redirect to store detail page

#### E. View Store Details
1. Navigate to a store detail page
2. Verify all store details are displayed
3. Check organization link works
4. Verify status badge displays correctly

#### F. Test Invitation Flow (Optional)
1. From organization detail page, use the invitation endpoint
2. Send invitation to an email
3. Check email for invitation link
4. Navigate to invitation acceptance page
5. Set password and complete account creation

### 9. Test Edge Cases

#### A. Empty States
- Navigate to organizations list with no organizations
- Verify empty state message displays

#### B. Error Handling
- Try creating organization with invalid data
- Verify error messages display correctly
- Check API returns proper error responses

#### C. Loading States
- Check loading spinners appear during API calls
- Verify forms disable during submission

#### D. Navigation
- Test browser back/forward buttons
- Verify breadcrumbs/navigation links work
- Check deep linking to organization/store pages

### 10. Verify API Endpoints

Test endpoints directly using API docs (http://localhost:8000/docs):

1. **GET /super-admin/organizations** - List organizations
2. **POST /super-admin/organizations** - Create organization
3. **GET /super-admin/organizations/{id}** - Get organization
4. **PUT /super-admin/organizations/{id}** - Update organization
5. **GET /super-admin/stores/organizations/{id}/stores** - List stores
6. **POST /super-admin/stores/organizations/{id}/stores** - Create store
7. **GET /super-admin/stores/{id}** - Get store
8. **PUT /super-admin/stores/{id}** - Update store

## Success Criteria

✅ **All CRUD operations work correctly:**
- Organizations can be created, read, updated (if implemented)
- Stores can be created, read, updated (if implemented)
- Data persists correctly in database

✅ **Authentication & Authorization:**
- Only super admin users can access routes
- Non-super admin users get 403 errors
- Unauthenticated users get 401 errors

✅ **UI/UX:**
- Forms validate input correctly
- Error messages are user-friendly
- Loading states work properly
- Navigation is intuitive

✅ **Data Integrity:**
- Organizations and stores are linked correctly
- Foreign key relationships work
- Cascade deletes work (if implemented)

## Troubleshooting

### Issue: Cannot connect to database
- Check `docker compose ps` - PostgreSQL should be running
- Check database connection string in `.env` file
- Verify migrations ran successfully

### Issue: Cannot login
- Verify super admin user was created
- Check OTP is being generated (check API logs)
- Verify phone number matches exactly

### Issue: 403 Forbidden on super admin routes
- Verify user has `is_super_admin = true` in database
- Check JWT token is being sent with requests
- Verify token hasn't expired

### Issue: API errors
- Check API logs for detailed error messages
- Verify database schema matches migrations
- Check CORS settings if frontend can't connect

## Notes

- OTP codes are printed to console in development mode
- Database can be inspected directly: `docker compose exec postgres psql -U laundromate -d laundromate`
- API docs available at `/docs` for interactive testing
- Check browser console for frontend errors
