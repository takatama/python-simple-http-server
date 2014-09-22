from server import get, post, run
from Template import Template
from Repository import Repository, RepositoryException


class Comment(object):
    __slots__ = ['id', 'comment', 'created_at']

    def __init__(self, id, comment, created_at):
        self.id = id
        self.comment = comment
        self.created_at = created_at


db_file = 'comments.db'
table_name = 'comments'

@post('/comments')
def create_comment(self, data, *args):
    comment = ','.join(data["comment"])
    with Repository(db_file, table_name) as repository:
        repository.save(Comment(None, comment, None)).complete()
    return 'redirect:/comments'

@get('/comments')
def list_comments(self, query, *args):
    with Repository(db_file, table_name) as repository:
        comments_tuple = repository.find_all()
        comments = [Comment(item[0], item[1], item[2]) for item in comments_tuple]
    return Template.render('comments.tpl', {"comments": comments})

run(host = '', port = 8888)
