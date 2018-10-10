import IPython

# noinspection PyUnresolvedReferences
get_ipython().run_line_magic("logstart", "-o -r -t " + IPython.paths.locate_profile() + "\\log\\ipython_log.log global")
# noinspection PyUnresolvedReferences
get_ipython().run_line_magic("logstate", "")
