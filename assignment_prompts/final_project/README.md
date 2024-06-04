Submission rules:
- By Thursday June 6 at 11:59 you will need to download your project (from the Dashboard page)
  and upload it into https://www.crowdgrader.org/ (details to be provided)
  ONLY THE LEAD OF THE GROUP SHOULD DO THE UPLOAD
- By Sunday June 10 at 11:59 you will need to review 4 projects from colleagues assigned to you.

Please edit the project metadata.json and make sure the list of collaborators is correct.

You final project consists of creating a task management app. Tasks have a title, a desciption, a signature (created_on, created_by), a deadline, and a status (pending, ackowledged, rejected, completed, failed). Task also have comments.

You you create tasks and assign them to yourself and/or other users. Every user must have a manager (another user), except the CEO, and every user can edit their own tasks as well the tasks created by people he/she manages.

Every user should be able to:
- select and change own manager
- create a task
- see all the tasks
- edit a task (any field) but only if created by self or a managed person (important!)
- add a comment to any task
- filter tasks by:
  - date created
  - deadline
  - status
  - created by self
  - assigned to self
  - created by a specific user
  - assigned to a specific user
  - created by any managed user
  - assigned to any managed user

You must use py4web. Vue is optional.

Different members of a team should be assigned a clear responsibility, perhaps a specific page. One person must be the group leader with the responsibility of submitted the final project. Teams will be assigned by the professor. Your team picks the group leader.

## Grading

- 15 points of the grade will be assigned based on whether the above requirements are met and the app works.
- 15 will be based on your own contribution (actual number of lines contributed to a .py, .js, .html file, relative to your team mates)
- 10 points Assigned by your peers using crowdgrader (mostly judging readability and usability)
- 10 points Will be be based on the overall quality of the result (at total discretion of the professor)
