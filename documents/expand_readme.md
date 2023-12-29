
## Application description

This application allows the user to vote for answer options in some polls and see the results. In addition, the application can provide comments on answers and enter separate statistics. Administration occurs through the Django shell or admin panel.

## Endpoints and additional functionality
Polls: Poll options
Details: selected survey with answer options
Results: Response to user selection

Additional functionality: programmer may colllect stats on some choices.

## Install requrements

From root:
```
pip install -r requirements.txt
```
#Main api
Go to django folder

## Run django
From root:
```
python manage.py runserver
```


## Run formatter and linter
From root:
```
pre-commit run --all-files
```

## Run module tests
From root:
```
python manage.py test polls
```

## Run integration tests
```
python manage.py test polls.integral_tests
```


#Microservices:
## Run recommendation microservice
```
go to microservice1/mysite

python manage.py runserver 8080
```

## Run paymeny microservice
```
go to microservice2/mysite

python manage.py runserver 8090

```

## Run recommendation microservice test
```
go to microservice1/mysite

python manage.py test recos.tests
```

## Run payment microservice test
```
go to microservice2/mysite

python manage.py test payment.tests
```
