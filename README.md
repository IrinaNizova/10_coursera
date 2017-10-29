# Coursera Dump

This script read courses from coursera xml-feed and write its title, language, average rating,
number of weeks, start date on xlsx file

# How to start

## Install requirements:
```
pip install -r requirements.txt
```

## Optional parameters:

-n --count <number> - count of courses, default 20

-f --filepath <string> - file to save, default courses_info.xlsx

## Example of lanch:
```
python coursera.py

python coursera.py -n 2 -f courses.xlsx
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
