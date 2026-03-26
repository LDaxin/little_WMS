# HTML namespace
The html files are sorted in the different applications 
- hub
- part
- storage
- registration

These are the directories that contain the base html files. They are include modules and extend the `header.html`.

The modules are in a separate `modules` subfolder in the respective directory, which is in the `application` folder and don't extend the `header.html`.
Example: `django_project/hub/templates/hub/modules`