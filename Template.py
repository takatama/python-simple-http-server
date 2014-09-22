class Template:
    @staticmethod
    def render(file_name, model = {}):
        import re
        source = ['buf = []\n']
        with open(file_name) as f:
            data = f.read()
        indent = ''
        for line in data.split('\n'):  
            command_index = line.find('%')
            if command_index >= 0:
                if line.find('end') >= 0:
                    indent = indent[4:]
                else:
                    source.append(indent + line[command_index + 1:].lstrip() + '\n')
                    indent += '    '
                continue
            while True:
                m = re.search(r'\{\{(\S+)\}\}', line)
                if not bool(m):
                    break
                source.append(indent + "buf.append('%s')\n" % line[:m.start()])
                source.append(indent + "buf.append(%s)\n" % m.group(1))
                line = line[m.end():]
            if len(line) > 0:
                source.append(indent + "buf.append('%s\\n')\n" % line)
        source.append("buf = ''.join(buf)")
        code = compile(''.join(source), '<string>', 'exec')
        exec code in model
        return model['buf']
