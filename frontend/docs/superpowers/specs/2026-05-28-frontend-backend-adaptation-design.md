# Frontend-Backend Adaptation Design

**Date**: 2026-05-28
**Branch**: backend-develop
**Scope**: Adapt frontend pages to match backend API after pulling frontend from `njk-branch`

## Summary

Frontend was pulled from `njk-branch` into `backend-develop`. It needs adaptation to fully cover the backend's 9 algorithm modules (68 algorithms), fix bugs, and replace hardcoded content with dynamic data from the API.

## Backend Context (unchanged)

- **9 algorithm modules**, 68 algorithms total
- **No authentication system** — no login, users, or sessions
- All API responses use `{ "success": bool, ... }` envelope
- Processing supports optional `second_image_path` for two-image algorithms

## Changes

### 1. `src/utils/check_health.js` — Fix missing import

Add `import { ElMessage } from 'element-plus'`. Currently references `ElMessage` without importing it, causing a runtime error on health check.

### 2. `src/api/run.js` — Implement run API function

Replace the empty file with an exported `runAlgorithm(moduleSlug, payload)` function:

- Converts module name to endpoint slug (underscores → dashes)
- POSTs to `/api/algorithms/{slug}/run`
- Returns unwrapped response data

This removes the inline `http.post()` call from WorkspaceView.

### 3. `src/views/WorkspaceView.vue` — Core adaptation

Three changes:

- **Remove `moduleRunEndpointMap`**: Replace the hardcoded 6-module map with a computed URL from the module name (underscores → dashes). This enables all 9 modules without manual mapping.
- **Use `runAlgorithm()`**: Call the extracted API function instead of inline `http.post()`.
- **Add second image selector**: When the selected algorithm belongs to `basic_operation` (which has 8 algorithms requiring two images), show a dropdown populated from `GET /api/library/images?category=`. The selected image path is sent as `second_image_path` in the request body.

### 4. `src/views/HomeView.vue` — Dynamic algorithm data

Replace the hardcoded `algorithmModules` array (6 items) with a `fetch` call to `GET /api/algorithms`:

- Use `getAlgorithmService()` from `src/api/algorithms.js`
- Render module cards dynamically from the response
- Each card shows: display_name, description, algorithm count
- Add loading skeleton while fetching
- Show error state on failure

### 5. No changes needed

- `LoginView.vue` — kept as-is per user decision
- `UserProfileView.vue` — kept as-is per user decision
- `LibraryView.vue` — already correctly integrated with backend
- `HeaderNav.vue`, `MainLayout.vue`, `AppFooter.vue` — no API dependencies
- `NotFoundView.vue` — static page

## Files Modified

| File | Change |
|------|--------|
| `frontend/src/utils/check_health.js` | Add ElMessage import |
| `frontend/src/api/run.js` | Implement `runAlgorithm()` |
| `frontend/src/views/WorkspaceView.vue` | Remove endpoint map, use runAlgorithm(), add second image selector |
| `frontend/src/views/HomeView.vue` | Fetch real algorithm data, dynamic rendering |

## Implementation Order

1. Fix `check_health.js` (independent)
2. Implement `run.js` (independent)
3. Update `WorkspaceView.vue` (depends on run.js)
4. Update `HomeView.vue` (independent)
