import IPython

# noinspection PyUnresolvedReferences
get_ipython().run_line_magic("logstart", "-o -r -t " + IPython.paths.locate_profile() + "\\ipython_log.log global")
