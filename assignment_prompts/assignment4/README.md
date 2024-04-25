You must complete the provided bird_spotter app. It is a single page app.

The main page is in apps/bird_spotter/static/index.html and in apps/bird_spotter/static/js/index.js
- `/bird_spotter/` should redirect to `/bird_spotter/static/index.html` or turn it into a template (1 point)
- in models.py define a database table to store birds, a "bird" should have an "id", a "name", an "habitat" (string), a "weight" (positive number), and a number of "sightings" (positive number) (1 point)
- create a POST endpoint `api/birds` to register a new bird as required by index.js (1 point)
- create a GET endpoint `api/birds` to get birds as required by index.js (1 point)
- create a POST endpoint `api/birds/{id}/increase_sightings` to increase the number of sightings by 1 (no body in POST) as required by index.js (1 point)
- create a PUT endpoint `api/birds/{id}` to update bird info as required by index.js (1 point)
- create a DELETE endpoint `api/birds/{id}` to delete a bird (1 point)
- wire the API to get birds in the JS (0.5 point)
- wire the API to register a bird in the JS (use validate_and_insert) (0.5 point)
- wire the API to increase sightings in the JS (0.5 point)
- wire the API to update the bird info in the JS (use validate_and_update) (0.5 point)
- add validators to the table to prevent invalid inputs and duplicated birds (1 point)
- modify the app to display the errors returned by the JS (for example negative weight) (2 point)

IMPORTANT:
Do not use authentication (no auth object) else the grader will not work.
You should use db and session fixtures.
