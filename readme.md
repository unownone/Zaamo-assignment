# Youtube Live Scrapper

### DRF , APScheduler , Postgres

This project aims to cache the data from youtube live channels and send it to the frontend.

# URLS

## `search/`

- `GET`: Search for a channels channel
  Parameters:

  - `query`: The query to search for

    - If not passed/no value is provided , it will return all the videos Paginated.
    - If a value is provided , if it is a video id, video will be returned or if a search term is provided , all the videos matching the search term will be returned.

    Eg: A video with title `How to make tea?` should match for the search query `tea how`

  - `page` : The page to search for
  - `per_page` : The amount of results per page

# Getting Started

- Run docker-compose to orchestrate the containers.

        `docker-compose up --build`

  App should be running on LocalHost:8000.

- MakeMigrations, open web container , and run:

                `python manage.py makemigrations`
                `python manage.py migrate`

- Create a SuperUser first:

            `python manage.py createsuperuser`
            - Provide the details.

- Go to admin panel at `localhost:8000/admin`

- Create a API_KEY : Add a api_key

- Create a query: Add any query to query about videos.

- Let it run.

This project was made with:

- Postgres
- Django
- Django Rest Framework
- APScheduler
- Python-youtube
- Docker
- docker-compose

Defining Multiple API KEYS will help you avoid letting the server go cold.
