projectend
==========

calculate the end of projects.

```bash
pip install projectend
projectend example.toml
```

example:

```toml
[project]
name = "Mein Projekt"
start = 2021-05-05
# In hours
workday = 8.0

    [[project.tasks]]
    name = "DEV Entfernen Kolab-Attribute"
    # In hours
    effort = 4
    [[project.tasks]]
    name = "DEV Mailbestellung"
    effort = 5
    [[project.tasks]]
    name = "DEV Mehrfachrollen"
    effort = 6
    [[project.tasks]]
    name = "DEV Person nicht angelegt"
    effort = 4
    [[project.tasks]]
    name = "DEV Polygon"
    effort = 8
    [[project.tasks]]
    name = "DEV Umzubenennende Accounts"
    effort = 6
    [[project.tasks]]
    name = "Verzögerungen"
    effort = 8

    [[project.resources]]
    name = "dave"
    from = 2021-05-08
    to = 2021-05-16
    # Per day
    hours = 4
    # 0 = monday - 4 friday, empty = all weekdays
    weekdays = [0,2,3]

    [[project.resources]]
    name = "hans 1"
    from = 2021-05-05
    to = 2021-05-13
    hours = 4

    [[project.resources]]
    name = "hans 2"
    from = 2021-05-14
    to = 2021-06-01
    hours = 2
    exceptions = [2021-05-18]

[[freedays]]
name = "Auffahrt"
date = 2021-05-13

[[freedays]]
name = "Pfingstmontag"
date = 2021-05-24

[[freedays]]
name = "Nationalfeiertag"
date = 2021-08-01

```

output:

```
Simulating project: Mein Projekt

Week 18
Wed 2021-05-05    4.6 days (    37 hours) left
Thu 2021-05-06    4.1 days (    33 hours) left
Fri 2021-05-07    3.6 days (    29 hours) left

Week 19
Mon 2021-05-10    2.6 days (    21 hours) left
Tue 2021-05-11    2.1 days (    17 hours) left
Wed 2021-05-12    1.1 days (     9 hours) left
Fri 2021-05-14    0.9 days (     7 hours) left

Week 20
Mon 2021-05-17    0.6 days (     5 hours) left
Wed 2021-05-19    0.4 days (     3 hours) left
Thu 2021-05-20    0.1 days (     1 hours) left
Fri 2021-05-21   -0.1 days (    -1 hours) left

The project ends on 2021-05-22
```
