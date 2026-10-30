# QR Sheet Printing Specification

## Purpose

Print QR labels for articles and storages on sheets: select items, choose a
grid format, size, and label content, and print via the browser.

## Requirements

### Requirement: Printable QR sheet

The system SHALL render a printable sheet of QR codes for the selected articles
or storages.

#### Scenario: Print selected articles

- **WHEN** the user selects articles and requests a QR sheet
- **THEN** a printable page with a QR code per article is rendered

#### Scenario: Print selected storages

- **WHEN** the user selects storages and requests a QR sheet
- **THEN** a printable page with a QR code per storage is rendered

### Requirement: Format and content options

The system SHALL let the user choose the grid format, the QR size, the label
content, and whether the QR encodes the code or a link.

#### Scenario: Choose a format

- **WHEN** the user picks a grid format and size
- **THEN** the sheet is laid out accordingly

#### Scenario: QR encodes a link

- **WHEN** the user chooses "link" as the QR content
- **THEN** each QR encodes the absolute URL of the item instead of its code
