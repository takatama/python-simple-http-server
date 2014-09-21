class Template:
    @staticmethod
    def render(file_name, model = {}):
        import re
        source = ["buf = []\n"]
        with open(file_name) as f:
            data = f.read()
        for line in data.split('\n'):  
            while True:
                m = re.search(r'\{\{(\w+)\}\}', line)
                if not bool(m):
                    break
                source.append("buf.append('%s')\n" % line[:m.start()])
                source.append("buf.append(%s)\n" % m.group(1))
                line = line[m.end():]
            if len(line) > 0:
                source.append("buf.append('%s\\n')\n" % line)
        source.append("buf = ''.join(buf)")
        code = compile(''.join(source), '<string>', 'exec')
        exec code in model
        return model['buf']
