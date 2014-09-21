class Hello:
    def say(self, name = 'World'):
        data = ''
        with open('hello.tpl') as f:
            data = f.read()
            data = data.replace('${name}', name)
        return data
