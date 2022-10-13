To run the Django REST API on your personal machine:

1. Install MySQL and MySQL Workbench
    a. go to https://dev.mysql.com/downloads/installer/
       then click the top download button. Once downloaded, run MySQL installer
    b. click "add" on the right side. In the select products menu, select
       MySQL Servers -> MySQL Server -> MySQL Server 8.0
       and also select:
       Applications -> MySQL Workbench -> MySQL Workbench 8.0 -> MySQL Workbench 8.0.30 - X64
       make sure to add both to the "products to be installed list"
       and then complete the rest of the steps on default settings. 

2. Create new schema
    a. click the create new schema button (looks like a 
       cylinder with a plus sign) and name it "djangodatabase"
    b. double click the "djangodatabase" schema in the left menu, it should become bold
    c. In the "Query 1" tab, paste the following commands:

        create user dbadmin identified by 'password12345';
        grant all on djangodatabase.* to 'dbadmin'@'%';
        flush privileges
    
    d. click the lightning bolt symbol to run the commands

3. Install MySQL client
    a. Assuming you already have python and pip installed, run the commands:
        pip install Django
        pip install djangorestframework
        pip install pymysql
        pip install mysqlclient

4. navigate to /backend/ directory and run: python manage.py migrate
    (this step might not work, message me if it doesn't and I'll give you the fix)

5. Run and test API
    a. in the command line, type: python manage.py runserver 0.0.0.0:8000
        (exclude the 0.0.0.0:8000 if you just want it to run on localhost port 8000)
    b. In your browser, put this link: http://127.0.0.1:8000/argus_test/region/
    c. play around with adding data to database
