# Savant Challenge

This project was developed in order to give solution to the technical test that consists of making a crud and login using jwt for user authentication and protecting routing.

**Note:** To access the user API it is only necessary to have an active user,

## How to start?🚀

_These instructions will allow you to get a copy of the project up and running on your local machine for development and testing purposes._

### Installation 🔧

First we must clone the repository, access the folder and then create a virtual environment to install all the necessary libraries.

```
git clone https://github.com/jsdnlb/savant-challenge.git
cd savant-challenge
python3 -m venv venv # Create virtual environment
source venv/bin/activate # Activate environment, may vary in other os
```

Once the environment is active we can install requirements

```
pip install -r requirements.txt
```
Create the .env file and include a secret key in SECRET
```
cp .env.local .env
```
The file should look something like this
```
SECRET=my-secret-key
```
With this we would have everything necessary to run the project and see the magic.

```
uvicorn main:app --reload
```

![image](https://github.com/jsdnlb/savant-challenge/assets/17171887/4121e4e7-0e33-43ac-b9b9-1b09bdd4506d)

## Running endpoints 🔐

Just enter the documentation [Swagger](http://localhost:8000/docs#/)  to start using it, I already included the database so you don't have to make any additional adjustments and it is easier to run it, below I share the test credentials.

```
username: test
password: secret
```

## Running tests ⚙️

To run a all tests section

```
pytest
```

![image](https://github.com/jsdnlb/savant-challenge/assets/17171887/89242e1b-8a87-411d-8b03-a349b161518a)

## Built with 🛠️

_This project was built with the following tools_

* [Python](https://www.python.org/) - Programming language
* [FastAPI](https://fastapi.tiangolo.com/) - Framework
* [SQLite](https://www.sqlite.org/) - Database
* [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM

## Wiki 📖

Once you have the project running you can run it in a simple way here: [Swagger](http://localhost:8000/docs#/) and find the documentation in a more visual way here [OpenAPI](http://localhost:8000/redoc) , although in theory both have the same information.

## Things to improve 🌟

* Include roles
* Add creation and update date
* Add SonarQube
* Add more and improve test cases
* Add Makefile
* Dockerize

## Developer by ✒️

* **Daniel Buitrago** - Documentation and programming - [jsdnlb](https://github.com/jsdnlb)

---
