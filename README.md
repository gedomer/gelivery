
## About The Project
> Gelivery. A food ordering backend system.

### Built With
-   Django
-   Django REST Framework
-   Python
-   PostgreSQL

### Prerequisites
-   Docker 20.10.7
-   docker-compose 1.29.2

## Installation

 1. Clone the gelivery ```git clone https://github.com/gedomer/gelivery.git```
 2. Copy example env file in ```"config/"``` into root of project as .env.
 3. Run ```docker-compose up```. After project started, open second terminal and type: ```docker-compose run app python manage.py order_consumer```
 4. Create initial data: ```docker-compose run app python manage.py loaddata fixtures/gelivery.json```
     (You can reset the database with  `docker-compose exec app python manage.py flush`).
 5. Default admin app credentials: "admin:admin"

### Commands

 - To shut down the Docker containers: ```docker-compose down```

### Run tests

 Run ```docker-compose run app python manage.py test```


## Documentations
* [API Endpoints](https://github.com/gedomer/gelivery/blob/main/docs/api.md)


## Release History
* 0.0.1
* Work in progress

## Meta
- gedomer – [@gedomer](https://github.com/gedomer)
- Distributed under the MIT license. See ``LICENSE`` for more information.