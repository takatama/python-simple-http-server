class Hello:
  def say(self, query):
    names = query.get('name', ['World'])
    return 'Hello %s' % ','.join(names)

