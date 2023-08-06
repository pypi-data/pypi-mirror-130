<h2>smModule</h2>
<p>Collection of methods and classes that are very useful and save a lot of time</p>
<p>Please report any errors to pascalvallaster@gmail.com</p>

<h2>Installation</h2>
```
pip install smModule
```

<h3>Description</h3>
<p>This module contains several sections, for example the Logging - Section for writing logs or the DB and SQL - Section. 
Every class and method has its own doc-string containing information about usage, examples, exceptions... . 
You can see the doc-string by hover over the element with your mouse in the editor (eg. PyCharm) or by typing following 
python command:

```
help(sm.<element>)
```
</p>

<h3>Usage</h3>
<p>
For example we would like to execute a SQL-Query in my DB-File:

```
from sm import dbworker


class db(dbworker):
        db_path = "/home/user1234/testDB.db"
        result = []

        def run_sql(self, sqlcom="SELECT Title FROM Books"):
            self.c.execute(sqlcom)
            self.connection.commit()
            for row in self.c.fetchall():
                self.result.append(str(row))

    db_instance = db()
    db_instance.run_sql()
    for element in db_instance.result:
        print(element)
    db_instance.close()
```
</p>

<h3>License</h3>
<p>Copyright by Pascal Vallaster | all rights reserved, OSI Approved; MIT-License</p>

<h3>Development</h3>
<p>Help and fixes welcome! <br>
Tested on the following python versions: 3.6, 3.7, 3.8, 3.9<br>
Tested on the following OS-Systems: Windows 10, Kali Linux, Ubuntu</p>





