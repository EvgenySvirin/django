
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
