README:

Files present in p8 directory:

1. blood_donation.db
2. create_db.sql
3. drop_tables.sql
4. populate_db.sql
5. README.txt
6. final.py


How to setup the database:

1. Enter the p8 folder on your terminal.

2. Run the following commands in the same order - 

	a. sqlite3 blood_donation.db
	b. .read drop_tables.sql
	c. .read create_db.sql
	d. .read populate_db.sql
	e. .exit
	f. python3 final.py


Database and data:
The database and data I have chosen to work with are related to blood donation data. This includes data like the donor name, the donation ID, the blood type of the donation etc.


Tables used and their attributes:

1. Donors (Relation X) - Donor ID, Name, Blood Type, Blood ID, Contact Information

The schema for this is given below - 
Donors(
   donor_id INT PRIMARY KEY     NOT NULL,
   name           VARCHAR(50)   NOT NULL,
   blood_type     VARCHAR(50)   NOT NULL,
   blood_id       INT           NOT NULL,
   contact_info   VARCHAR(50)
)

2. Donate (Relation Y) - Donation ID, Donor ID, Blood ID, Drive ID

The schema for this is given below - 
Donate(
  donation_id INT PRIMARY KEY     NOT NULL,
  donor_id    INT                 NOT NULL,
  blood_id    INT                 NOT NULL,
  drive_id    INT                 NOT NULL,
  FOREIGN KEY(donor_id) REFERENCES Donors(donor_id),
  FOREIGN KEY(drive_id) REFERENCES Drives(drive_id)
)

Since the data has been randomly generated and the amount of data was 20, it may seem like there is a one-to-one relationship between Donors and Donate, however, this is NOT the case. If you play around with different inserts into either table and linking between entries in Donors and Donate, this will be clear to you.

Data Constraints:

1. None of the entries in either table are allowed to be null/empty with the exception of one attribute in the table Donors - Contact Information (contact_info).

2. Blood types are restricted to the following types - O positive, O negative, A positive, A negative, B positive, B negative, AB positive, AB negative. These ARE case sensitive.

(All forms on the website are subject to these data constraints meaning that if any field other than contact information is left empty, the error is caught and a message is displayed. Additionally, if any entry for the blood type is not in the accepted list, an appropriate error message will be displayed. Furthermore, error handling accounts for ensuring no collisions of primary keys/ foreign keys in the insertion/updating/linkage functionality.)


Website:

Main Page (Landing Page) - http://localhost:8080/
This page contains the information on the Donors table. It displays all entries in the Donors table. There is a search form that can be used to search through the Donors table. Two attributes in the Donors table can be searched through - 
1. Donor Name - This is a regular search which search for an entry containing the string specified.
2. Blood Type - This is a wildcard search meaning the user has the flexibility to include wildcard characters in the search to perform a more robust and flexible form of pattern matching e.g using A% will return all entries whose blood type starts with an A i.e A positive, A negative, AB positive and AB negative. This is indicated with an asterisk (*).

The search is conjunctive, each search attribute can be used individually and if no attribute is specified, the results will be the first 20 results in the Donors table. If no matches are found, the results, as expected is an empty table.


At the top of this search page, you are able to click on a link which will lead to another page. This page will provide you with a form, through which, you are able to insert records into the Donors table. This is subject to the data constraints.


For each record in the search result we are able to go to the following pages - 
1. View/Update page which allows you to view that specific record that you clicked on and update values (subject to the constraint that primary and foreign keys cannot be updated, furthermore, blood id cannot be updated since this seemed like a logical constraint that has been added).

2. Delete - Delete the specific record in Donors.

3. Display Donate - This shows all the records in the table Donate associated with the chosen record in the table Donors.

4. Add record to Donate - This allows you to add new records to the Donate table (through the form at the top of the page) which will be linked with the record chosen in the Donors table. In the table shown below the insertion form, you are able to view all the records in the Donate table and update an existing record by linking that record to the record chosen in the Donors table. These changes can be view in the Donate table.


Changes on the Donors table can be seen by going back to the landing page (which a link for is provided).


Each page has a link provided that allows you to return home to the landing page. If changes/modifications are made to the Donate table as well, there is a link on these pages provided to view the donate table to view changes made such as updates, linking and inserting.


Enjoy!


