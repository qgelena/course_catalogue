# course_catalogue

## Requirements:

Python >= 3.7

## Розгортання і запуск:

### створити venv 
```
$ python3 -m virtualenv -- venv
$ source venv/bin/activate
```

### поставити requirements
```
(venv)$ pip install -r requirements.txt
```

### запуск
```
(venv)$ ./courseapp.py
Listening on http://127.0.0.1:5000
```

### test using Pytest:
```
(venv)$ pip install -r test-requirements.txt
(venv)$ pytest
```
