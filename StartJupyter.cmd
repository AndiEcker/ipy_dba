REM start jupyter server on Windows machine with Anaconda (installed without extending PATH env variable)

REM change current working directory to dba-notebooks folder
c:
cd \src\python\ipy_dba

REM temporarilly extend PATH (with SETLOCAL only for this batch file) to Oracle 64bit client and Anaconda (instead of running directly C:\ProgramData\Anaconda3\Scripts\jupyter-notebook)
setlocal
set PATH=C:\app\aecker64bit\product\11.2.0\client_1\BIN;C:\ProgramData\Anaconda3;C:\ProgramData\Anaconda3\Library\mingw-w64\bin;C:\ProgramData\Anaconda3\Library\usr\bin;C:\ProgramData\Anaconda3\Library\bin;C:\ProgramData\Anaconda3\Scripts;%PATH%
REM echo %PATH%

REM finally start jupyter server
jupyter notebook
