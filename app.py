from server import get, run
from Hello import Hello

@get('/hello')
def say(self, query, *args):
    hello = Hello()
    name = query.get('name');
    if name is None:
        return hello.say()
    return hello.say(', '.join(name))

@get('/greeting/:name')
def greeting(self, query, *args):
    hello = Hello()
    return hello.say(args[0])

run(host = '', port = 8888)
