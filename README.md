# Simple HTTP Server
A toy program written in Python.

## Usage

### for GET request processor
@get decorator binds a URL and a function for processing GET requests for the URL.
You can use wildcards in the URL starts with ':'.

app.py:
```python
from server import get, run

@get('/hello')
def hello(self, query, *args):
    return 'Hello, World'

@get('/hello/:name')
def hello_with_name(self, query, *args):
    return 'Hello, %s' % args[0]

run(host = '', port = 8888)
```

$ python app.py

### using Template
Template#render generats HTML string merged from a template file and a dictionary.
You can embedd python code into the template. The code starts with '%' and ends with '% end'.

hello.tpl:
```html
<body>
  <h1>Hello, {{name}}</h1>
</body>
```

hello3.tpl:
```html
<body>
% for i in range(0, 3):
  <h1>Hello, {{name}}</h1>
% end
</body>
```

app.py:
```python
from server import get, run
from Template import Template

@get('/hello/:name')
def hello_by_template(self, query, *args):
    return Template.render('hello.tpl', {"name": args[0]})

@get('/hello3/:name')
def hello_3_times(self, query, *args):
    return Template.render('hello3.tpl', {"name": args[0]})
```

$ python app.py:

