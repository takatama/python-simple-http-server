from Template import Template

class Hello:
    def say(self, name = 'World'):
        return Template.generate('hello.tpl', {'name': name})
