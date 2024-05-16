# Syllabus

## Important Times and Dates

- Meeting location: online (Zoom link will be provided)
- Meeting days: Monday and Wednesday
- Meeting time: 7:10pm - 8:45pm
- Instructor office hours: Monday and Wedensday 9-10pm (requires appoinment)
- TA office hours: (see canvas)
- First day of class: April 1, 2024
- Last day of class: June 5, 2024

##  Important Links
- Discussion group: https://groups.google.com/g/ucsc2024-cse183
- Class code: https://github.com/ucsc2024-cse183/class_code
- Py4Web: https://py4web.com

Work done in class will be commited under class_code/lectures
Assignments will be posted under class_core/assignments

## The first week

The first week is the most important week. Not only a lot of critical material will be covered.
This is also the time when you will setup everything the class.
- read the syllabus https://github.com/ucsc2024-cse183/class_code
- setup your Linux machine
- upload your ssh key to github
- fill the Google form questionaire from the instructor
- `git clone {your git username}-code` repo
- run bootstrap-shell-cse183.sh
- test the `grade` script on the dummy assignment0

```
git clone https://github.com/ucsc2024-cse183/class_code.git
cd class_code
./bootstrap-shell-cse183.sh
```

## Class rules and policies

### Requirements

This class requires a Linux machine or a Linux VM or a Windows Subsystem for Linux.
Any Linux distribution is fine although the instructor recommends 1) Manjaro 2) Ubuntu 3) CantOS
You are supposed to be familiar with Linux and basic bash shell commands.
Instructor does not use Windows and any question mentining "Windows" will result in loss of points.

This class also requires familiarity with basic git commands (close, commit, push, pull, rebase)

### Important dates

- April 14 - Assignment 1 due
- April 21 - Assignment 2 due
- April 28 - Assignment 3 due
- May 5 - Assignment 4 due
- May 19 - Assignment 5 due
- June 5 - Final project due
- June 9 - Crowdgrader project review due

### Assignment submissions

Assignments are to be submitted using the github created for you by the instructor.
They are also to be submitted using crowdgrader.com.

### Grading

Your score is computed in points, not percentages. Each assignment/project will earn you some points. Up to 12 points for each of the 5 assignemnts and up to 50 points for the final project. This means you can earn up to 110 points (not incuding extra cerdit). Anything above 93 points is an A in the class. This means you can miss an assignment and still get an A in the class. If you miss 2 assignments you can still get a B.

Late assignments are not accepted and there is way to make up for a missed assignments.

There will be options for extra credit but, typically, extra credit projects are much more advanced and challenging than regular assignemnts. Extra credit is not designed to make up for missing work or low grades. It is designed to give you an opportunity to show off you advanced skills.

Part of your final project grade will be computed using crowdgrader, a collaborative peer grading tool.
Another component will be evaulated based on your specific commits.

You can lose points if you ask questions about Windows setup or about isses that were
discussed in class or on the google group.

Points will be converted to grade based on this scale:
- A >93
- A- 90-92
- B+ 88-89
- B 83-87
- B- 80-82
- C+ 78-79
- C 73-77
- C- 70-72
- D+ 68-69
- D 63-67
- D- 60-62
- F 59 and below

### Discussions

Do not send email to the instructor about questions on the class content. All discussions on class content should be done on the google group linked above. Students are encouraged to help others. Students who help the most may rewarded with extra credit at the instructor's discretion.

### Office hours

Before using office hours ask for help to the Tutors/TAs.
Students are expected to come prepared with specific questions or topics they need help with.
Review the course material before attending office hours. If you plan to attend office hours, let the professor known during class time. 

For matters not covered during office hours, such as career advice or personal issues, students are encouraged to seek out other resources provided by the institution, such as career services or counseling centers.

### Plagiarism

In our class, academic integrity is paramount. Every student is expected to uphold the highest standards of honesty and ethical behavior. Submitting someone else's work as your own, whether it be from a book, article, another student, or any other source—is a serious violation of these standards.

Definition: Plagiarism includes, but is not limited to, copying text directly without quotation marks and proper citation, paraphrasing someone else's ideas without acknowledging the original source, submitting assignments meant for another class as if they were original work for this class, and using unauthorized assistance to complete assignments.

Consequences: Any instance of plagiarism will be taken very seriously. Depending on the severity and nature of the violation, consequences may range from receiving a zero on the assignment to more severe academic penalties such as failing the course or disciplinary action by the institution. Every case of plagiarism will also be reported to the appropriate academic authorities.

## Course Plan

### Week 1 - April 1
- discuss class rules and policies
- settings things up (the bootstrap-csc183 script)
- TCP/IP protocol
- HTTP protocol
- implement a minimalist web server in Python
- basic structure and syntax of HTML
- basic CSS rules for styling a page (color, font, size, position)
- box text model concept
- the Bulma CSS library and the grid system

### Week 2 - April 8
- HTML forms and user input
- JavaScript basics: Variables, data types, functions, and control structures.
- DOM manipulation: Selecting and modifying webpage elements dynamically.
- Event handling: Responding to user inputs and actions.
- Introduction to Vue.js: Core concepts and advantages of using Vue.
- Vue instance, data binding, and directives: Building dynamic, reactive web interfaces.

### Week 3 - April 15
- Overview of web frameworks (routing, templates, sessions, caching, databases, CRUD)
- The model-view-controller architecture

### Week 4 - April 22
- The database abstraction layer
- RESTful API and web services

### Week 5 - April 29
- py4web forms and grid
- Basic Auth and single sign on

### Week 6 - May 6
- Putting it all together, an Ecommerce app.
- Project discussions

### Week 7 - May 13
- Handling file uploads
- Security

### Week 8 - May 20
- Examples of Vue components
- Running tasks in background
- Internationalization (i18n) and pluralization (p13n)

### Week 9 - May 27
- Single server deployment (docker compose + caddy)
- Help finalize projects

### Week 10 - June 3
- Scaling web applications
- Optional topics

## Reading Suggestions

Week 1 - Suggested readings
- https://reintech.io/blog/how-to-create-a-simple-web-server-with-python
- https://www.cloudflare.com/learning/network-layer/internet-protocol/
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- https://www.youtube.com/watch?v=UVR9lhUGAyU (video)
- https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
- https://html.com/
- https://www3.ntu.edu.sg/home/ehchua/programming/webprogramming/HTML_CSS_Basics.html
