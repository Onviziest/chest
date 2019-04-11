from os.path import (
    join as join_path,
    dirname,
)

path_base = join_path(dirname(dirname(__file__)))

path_db = join_path(path_base, 'app.db')

db = 'sqlite:///{}'.format(path_db)

path_misc = join_path(path_base, 'misc')
