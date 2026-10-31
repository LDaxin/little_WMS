## 1. Settings

- [x] 1.1 `LANGUAGES`, `LOCALE_PATHS`, `LocaleMiddleware`

## 2. Per-user language

- [x] 2.1 `UserProfile.language` (default English) + migration
- [x] 2.2 `UserLanguageMiddleware` activates the profile language

## 3. UI

- [x] 3.1 Language selector on the preferences page

## 4. Import strings

- [x] 4.1 Wrap the import service and templates with `gettext` / `{% trans %}`

## 5. Tests

- [x] 5.1 Default language is English
- [x] 5.2 A set language is activated
- [x] 5.3 The selector stores the language

## 6. Verify

- [x] 6.1 Full test suite green in Docker
- [x] 6.2 Rebuild Docker for manual testing
