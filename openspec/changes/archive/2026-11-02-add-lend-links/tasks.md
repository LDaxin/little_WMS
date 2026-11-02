## 1. Model

- [x] 1.1 `LendLink` (TokenisedModel) with `lender_name`/`lender_email`
- [x] 1.2 `Loan.lend_link`
- [x] 1.3 Migration

## 2. Views & URLs

- [x] 2.1 `lendLinks` (list + create) and `lendLinkRevoke` (deactivate + remove + anonymise)
- [x] 2.2 `lendLinkView` (details, list, add, edit, delete)
- [x] 2.3 URLs

## 3. Templates

- [x] 3.1 `loans/lendLinks.html` (member list/create)
- [x] 3.2 `loans/lendLink.html` (details form, item list, add/edit)
- [x] 3.3 Link from the loans page

## 4. Tests

- [x] 4.1 Create/deactivate a link; details; add/edit/delete; invalid link

## 5. Verify

- [x] 5.1 Full suite green in Docker
- [x] 5.2 Rebuild + restart
