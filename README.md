# BlogNest

BlogNest is an application developed in Python using Django, designed for creating, editing, and publishing posts. The system is built with a decoupled approach, allowing asynchronous content publishing through the use of message queues with Celery.

## technologies

* Python
* Docker
* Celery
* JWT Authentication

## Main functionalities

* Create blog posts
* Edit existing posts
* Publish posts asynchronously
* Communication between applications using message queues
* Preparation for scalability and background processing
* User authentication and role management

## Technical approach

The project was designed following principles of decoupled architecture, where the responsibility for publishing is delegated to an independent process using asynchronous messaging.

* **Django:** Used as the main framework for Model management, business logic and post administration
* **Celery:** Implemented as a queue-based communication mechanism, allowing publication tasks to be sent to an external process responsible for consuming and executing messages.
* **Asynchronous communication:** BlogNest communicates with an external consumer application, which is responsible for processing messages sent by Celery and publishing the post.

