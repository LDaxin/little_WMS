## 1. App and settings

- [x] 1.1 Create the `api` app (apps.py, `INSTALLED_APPS`)
- [x] 1.2 `REST_FRAMEWORK` settings (auth, default permission)
- [x] 1.3 Remove the broken `article/serializer.py`

## 2. Serializers and viewsets

- [x] 2.1 Serializers for the main models
- [x] 2.2 Read-only viewsets with `permission_area`
- [x] 2.3 `/api/v1/` router + root urls

## 3. Permissions

- [x] 3.1 `RolePermission`

## 4. Tests

- [x] 4.1 List/retrieve returns data
- [x] 4.2 Unauthenticated request is rejected
- [x] 4.3 Missing permission → 403

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker for manual testing
