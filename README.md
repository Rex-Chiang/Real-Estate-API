# Real Estate API

## Overview
This project used the real estate related data as resource from public government information platform. User will register an account to apply the token key, and retrieve data. The authentication would block the visit if user didn't provide token key when user request to retrieve data. According to the profile that user provide in register, there have three user level. Users with level 1 could retrieve the basic data, and users with level 2 or level 3 could retrieve advanced data. The permission setting would block the visit if level 1 user try to retrieve advanced data.

## Developing
**Built With:**
* Python3
* Django
* Django Rest Framwork
* PyMySQL
* Pandas
* Pytest

**Database:**
* SQLite3
* MySQL

## Tests
```
cd Real-Estate-API
python3 -m venv RealEstateEnv
source RealEstateEnv/bin/activate
pip3 install -r requirements.txt
cd RealEstateProject
python3 manage.py runserver
```

## Demo
![Demo](https://github.com/Rex-Chiang/Real-Estate-API/blob/main/Demo.gif)
