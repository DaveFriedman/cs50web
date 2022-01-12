## Notes: Lecture 3 Django  
Django: A framework to create dynamic web applications, written in Python


## Web Applications
Static websites look exactly the same every time they're viewed.  
Dynamic websites change, based on time, user interaction, etc.. It is much
easier to update a website through a framework than to rewrite static HTML and
CSS files.  
Django runs on a web server, and when clients make a request, Django will return
a dynamic response. 


## HTTP
HTTP is the protocol for how messages are sent back and forth over the internet,
between web clients (browsers, search bots, APIs, etc.) and the web server 
(which contains our Django application).  
A request example:  
```GET / HTTP/1.1```  
```Host: www.example.com```  
```...```  
The client has sent a request to the server. It is a GET request, GET is one
possible method of requests (others: POST, PUT, DELETE, etc.). The ```GET```
request is for the data at ```/```, the root, from the host (www.example.com).
```HTTP/1.1``` is the HTTP version being used.  

The server sends back a response, for example:  
```HTTP/1.1 200 OK```  
```Content-Type: text/html```  
```...```  
Code ```200``` means OK (```500``` means server error), then a description of
the content being sent (```Content-Type: text/html```), then additional
information. The HTTP version being used is also included.  


## Django
Installing Django: ```pip3 install Django```  
Create a django project: ```django-admin startproject PROJECT_NAME```  
Creates a new project in the directory you're in. The project contains some
boilerplate django files.  
```manage.py```: Used to execute commands on the django project  
```settings.py```: Contains config settings for the project, with defaults  
```urls.py```: A table of contents for the webapp. The URLs of the website  
```python manage.py runserver```: run the app, default is http://127.0.0.1:8000
A launch is a django project, may contain 1 or more applications. Many services
(applications) can exist in one project.  

Create a Django app: ```python manage.py startapp hello```, creates a "hello"
folder that contains the "hello" app.  
The "hello" app must be installed in the Django project. Do this by editing
```settings.py``` to include "hello" in the INSTALLED_APPS list.  
The app "hello" now exists in the Django project

## Routes
The most basic route is the index, at ```/```, and requests to it are handled by
a function that represents a view.  

In hello/views.py:
```from django.http import HttpResponse```  
```def index(request):```
&emsp;```return HttpResponse("Hello, world!")```  

To associate the view with a specific url, create a ```urls.py``` file inside
the Hello folder. Inside ```urls.py```,  
first, ```from django.urls import path``` and ``` from . import views```  
then, add ```urlpatterns = [path("", views.index, name="index")]```  
```urlpatterns``` is a list that contains all the url paths of the app.  
```path("", views.index)``` is an item in the list.  
```path()``` takes 3 arguments:  
```""``` is the empty string, and it means there are no additional url
arguments, so, just index.  
```views.index``` is the ```index()``` function written in ```views.py```  
```name="index"``` allows us to give a name to the path   

Finally, in the Django project (not the Hello app), edit the project-level
urls.py file.  
By default, it contains ```urlpatterns = [path('admin/', admin.site.urls)]```.  
Add ```from django.urls import path, include``` and then ```path('hello/',
include("hello.urls"))``` to the urlpatterns list. ```include("hello.urls")```
tells the django project to include all urls from the urls.py file in the Hello
app.   
This creates the url ```http://www.example.com/hello```, which will display the "Hello, world!"
text from ```index()```.  

Parameterized paths:  
in hello/views.py, add a greet() function:  
```def greet(request, name.capitalize()):```  
&emsp;```return HttpResponse(f"Hello, {name}!")```  
in the Hello app urls.py, add to urlpatterns:  
```path("<str:name>", views.greet, name="greet")```  


## Templates
In order to separate a HTML response from it's python logic, use templates.  
Replace a view's return, from ```return HttpRequest("Hello, world!")``` to
```return render(request, "hello/index.html)```. But first, create a templates
folder in the app's dir and add the app name to it, then put the index.html file
in there. The structure should be: /hello/templates/hello/index.html  




## Tasks



## Forms



## Sessions

