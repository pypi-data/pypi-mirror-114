# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['projectend']
install_requires = \
['click>=7.1.2', 'intervaltree>=3.1.0', 'toml>=0.10.2']

entry_points = \
{'console_scripts': ['projectend = projectend:cmd']}

setup_kwargs = {
    'name': 'projectend',
    'version': '0.14.0',
    'description': 'calculate the end of projects',
    'long_description': 'projectend\n==========\n\ncalculate the end of projects.\n\n```bash\npip install projectend\nprojectend example.toml\n```\n\nexample:\n\n```toml\n[project]\nname = "Mein Projekt"\nstart = 2021-05-05\n# In hours\nworkday = 8.0\n\n    [[project.tasks]]\n    name = "DEV Entfernen Kolab-Attribute"\n    # In hours\n    effort = 4\n    [[project.tasks]]\n    name = "DEV Mailbestellung"\n    effort = 5\n    [[project.tasks]]\n    name = "DEV Mehrfachrollen"\n    effort = 6\n    [[project.tasks]]\n    name = "DEV Person nicht angelegt"\n    effort = 4\n    [[project.tasks]]\n    name = "DEV Polygon"\n    effort = 8\n    [[project.tasks]]\n    name = "DEV Umzubenennende Accounts"\n    effort = 6\n    [[project.tasks]]\n    name = "Verzögerungen"\n    effort = 8\n\n    [[project.resources]]\n    name = "dave"\n    from = 2021-05-08\n    to = 2021-05-16\n    # Per day\n    hours = 4\n    # 0 = monday - 4 friday, empty = all weekdays\n    weekdays = [0,2,3]\n\n    [[project.resources]]\n    name = "hans 1"\n    from = 2021-05-05\n    to = 2021-05-13\n    hours = 4\n\n    [[project.resources]]\n    name = "hans 2"\n    from = 2021-05-14\n    to = 2021-06-01\n    hours = 2\n    exceptions = [2021-05-18]\n\n[[freedays]]\nname = "Auffahrt"\ndate = 2021-05-13\n\n[[freedays]]\nname = "Pfingstmontag"\ndate = 2021-05-24\n\n[[freedays]]\nname = "Nationalfeiertag"\ndate = 2021-08-01\n\n```\n\noutput:\n\n```\nSimulating project: Mein Projekt\n\nWeek 18\nWed 2021-05-05    4.6 days (    37 hours) left\nThu 2021-05-06    4.1 days (    33 hours) left\nFri 2021-05-07    3.6 days (    29 hours) left\n\nWeek 19\nMon 2021-05-10    2.6 days (    21 hours) left\nTue 2021-05-11    2.1 days (    17 hours) left\nWed 2021-05-12    1.1 days (     9 hours) left\nFri 2021-05-14    0.9 days (     7 hours) left\n\nWeek 20\nMon 2021-05-17    0.6 days (     5 hours) left\nWed 2021-05-19    0.4 days (     3 hours) left\nThu 2021-05-20    0.1 days (     1 hours) left\nFri 2021-05-21   -0.1 days (    -1 hours) left\n\nThe project ends on 2021-05-22\n```\n',
    'author': 'Jean-Louis Fuchs',
    'author_email': 'jean-louis.fuchs@adfinis-sygroup.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ganwell/projectend',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
