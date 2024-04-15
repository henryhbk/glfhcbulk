## Bulk Update Tool for GLFHC Athena Health
Author: Henry Feldman, MD

This tool is designed to provide bulk updates to a cohort of records (say patients) where you establish a set of records (via a list of their primary key from some criteria based search) and then do some bulk update of the records. 

### Tech Stack
The project is a python Flask application. Flask is a app framework, similar to Django except without being a full stack, so this provides less automation but much greater simplicity as Django handles many tasks a little too magically.

Flask is a standard python package available in most python IDEs via pip (python's package manager). This project requires at least python 3.9 or later. THe IDE used in the project in JetBrain's PyCharm (pro edition) which is a very commonly used commercial enterprise IDE.

Since from a security standpoint independent user management is a high-risk the application uses SAML to grab the user's identity from active Directory allowing the usual GLFHC SSO to handle authentication. Within athena of course the usual user privs handle what you can and cannot do.

In addition to Flask, the application uses local instance of sqllite to store data within the appliction. This is not the "real" database where athena stores data or lookups are performed, but this is where the application stores local data, such as saved searches, etc rather than having a collection of unmanaged csv files on disk which could run into concurrency problems or become a security risk.

Deployment is intended to be containerized to make the application OS indepdendent on the deploy environment this also allows us to run in a fail-safe mode where if the container goes down it auto-spawns and can be used in a clustered envoronment via kubernetes or the like.
