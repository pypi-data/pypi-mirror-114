# Notelist
Notelist is a tag based note taking REST API that can be used to manage
notebooks, tags and notes. Notelist is written in Python and is based on the
Flask framework.

#### Project information:
- Version: 0.3.0
- Author: Jose A. Jimenez (jajimenezcarm@gmail.com)
- License: MIT License
- Repository: https://github.com/jajimenez/notelist

## How to install

It's recommended to install Notelist in a Python **virtual environment**. To
create a virtual environment and activate it (in Linux or Mac OS), you can use
the `venv` Python module and the `source` command:

```bash
python -m venv env
source env/bin/activate
```

Then Notelist can be downloaded from the **PyPI** repository and installed with
**PIP**:

```bash
pip install notelist
```

Alternatively, you can generate the **built package** or the **source archive**
from the source code and install any of them. To generate and install the
**built package** (preferred):

```bash
pip install wheel
python setup.py bdist_wheel
pip install ./dist/notelist*.whl
```

To generate and install the **source archive**:

```bash
python setup.py sdist
pip install ./dist/notelist*.tar.gz
```

## How to run

To run Notelist, we need first to set the following **environment variables**:

- `FLASK_APP`:<br>
Its value must be always the Notelist package name: `notelist`.

- `NOTELIST_SECRET_KEY`:<br>
The Secret Key is used for storing session information specific to a user from
one request to the next. Its value must be a **random** sequence of characters
and must be kept **secret**.

- `NOTELIST_DB_URI`:<br>
Database connection string. Only **PostgreSQL** and **SQLite** are supported.
The format of the connection string is:
  - PostgreSQL: `postgresql://user:password@host:port/db`
  - SQLite: `sqlite:///path_to_database_file`

In addition, you can set the following optional environment variables:
- `NOTELIST_AC_ALLOW_ORIGIN`:<br>
Value of the **Access-Control-Allow-Origin** response header. The value of this
header determines which host is allow to make requests to the API from a front-end
application (from JavaScript code).<br><br>
If this API is used through a front-end application and the API and the front-end
application are in the same host, then it's not needed to set this header. If the
API and the front-end are in different hosts, then the header must be set to the
host of the front-end application (starting with "https://").<br><br>
The value `*` for the header allows a front-end from any host to make requests to
the API but this is not recommended and is not supported by all browsers.

- `NOTELIST_ROOT_DOC`:<br>
If its value is "yes", then the root route (`/`) returns a documentation page.
Otherwise, a 404 error response is returned.

To create the **database tables**:

```bash
flask db upgrade -d $(flask path migrations)
```

To create a **user**:

```bash
flask user create <username> <password> <admin> <enabled> <full-name> <e-mail> 
```

- admin = `0` (default) or `1`
- enabled = `0` (default) or `1` (if value is 0, the user won't be able to log in)
- Example for an administrator user: `flask user create admin somepassword 1 1`

To run Notelist on a **local development** server (**not** for a production
environment) from the Python package installed:

```bash
flask run
```

Alternatively, you can run Notelist on a **local development** server (**not**
for a production environments) from a script in the source code (without
installing the Python package):

```bash
cd src
python run.py
```

To run Notelist in a **production** environment, we need to run it through a
**WSGI** server (e.g. Gunicorn). We can install **Gunicorn** from the
`requirements_pro.txt` file:

```bash
pip install -r requirements_pro.txt
```

Then we can run Notelist through Gunicorn (for instance, with 4 worker processes,
listening to connections from outside our computer on port 5000):

```bash
gunicorn -w 4 -b 0.0.0.0:5000 notelist:app
```

## How to run with Docker

You can run a Docker container with Notelist with the following command. This
command downloads the Docker image from the Docker Hub repository (if the image
doesn't exist locally yet) and runs a container from the image:

```bash
docker container run --name notelist -d -p 5000:5000 -e NOTELIST_SECRET_KEY=<key> -e NOTELIST_DB_URI=<uri> NOTELIST_ROOT_DOC="yes" jajim/notelist:0.3.0
```

Once the container is running, we can create the database tables with this
command:

```bash
docker container exec -it notelist upgrade-db
```

To create an administrator user:

```bash
docker container exec -it notelist create-user <username> <password> <admin> <enabled> <name> <email>
```

- admin: `0` (default) or `1`
- enabled: `0` (default) or `1` (if it's 0, the user won't be able to log in)
- To create an administrator user: `docker container exec -it notelist
create-user admin pw_example 1 1`

## How to run with Docker Compose

We can try Notelist using **Docker Compose** to run a Notelist container and a
PostgreSQL container to store the Notelist data. Run the containers from the
same directory of the `docker-compose.yml` file (the project's root directory):

```bash
docker compose up -d
```

Create the database tables:

```bash
docker container exec -it notelist-api upgrade-db
```

Create an administrator user:

```bash
docker container exec -it notelist-api create-user admin somepassword 1 1
```

## How to run the unit tests

To run all the unit tests, run the following command from the project's root
directory:

```bash
python -m unittest discover test
```

## Documentation

You can find the documentation of all the operations of the API by running the
API with the `NOTELIST_ROOT_DOC` environment variable set to `yes` and navigating
to the root route (`/`) in a browser.

## Request examples

The following are some examples of requests to the Notelist API with the `curl`
command assuming that the API is running in our local computer and listening on
port 5000.

Log in:

```bash
curl -X 'POST' 'http://localhost:5000/auth/login' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"username": "<username>", "password": "<password>"}'
```

Create a notebook:

```bash
curl -X 'POST' 'http://localhost:5000/notebooks/notebook' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <access_token>' \
-d '{"name": "Example Notebook"}'
```

Create a note:

```bash
curl -X 'POST' 'http://localhost:5000/notes/note' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <access_token>' \
-d '{"notebook_id": "<notebook_id>", "title": "Example Note", "body": "This is a test note", tags: ["tag_name_1", "tag_name_2"]}'
```

Get the notes of a notebook by a filter:

```bash
curl -X 'POST' 'http://localhost:5000/notes/notes/<notebook_id>' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <access_token>' \
-d '{"active": true, "tags": ["tag_name_1", "tag_name_2"]}'
```

Search for notebooks, tags and notes that match a given text:

```bash
curl -X 'GET' 'http://localhost:5000/search/&lt;search&gt;' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer &lt;access_token&gt;'
```

Archive a note:

```bash
curl -X 'PUT' 'http://localhost:5000/notes/note/<note_id>' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer &lt;access_token&gt;' \
-d '{"active": false}'
```

Log out:

```bash
curl -X 'GET' 'http://localhost:5000/auth/logout' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <access_token>'
```
