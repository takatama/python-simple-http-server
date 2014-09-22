from server import get, post, run
from Hello import Hello
from Template import Template

@get('/hello')
def say(self, query, *args):
    hello = Hello()
    name = query.get('name');
    if name is None:
        return hello.say()
    return hello.say(', '.join(name))

@get('/hello/:name')
def hello(self, query, *args):
    return Template.render('hello.tpl', {"name": args[0]})

@get('/greeting/:name')
def greeting(self, query, *args):
    hello = Hello()
    return hello.say(args[0])

@post('/comments')
def comment(self, data, *args):
    print data
    return ''

run(host = '', port = 8888)
