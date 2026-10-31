## 1. Settings

- [ ] 1.1 `LANGUAGES`, `LOCALE_PATHS`, `LocaleMiddleware`

## 2. Per-user language

- [ ] 2.1 `UserProfile.language` (default English) + migration
- [ ] 2.2 `UserLanguageMiddleware` activates the profile language

## 3. UI

- [ ] 3.1 Language selector on the preferences page

## 4. Import strings

- [ ] 4.1 Wrap the import service and templates with `gettext` / `{% trans %}`

## 5. Tests

- [ ] 5.1 Default language is English
- [ ] 5.2 A set language is activated
- [ ] 5.3 The selector stores the language

## 6. Verify

- [ ] 6.1 Full test suite green in Docker
- [ ] 6.2 Rebuild Docker for manual testing
