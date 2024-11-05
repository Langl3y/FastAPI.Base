<p align="center" width="100%">
    <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png">
    <p style="text-align: center;">
</p>

# FastAPI - Task Management (Customore Case Study #1)

<span style="color:red;font-weight:700;font-size:50px">
    Tested on Windows
</span>

## Requirements
- Python 3.10
- FastAPI 1.104.1
- MySQL >= 5.8
- Uvicorn 0.20.0
- SQLAlchemy 2.0.23
- pydantic 2.5.2

## Setup PostgreSQL
```shell
psql -U postgres
```

```postgresql
CREATE DATABASE <your_database> OWNER <your_username>;
GRANT ALL PRIVILEGES ON DATABASE <your_database> TO <your_username>;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO <your_username>;
```

## Initialize the project and migrate schemas
```shell
conda create --name <env-name> python=3.10
conda activate <env-name>
```

```shell
./init.sh
```
`** Please configure your DB metadata in the .env file after the process for the project to run` 

## Run server for testing
```shell
uvicorn main:app
```
Or with --reload:
```shell
uvicorn main:app --reload    
```


## Serve the webapp globally (or to nginx)
```shell
 uvicorn main:app --host 0.0.0.0 --port <your_desired_port> --reload
```

## Docker
#### Containerize
```shell
docker build -t task-management .
```

#### Docker run
```shell
docker run -d --name task-management -p 8000:8000 task-management                        
```
`**DB port mapping is not available yet`

## APIs Documentation

See: `<host>`/`docs` in your browser for FastAPI's built-in Swagger documentation.
* Alternatives: api_documentation.md and openapi_schema.json are also included in the project directory.

## Project design and structure
All modules in this project were carefully built with modularity and reusability in mind.

```
task_management/
│
├── api/
│   ├── common/
│   │   ├── __init__.py
│   │   ├── responses.py
│   │   └── utils.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── tasks.py
│   │   └── users.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── tasks.py
│   │   └── users.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── tasks.py
│   │   └── users.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── tasks.py
│       └── users.py
│
├── be/
│   ├── __init__.py
│   ├── env.py
│   └── settings.py
│
├── .gitignore
├── Dockerfile
├── README.md
├── main.py
├── init.sh
├── .env
└── requirements.txt
└── task_management.drawio
```

### Overview
I don't use regular HTTP response codes as they do not provide detailed information on errors and the state of my APIs, 
hence custom API response codes are implemented here in the common directory for better API troubleshooting should they fail 
to operate as intended.

Initially, I would place everything db-related inside a file called `database.py` but seeing the lack of reusability when coding
services, I decided to place them inside `utils.py`. 

Moreover, as this is relatively OOP-heavy I saw no reason to why I should not name all modules of their respective models the same.
In my defense this is a good practice for future maintenance since my design provides consistency across the codebase.

The flow would be something like this:
1. User requests an API
2. The request is routed to its corresponding service through a router
3. The request payload is then serialized into Pydantic model for data validation
4. The service then interacts with DB to perform read/write operation on the specified record
5. The service then returns desired data to its router
6. The router then deserializes returned data and response to User

### Database design

Every model created in this project is equipped with `created_at`, `updated_at` and `is_deleted` fields. The first 2 fields 
will help ensuring data integrity and tracking changes over time while `is_deleted` is used to avoid missing indexes when deleting actual
records in DB.

The design is generated using draw.io: `task_management.drawio`

### The use of dotenv

I use dotenv to manage sensitive data like passwords, access tokens... This practice is a standard that must be enforced 
to ensure a safe and secured back end application.

Also, using a dotenv can help migrating this back end application easier, for instance, if you want to change DB user, DB name,
DB password... then everything will be available in just one file for you to reconfigure.

This project is also equipped with a dotenv sample for used when cloning from git services like GitHub, GitLab...
as .gitignore excludes files that end with .env.

### POST method for all CRUD operations

GET methods' parameters can be bookmarked and cached, so while POST requests take a bit more resources, data can not be stored locally
from client side. Sensitive data like credit card information, user password, etc... can instead be sent through the request body
of POST requests.

I treat every user request as unsafe, so to be able to tackle this problem, POST requests are the only kind of HTTP request
I use for basic CRUD operations (with data uploading operations, however, PUT request would still be used).

## Future integration

A `settings.py` file is present should the need to configure tools like `redis`, `celery`... arises.

## _Room for improvements_
1. [ ] Error handling:
   * can provide more information about where the errors originate from in json responses, not just the errors themselves.
2. [ ] Data validation: 
   * more constraints in Pydantic models to better validate incoming data.
3. [ ] Data filtering:
   * datetime in ISO format can sometimes be too complex for users to query, a filtering mechanism that can also take YY-mm-dd format as input can be helpful in this situation.
4. [ ] Project structure:
    * services can also be split into services and db_managers where services handle business logic and only db_managers can interact with DB.
    * there should be urls.py files to separate API routers from the main file.
5. [ ] Database design:
   * User and Task can have a many-to-many relationship with User having a 'role' field so that a task can also be assigned to different users with different roles.
   * A boolean `is_active` field may be needed for users to control their tasks.
6. [ ] Response data:
   * Also display user data, not just user_id