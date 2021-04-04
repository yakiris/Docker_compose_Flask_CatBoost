# python-flask-docker  
Итоговый проект (пример) курса "Машинное обучение в бизнесе"  

Стек:  

ML: catboost, pandas, numpy  
API: flask  
Данные: с kaggle - https://www.kaggle.com/arashnic/hr-analytics-job-change-of-data-scientists  

Задача: предсказать по анкетным данным верояность заинтересованности кандидатов на вакансию Data Scientists.  

Бинарная классификация.  
target: 0(не заинтересован), 1(заинтересован)  

Используемые признаки:  

- gender (object) - пол кандидата  
- relvent_experience (object) - релевантный опыт в годах  
- enrolled_university (object) - тип зачисленных университетских курсов, если таковые имеются   
- education_level (object) - уровень образования  
- major_discipline (object) - основная дисциплина  
- experience (object)- общий стаж в годах  
- company_size (object) - количество сотрудников в компании текущего работодателя  
- company_type (object) - тип текущего работодателя  
- last_new_job (object) - разница в годах между предыдущей работой и текущей работой  

Модель: CatBoostClassifier  

### Клонируем репозиторий и создаем образ  
```
$ git clone https://github.com/fimochka-sudo/GB_docker_flask_example.git  
$ cd Docker_compose_Flask_CatBoost  
$ docker-compose build  
```
### Запускаем контейнер
```
docker-compose up
```

### Web-service
Переходим на localhost:8181

### REST API
Postman.
POST: 0.0.0.0:8180/predict
Key: Content-Type, Value: application/json
Body:
{
    "gender": "Male",
    "relevent_experience": "Has relevent experience",
    "enrolled_university": "Full time course",
    "education_level": "Graduate",
    "major_discipline": "Humanities",
    "experience": ">15",
    "company_size": "<100",
    "company_type": "Pvt Ltd",
    "last_new_job": "never"
}