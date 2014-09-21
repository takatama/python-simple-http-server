from Template import Template

class Hello:
    def say(self, name = 'World'):
        return Template.render('hello.tpl', {'name': name})
