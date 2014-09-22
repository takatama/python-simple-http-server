from server import get, post, run
from Template import Template


class Comment:
    def __init__(self, comment_id, comment, created_at):
        self.comment_id = comment_id
        self.comment = comment
        self.created_at = created_at

import sqlite3

db_file = 'comments.db'
insert_sql = 'INSERT INTO comments(comment) values (?)'
select_sql = 'SELECT * FROM comments'

def __execute(query ,parameters):
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        connection.commit()
        fetched_list = cursor.fetchall()
        return fetched_list

@post('/comments')
def create_comment(self, data, *args):
    comment = ','.join(data["comment"])
    __execute(insert_sql, (comment,))
    print "Comment '%s' is created.\n" % comment
    return 'redirect:/comments'

@get('/comments')
def list_comments(self, query, *args):
    comments = [Comment(item[0], item[1], item[2]) for item in __execute(select_sql, ())]
    return Template.render('comments.tpl', {"comments": comments})

run(host = '', port = 8888)
