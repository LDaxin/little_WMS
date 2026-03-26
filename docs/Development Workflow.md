# Development Workflow

1. Create a [issue](https://kanban.krauseadrian.de/project/little-wms/issues) with a title
2. Describe what the bug, feature, or question is about
3. Set the [issue](https://kanban.krauseadrian.de/project/little-wms/issues) to the correct type and set the [issue](https://kanban.krauseadrian.de/project/little-wms/issues) status to "spelled out"
4. If you can, select a Severity and Priority
5. Now other contributors can comment on the [issue](https://kanban.krauseadrian.de/project/little-wms/issues) and discuss if, how, Priority, Severity, and when the bug or feature gets implemented or fixed
  1. If the [issue](https://kanban.krauseadrian.de/project/little-wms/issues) is a question and gets answered, mark it as answered.
6. If the [issue](https://kanban.krauseadrian.de/project/little-wms/issues) is ready to be worked on, promote it to the [Kanban](https://kanban.krauseadrian.de/project/little-wms/kanban) (user story) and set the [issue](https://kanban.krauseadrian.de/project/little-wms/issues) status to "in [Kanban](https://kanban.krauseadrian.de/project/little-wms/kanban)"
  - When an [issue](https://kanban.krauseadrian.de/project/little-wms/issues) is promoted to [Kanban](https://kanban.krauseadrian.de/project/little-wms/kanban), all communication is now done on the [Kanban](https://kanban.krauseadrian.de/project/little-wms/kanban) task
8. Want to work on something:
  - If you want to work on something that is not in the [Kanban](https://kanban.krauseadrian.de/project/little-wms/kanban), promote it and assign it to yourself
  - If it is already in the [Kanban](https://kanban.krauseadrian.de/project/little-wms/kanban), just assign it to yourself
9. If it got assigned, move it to Ready
10. If you start working on it, move the task to In Progress
11. Create a new git branch with dev as the origin with the following structure:
  - The type of change (doc, feat, or bug) followed by / then the ID of the [Kanban](https://kanban.krauseadrian.de/project/little-wms/kanban) task followed by / with a short name in [camelCase](https://en.wikipedia.org/wiki/Camel_case) for easier readability.
  - For example bug/67/MultySelectError
  - Put the branch name in the field "Git branch name" for easy traceability
12. When the work is finished, move the task to Ready for testing and ask in the group if someone wants to check it
13. When someone checked it and commented on the [Kanban](https://kanban.krauseadrian.de/project/little-wms/kanban) task that it is fine, then it can be merged into the dev branch
14. Move the [Kanban](https://kanban.krauseadrian.de/project/little-wms/kanban) task to Done
15. The task gets moved to archived only by the project manager
