import os
import shutil
import datetime
import glob
import pandas as pd
import numpy as np


def new_file_name(in_file_name, time_stamp=None, new_ext=None):
    fnam, ext = os.path.splitext(in_file_name)
    if time_stamp:
        fnam += time_stamp.strftime('_%Y%m%d_%H%M%S')
    if new_ext:
        ext = new_ext
    return fnam + ext
    

xl_import_root_path = '//acumen.es/files/Logfiles/'
processed_folder_name = 'Processed'
summary_sheet_name_prefix = 'Summary'

SUM_SHEET_HEADER_ROW = 0
SUM_SHEET_IN_RECS_ROW = 2
SUM_SHEET_SEP_ROWS = 3


def xl_init_env(nb_name, in_sheet_skip_rows=1, in_sheet_header=0, in_sheet_use_cols=None, db_name=None):
    # prevent shortening of long columns
    pd.set_option('display.max_colwidth', -1)
    # set environment variables (all locals() that will be returned to caller)
    startup_time = datetime.datetime.now()
    in_folder = os.path.join(xl_import_root_path, nb_name)
    in_file_names = glob.glob(in_folder + '/*.xls*')
    in_file_name = os.path.basename(in_file_names[0]) if in_file_names else ''
    in_file_path = os.path.join(in_folder, in_file_name)
    # print("Selected {} from unprocessed files: {}".format(in_file_path, in_file_names))
    xl_reader = pd.ExcelFile(in_file_path)
    in_sheet_names = xl_reader.sheet_names
    in_sheets = {sn: pd.read_excel(in_file_path, sheet_name=sn, skiprows=in_sheet_skip_rows,
                                   in_sheet_header=in_sheet_header, usecols=in_sheet_use_cols)
                 for sn in in_sheet_names}
    in_record_count = sum(len(sd) for sd in in_sheets.values())
    in_records = pd.concat([sd for sd in in_sheets.values()], ignore_index=True, verify_integrity=True)
    out_file_name = new_file_name(in_file_name, time_stamp=startup_time)
    out_file_path = os.path.join(in_folder, processed_folder_name, out_file_name)
    xl_writer = pd.ExcelWriter(out_file_path)
    sum_sheet_name = summary_sheet_name_prefix + '_' + processed_folder_name
    # need to create the sheet before writing the in_sheet_header
    xl_add_sheet_from_df(xl_writer, in_records, sum_sheet_name,
                         title=nb_name + 
                         (" - Number of converted sales inventory: {}, number of previous/new owners: {}/{}"
                          .format(len(in_records), len(in_records['PREVIOUS OWNER'].value_counts()),
                                  len(in_records['NEW OWNER'].value_counts()))
                          if nb_name == 'AptWeeksMove' else " - {} affected data records".format(len(in_records))),
                         first_row_df=SUM_SHEET_IN_RECS_ROW, first_row_title=SUM_SHEET_HEADER_ROW)
    nb_out_file_name = os.path.join(in_folder, processed_folder_name,
                                    new_file_name(in_file_name, time_stamp=startup_time, new_ext='.ipynb'))
    # finally write the env vars to the output Excel file and return them to caller
    sum_sheet_next_row = SUM_SHEET_IN_RECS_ROW + in_record_count + SUM_SHEET_SEP_ROWS
    # pd.DataFrame([(k, v) for k, v in locals().items()]).to_excel(xl_writer, sheet_name=sum_sheet_name,
    #                                                              startrow=sum_sheet_next_row)
    xl_add_sheet_from_df(xl_writer, pd.DataFrame([(k, v) for k, v in locals().items()]), sum_sheet_name,
                         first_row_df=sum_sheet_next_row, first_col=9)
    sum_sheet_next_row += len(locals()) + SUM_SHEET_SEP_ROWS
    return locals()


def xl_exit_env(env, move_in_file=None):
    if move_in_file is None and 'acu_conn' in globals() and 'acl_conn' in globals():
        move_in_file = globals().get('acu_conn') == globals().get('acl_conn')
    if 'out_records' in env:
        out_rec_count = len(env['out_records'])
        # env['sum_sheet'].write_string(env['sum_sheet_next_row'], 0, "Output data ({} records):".format(out_rec_count))
        # env['sum_sheet_next_row'] += 1
        # env['out_records'].to_excel(env['xl_writer'], sheet_name=env['sum_sheet_name'], index=False,
        #                             startrow=env['sum_sheet_next_row'])
        # env['sum_sheet_next_row'] += out_rec_count + SUM_SHEET_SEP_ROWS
        xl_add_sheet_from_df(env['xl_writer'], env['out_records'], env['sum_sheet_name'], 
                             title="Output data ({} records):".format(out_rec_count), 
                             first_row_df=env['sum_sheet_next_row'] + 1, first_row_title=env['sum_sheet_next_row'])
        env['sum_sheet_next_row'] += 1 + out_rec_count + SUM_SHEET_SEP_ROWS
    env['xl_writer'].save()
    if move_in_file:
        # os.rename(env['in_file_path'], os.path.join(env['in_folder'], processed_folder_name, env['in_file_name']))
        shutil.move(env['in_file_path'], os.path.join(env['in_folder'], processed_folder_name))

 
def xl_add_sheet_from_df(xl_writer, df, name, title="", first_row_df=3, first_row_title=0, first_col=0):
    df.to_excel(xl_writer, sheet_name=name, index=False, startrow=first_row_df, startcol=first_col)
    worksheet = xl_writer.sheets[name]
    if title:
        worksheet.write_string(first_row_title, first_col, title)       # put optional title
    for idx, col in enumerate(df):                                      # loop through all columns
        series = df[col]
        mil: int = np.nan_to_num(series.astype(str).map(len).max())     # len of largest item
        mcl = len(str(series.name))                                     # len of column name/header
        max_len = max(mil, mcl) + 3                                     # adding a little extra space
        # print("xl_add_sheet_from_df() debug: val_max={}, header_max={}, max_len={}"
        #       .format(series.astype(str).map(len).max(), len(str(series.name)), max_len))
        worksheet.set_column(first_col + idx, first_col + idx, max_len)             # set column width
    return df


def xl_add_sheet_from_sql(env, sql, name, title, bind_vars=None):
    df = pd.read_sql_query(sql, con=globals().get('acu_conn'), params=bind_vars)
    return xl_add_sheet_from_df(env['xl_writer'], df, name, title=title)
