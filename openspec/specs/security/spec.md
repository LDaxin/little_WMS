# security Specification

## Purpose
TBD - created by archiving change add-security-hardening. Update Purpose after archive.
## Requirements
### Requirement: HTTPS-capable settings

The system SHALL enable HTTPS-related settings (SSL redirect, secure cookies,
HSTS, proxy header) when the `SECURE_HTTPS` environment variable is set.

#### Scenario: HTTPS enabled

- **WHEN** `SECURE_HTTPS` is set
- **THEN** secure cookies, SSL redirect, and HSTS are enabled

#### Scenario: HTTPS disabled

- **WHEN** `SECURE_HTTPS` is not set
- **THEN** the settings stay off (local development)

### Requirement: Login rate limiting

The system SHALL limit failed login attempts per IP and per account, with a
temporary lockout, and SHALL log failed attempts.

#### Scenario: Too many failures for an account

- **WHEN** an account has too many failed attempts
- **THEN** further attempts are rejected until the lockout expires

#### Scenario: Too many failures from an IP

- **WHEN** an IP has too many failed attempts
- **THEN** further attempts from it are rejected

