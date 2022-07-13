#!/usr/bin/python

# ---------------------------------------
# importing modules
# ---------------------------------------

from curses import curs_set
from ijpypostgresql.Crud_oper import CrudOperations
from ijpypostgresql.ModulePostgreSQLdb import ModulePostgreSQLdb
# from ijpypostgresql.HelperModule import HelperModule
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# the main method of testing app
def run_db_config():

    DATABASE_NAME = 'keeggo_db'
    TABLA_NAME = 'player'
    # import pdb; pdb.set_trace()

    conn_params = config_database_from_file(filename='psql_database_config.db')
    # pgdbo = ModulePostgreSQLdb(db='postgres', user='ijdevpg', pwd='ijdevsd1')
    psql = ModulePostgreSQLdb(conn_params)
    crud = CrudOperations()

    conn, cursor = psql.connect2db()

    crud.read_one(conn, cursor, TABLA_NAME)


    # psql.create_db(cursor, DATABASE_NAME)

    # psql.activate_db(conn, cursor, DATABASE_NAME)

    # psql.create_table_player(cursor, TABLA_NAME)

    TABLA_NAME = 'land_property'
    # psql.create_table_property(cursor, TABLA_NAME)

    psql.close_pg_con(conn, cursor)

    return



def config_database_from_file(**kwarg):
    # import pdb; pdb.set_trace()

    os.chdir('utils')
    filename = kwarg['filename']

    with open(filename, 'r', encoding='utf-8') as file_obj:
        content = file_obj.read()

        conn_data = {}

        conn_content_list = content.split('\n')
        for data_ in conn_content_list:
            content_list = data_.split('=')

            param = content_list[0]
            value = content_list[1]

            conn_data[param] = value

    return conn_data




if __name__=='__main__':
    run_db_config()
