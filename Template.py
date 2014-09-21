class Template:
    @staticmethod
    def generate(file_name, model):
        data = ''
        with open('hello.tpl') as f:
            data = f.read()
            for name, value in model.iteritems():
                data = data.replace('${' + name + '}', value)
        return data
