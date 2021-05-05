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

## API

При неправильному сформованому запиті HTTP-відповідь має код 400, тіло відповіді має вигляд `{"error": "..."}`. Успішна відповідь має код 200.

Повний запис курсу виглядає як такий JSON:

```
  {
    "coursename": "your course",
    "startdate": "2021-05-01",
    "finishdate": "2021-06-01",
    "numberlectures": 42
  }
```

* `POST /api/course` - Додавання курсу в каталог (create)
  
  Request payload - повний запис курсу:
  ```
  {
    "coursename": "your course",
    "startdate": "2021-05-01",
    "finishdate": "2021-06-01",
    "numberlectures": 42
  }
  ```

  Response:
  ```
  {
    "status": "ok",
    "course_id": 1
  }
  ```
.
  
* `GET /api/course` - Відображення списку курсів (read)

    Response 
    ```
    {
        "status":"ok",
        "courses": [
            # повні записи курсів
        ]
    }
    ```
* `GET /api/course/<id>` - Відображення деталей курсу по id (детальна  сторінка курсу повинна відображати повну інформацію про курс) (read)
    
    Response: повний запис курсу

* `POST /api/course/search` - Пошук курсу за назвою і фільтр по датах (search)
    
    Request: 
    + JSON рядок, який міститься в імені курсу
    + словник параметрів: 
      ```
      {
          "coursename": "...",
          "startafter": "2021-05-05"
      }
      ```

    Response: список повних записів курсів, які відповідають параметрам пошуку

* `PATCH /api/course/<id>` - Зміна атрибутів курсу (update)

    Request: словник з довільним набором ключів `coursename`, `startdate`, `finishdate`, `numberlectures`.

    Response: повний оновлений запис курсу

* `DELETE /api/course/<id>` - Видалення курсу (delete)
