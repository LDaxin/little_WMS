## 1. Model

- [x] 1.1 `LendLink` (TokenisedModel) in `loans/models.py`
- [x] 1.2 Migration

## 2. Views & URLs

- [x] 2.1 `lendLinks` (list + create) and `lendLinkRevoke` for members
- [x] 2.2 `lendLinkView` (public form + status)
- [x] 2.3 URLs

## 3. Templates

- [x] 3.1 `loans/lendLinks.html` (member list/create)
- [x] 3.2 `loans/lendLink.html` (public form + status)
- [x] 3.3 Link from the loans page

## 4. Lending

- [x] 4.1 Create the borrowed article (type, base, stock, photo)
- [x] 4.2 Create the loan + calendar entry

## 5. Tests

- [x] 5.1 Create/revoke a link; submit the form; status; invalid link

## 6. Verify

- [x] 6.1 Full suite green in Docker
- [x] 6.2 Rebuild + restart
