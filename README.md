MySQL Shell DBA Toolkit
=======================

This is toolkit with several Python module for MySQL Shell to make
MySQL DBA's life easier ;)

How to use it:
--------------

```
 mysqlsh --py root@localhost

 import sys
 sys.path.append('/home/fred/workspace/mysql-shell-mydba')
 import mydba

 innotop.session_processlist.run()
``` 

It's also possible to add some steps in *~/.mysqlsh/mysqlshrc.py*:

```
 import sys
 sys.path.append('/home/fred/workspace/mysql-shell-mydba')
 import mydba
```

and then in the Shell, just call _mydba.<and the name of the function>()_ 

Current Functionalities:
------------------------

* **getProcedures() :** *list all routines (functions and/or procedures) for a specified schema*
* **deleteProcedures() :** *delete all routines for a specified schema*
* **getPasswordExpiration() :** *list the account that have a password that will expire (and expired)*
* **getFragmentedTables() :** *list the tables that are potentially fragmented (more than <10%> free)*
* **getDefaults() :** *list all fields (column) for a table and evaluate and example for default value*

Example:
--------

```
 MySQL   127.0.0.1:33060+  Py  mydba.getProcedures('test')
PROCEDURE `test`.`helloworld`
Total: 1

 MySQL   127.0.0.1:33060+  Py  mydba.deleteProcedures('test')
DROP PROCEDURE `test`.`helloworld`
Total dropped: 1
```
