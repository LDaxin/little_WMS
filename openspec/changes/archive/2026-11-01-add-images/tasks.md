## 1. Setup

- [x] 1.1 Add Pillow to `requirements.txt`
- [x] 1.2 Add `MEDIA_ROOT`/`MEDIA_URL` to settings and dev media serving to the root urlconf

## 2. Models

- [x] 2.1 `BaseImage` abstract model + `ArticleImage` and `StorageImage`
- [x] 2.2 Resize + thumbnail on save; delete the file on delete
- [x] 2.3 Migration for both models

## 3. Views & URLs

- [x] 3.1 Upload view (article + storage)
- [x] 3.2 Delete and set-primary views
- [x] 3.3 URLs

## 4. Templates

- [x] 4.1 Gallery + upload form on the detail page (`item.html`)
- [x] 4.2 Thumbnail column in the list (`results.html`)

## 5. Tests

- [x] 5.1 Model tests (primary, resize, thumbnail, delete)
- [x] 5.2 View tests (upload, delete, set-primary)

## 6. Verify

- [x] 6.1 Full test suite green in Docker
- [x] 6.2 Rebuild Docker and restart the container
