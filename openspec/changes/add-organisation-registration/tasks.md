## 1. Model

- [x] 1.1 `hub.Settings.registration_policy` + migration
- [x] 1.2 `OrganisationRequest` model + migration

## 2. Views and URLs

- [x] 2.1 Public `registerOrganisation` (open / request / invite)
- [x] 2.2 Server-admin `organisationRequests` list + approve/reject
- [x] 2.3 Server-admin `serverSettings` (policy)

## 3. Templates

- [x] 3.1 `register.html`, `organisationRequests.html`, `serverSettings.html`

## 4. Tests

- [x] 4.1 Open registration creates the org + admin
- [x] 4.2 Request registration records a pending request
- [x] 4.3 Invite-only shows the message
- [x] 4.4 Approve creates the org; reject does not
- [x] 4.5 Non-superuser gets 403 on the review page

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker for manual testing
