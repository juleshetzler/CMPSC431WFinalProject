# CMPSC431WFinalProject
Formula 1 database system for CMPSC431W Final Project Deliverable III. This repository contains the SQL schema and data exports for the final project, along with a CLI script for database manipulation and querying.

To recreate database locally:

1. Download a copy of the repository
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository

2. Create a new database to import your SQL file into
createdb -U username dbname

** A quick note about the full_database.sql file: You may have to convert the encoding in Notepad++ to UTF-8-BOM if you get a syntax error when trying to run the psql command in step 3. **

3. Use the psql command to import the full_database.sql into the newly created database
psql -U username -d new_dbname -f full_database.sql

4. Connect to the database
psql -U username -d new_dbname

5. Test database in terminal or pgAdmin4
\dt (to show all tables)






