# hub Specification

## Purpose
TBD - created by archiving change centralize-toast-feedback. Update Purpose after archive.
## Requirements
### Requirement: Toast feedback

The system SHALL render feedback toasts (add / update / delete / error) through
a single helper, so views do not build the toast context themselves.

#### Scenario: A view reports success

- **WHEN** a view reports a successful action
- **THEN** a success toast is rendered

#### Scenario: A view reports an error

- **WHEN** a view reports an error
- **THEN** an error toast is rendered

