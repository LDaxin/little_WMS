## 1. Models

- [x] 1.1 `FloorPlan` and `FloorPlanArea` in `storage/models.py`
- [x] 1.2 Migration

## 2. Views & URLs

- [x] 2.1 Plan view (display + highlight)
- [x] 2.2 Upload/replace plan image
- [x] 2.3 Save areas (JSON from the editor)
- [x] 2.4 URLs
- [x] 2.5 Area click prefers the target storage's own plan

## 3. Templates

- [x] 3.1 Plan display with clickable SVG areas (`floorPlan.html`)
- [x] 3.2 Drawing editor (`floorPlanEditor.html`)
- [x] 3.3 Link to the plan from the storage detail page
- [x] 3.4 Back link from the plan to the storage detail page

## 4. Tests

- [x] 4.1 Model tests (plan, areas, replace keeps areas)
- [x] 4.2 View tests (upload, save areas, click target, highlight)

## 5. Verify

- [x] 5.1 Full test suite green in Docker
- [x] 5.2 Rebuild Docker and restart the container
