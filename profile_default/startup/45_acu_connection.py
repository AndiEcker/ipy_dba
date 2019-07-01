# %load_ext sql -- NOT WORKING BECAUSE %sql CONNECTION IS ONLY A STRING
import datetime
import cx_Oracle
import ipywidgets

# cfg_parser gets initialized in 06_config.py - added next lines for to hide PyCharm error
cp = globals().get('cfg_parser', None)
conn_args = dict(user=cp.get('ae_Options', 'acuUser'), password=cp.get('ae_Options', 'acuPassword'),
                 encoding="UTF-8", nencoding="UTF-8")

acu_opt = list()
acu_conn = acu_curs = None

# acu_live
try:
    conn_args['dsn'] = 'SP.WORLD'
    acl_conn = acu_conn = cx_Oracle.connect(**conn_args)
    acl_curs = acu_curs = acl_conn.cursor()
    acu_opt.append('LIVE')
except Exception as ex:
    print("error in connecting to SP.WORLD", ex)

# acu_dev
try:
    conn_args['dsn'] = cx_Oracle.makedsn(host='tf-sh-ora3.acumen.es', port=1521, sid='spdev')
    acd_conn = acu_conn = cx_Oracle.connect(**conn_args)
    acd_curs = acu_curs = acd_conn.cursor()
    acu_opt.append('DEV')
except Exception as ex:
    print("error in connecting to DEV", ex)

# acu_test
try:
    conn_args['dsn'] = 'SP.TEST'
    act_conn = acu_conn = cx_Oracle.connect(**conn_args)
    act_curs = acu_curs = act_conn.cursor()
    acu_opt.append('TEST')
except Exception as ex:
    print("error in connecting to SP.TEST", ex)

del conn_args

acu_conn_selector = ipywidgets.ToggleButtons(description='Acumen', options=acu_opt)


def acu_conn_choice(choice):
    global acu_conn, acu_curs
    acu_conn, acu_curs = (acl_conn, acl_curs) if choice == 'LIVE' \
        else ((act_conn, act_curs) if choice == 'TEST'
              else (acd_conn, acd_curs))
    return acu_conn


def acu_conn_select():
    ipywidgets.interact(acu_conn_choice, choice=acu_conn_selector)
    return "Selected Acumen database instance: " + acu_conn_selector.value + " (" + str(acu_conn) + ")"


# the following helper methods got borrowed from ae_db.py
def prepare_ref_param(value=None):
    if isinstance(value, datetime.datetime):  # also True if value is datetime.date because inherits from datetime
        ora_type = cx_Oracle.DATETIME
    elif isinstance(value, int) or isinstance(value, float):
        ora_type = cx_Oracle.NUMBER
    else:
        ora_type = cx_Oracle.STRING
        value = str(value)
    ref_var = acu_curs.var(ora_type)
    if value is not None:
        ref_var.setvalue(0, value)
    return ref_var
