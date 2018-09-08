import psycopg2

# cfg_parser gets initialized in 06_config.py - added next lines for to hide PyCharm error
cp = globals().get('cfg_parser', None)

# conn_args = dict(user='ass_interfaces', password='...', dbname='ass_cache', application_name='ipython_notebooks')
# .. doesn't work (assuming because of ñ character in the pw)
# conn_args = dict(user='postgres', password='...', dbname='ass_cache', application_name='ipython_notebooks')  # works
conn_args = dict(user=cp.get('ae_Options', 'assUser'), password=cp.get('ae_Options', 'assPassword'),
                 dbname='ass_cache', application_name='ipython_notebooks')
# print(conn_args)

# ass_cache at Sihot TEST
conn_args['host'] = 'tf-sh-sihot3v.acumen.es'
ast_conn = psycopg2.connect(**conn_args)
ast_curs = ast_conn.cursor()

# ass_cache at Sihot LIVE
conn_args['host'] = 'tf-sh-sihot1v.acumen.es'
asl_conn = psycopg2.connect(**conn_args)
asl_curs = asl_conn.cursor()

del conn_args
