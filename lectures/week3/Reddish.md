Data Model

table Auth (free)
- username
- first name
- last name
- password
- email

table community
- name

table entry
- belong to a community
- title: string
- descriptionL string
- post date: datestamp
- author: reference to a user
- score: integer

table comment:
- belong to an entry
- body
- author

Pages
- home page (per community)
- post a new entry
- page to see comments and post comments

Admin Database Interface (free)
- manage communities

Automatically generated (free)
- login
- logout
- register
- edit my profile
- verify email
- retrieve your password
- 2 FA
  