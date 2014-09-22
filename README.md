# Simple HTTP Server
A toy program written in Python.

## Usage

### for GET/POST request processor
@get/@post decorator binds a URL and a function for processing GET/POST requests for the URL.
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
Template#render generates HTML string merged from a template file and a dictionary.
You can embed python code into the template. The code starts with '%' and ends with '% end'.

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

### BBS example
At first, create comments database file named as comments.db.

$ sqlite3 comments.db
SQLite version 3.7.13 2012-07-17 17:46:21
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite> CREATE TABLE comments(id INTEGER PRIMARY KEY AUTOINCREMENT , comment TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

comments.tpl:
```html
<html>
  <head>
    <title>Comments</title>
  </head>
  <body>
    <ul>
% for comment in comments:
      <li>{{str(comment.comment_id)}} : {{comment.comment}} ({{comment.created_at}})</li>
% end
    </ul>
    <form method="POST" action="/comments">
      <input type="text" name="comment">
      <input type="submit">
    </form>
</html>
```

comments.py:
```python
from server import get, post, run
from Template import Template


class Comment:
    def __init__(self, comment_id, comment, created_at):
        self.comment_id = comment_id
        self.comment = comment
        self.created_at = created_at

import sqlite3

db_file = 'comments.db'
insert_sql = 'INSERT INTO comments(comment) values (?)'
select_sql = 'SELECT * FROM comments'

def __execute(query ,parameters):
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        connection.commit()
        fetched_list = cursor.fetchall()
        return fetched_list

@post('/comments')
def create_comment(self, data, *args):
    comment = ','.join(data["comment"])
    __execute(insert_sql, (comment,))
    print "Comment '%s' is created.\n" % comment
    return 'redirect:/comments'

@get('/comments')
def list_comments(self, query, *args):
    comments = [Comment(item[0], item[1], item[2]) for item in __execute(select_sql, ())]
    return Template.render('comments.tpl', {"comments": comments})

run(host = '', port = 8888)
```
$ python comments.py