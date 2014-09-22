import sqlite3


def get_connection(db_flie):
    connection = sqlite3.connect(db_flie)
    connection.text_factory = str
    return connection

class RepositoryException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors

class Repository:
    def __init__(self, db_file, table_name):
        try:
            self.connection = get_connection(db_file)
        except Exception as e:
            raise RepositoryException(*e.args, **e.kwargs)
        self._complete = False
        self._table_name = table_name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def complete(self):
        self._complete = True

    def close(self):
        if self.connection:
            try:
                if self._complete:
                    self.connection.commit()
                else:
                    self.connection.rollback()
            except Exception as e:
                raise RepositoryException(*e.args)
            finally:
                try:
                    self.connection.close()
                except Exception as e:
                    raise RepositoryException(*e.args)

    def questions(self, i):
        return '?' if i < 2 else '?' + ',?' * (i - 1)

    def save(self, domain_object):
        try:
            slots = list(domain_object.__slots__)
            slots.remove('id') #special column
            slots.remove('created_at') #special column
            cursor = self.connection.cursor()
            sql = 'INSERT INTO %s(%s) values (%s)' % (self._table_name, ','.join(slots),  self.questions(len(slots)))
            data = [getattr(domain_object, attr) for attr in slots]
            cursor.execute(sql, tuple(data))
        except Exception as e:
            raise RepositoryException(e)
        return self

    def find_all(self):
        try:
            cursor = self.connection.cursor()
            tuples = cursor.execute('SELECT * FROM %s' % self._table_name, ()).fetchall()
            return tuples
        except Exception as e:
            raise RepositoryException(e)

    def find_one(self, id):
        try:
            cursor = self.connection.cursor()
            tuples = cursor.execute('SELECT * FROM %s WHERE id = ?' % self._table_name, (id,)).fetchone()
            return tuples
        except Exception as e:
            raise RepositoryException(e)

    def delete(self, domain_object):
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM %s WHERE id = ?' % self._table_name, (domain_object.id,))
        except Exception as e:
            raise RepositoryException(e)
        return self