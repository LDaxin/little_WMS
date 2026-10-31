## ADDED Requirements

### Requirement: Onboarding wizard

The system SHALL provide an onboarding wizard that asks how the system will be
used and offers the standard article types, storage types, and role templates as
a pre-selected suggestion. Applying the selection SHALL create the chosen
defaults; skipping SHALL create nothing. Either way the wizard SHALL be marked
completed.

#### Scenario: Apply the suggestions

- **WHEN** the user applies the wizard's suggestions
- **THEN** the selected article types, storage types, and role templates are created

#### Scenario: Skip

- **WHEN** the user skips the wizard
- **THEN** nothing is created and the wizard is marked completed

#### Scenario: Restart

- **WHEN** the user restarts the wizard from the configuration page
- **THEN** the wizard is shown again
