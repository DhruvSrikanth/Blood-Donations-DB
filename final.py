from bottle import route, run, template, post, get, request
import sqlite3

# Constants
HOST_NAME = 'localhost'
PORT_NUMBER = 8080
DATABASE_NAME = "blood_donation.db"
TABLE_NAMES = ["Donors", "Donate"]
SEARCH_LIMIT = 20
welcome_message = "Welcome to the Blood Donation Database!"
blood_types = ['O positive', 
               'O negative', 
               'A positive', 
               'A negative', 
               'B positive', 
               'B negative', 
               'AB positive', 
               'AB negative']

# HTML useful constants
break_html = "<br/>"
newline_html = "</tr>"
return_to_landing_page_html = " </br> Return to <a href = \"/\">landing page</a>"
record_deleted_html = "Record Deleted! </br>" + return_to_landing_page_html
record_updated_html = "Record Updated! </br>" + return_to_landing_page_html
record_inserted_linked_html = "Record Inserted and Linked! </br>" + return_to_landing_page_html
record_linked_html = "Record Linked! </br>" + return_to_landing_page_html
record_inserted_html = "Record Inserted! </br>" + return_to_landing_page_html

# Database connection
con = sqlite3.connect(DATABASE_NAME)
cur = con.cursor()

# Functions
@route('/delete/<id>')
def delete(id):
    '''
    Delete record.
    '''
    # Execute commands (cascading)
    for table in TABLE_NAMES:
        cur.execute("DELETE FROM {} WHERE donor_id = {}".format(table, str(id)))
        con.commit()

    # Return home
    html = record_deleted_html

    return html

@post('/update/<id>')
def update(id):
    '''
    Update record.
    '''
    # Error handling flag
    invalid_data_flag = False

    # Create update command
    update_command = "UPDATE {} SET {} = '{}' WHERE donor_id = {};"
    update_commands = []

    # Get data
    donor_name = request.forms.get('name')
    if donor_name != "":
        update_commands.append(update_command.format(TABLE_NAMES[0], 'name', donor_name, id))

    blood_type = request.forms.get('blood_type')
    if blood_type != "":
        if blood_type not in blood_types:
            invalid_data_flag = True
        update_commands.append(update_command.format(TABLE_NAMES[0], 'blood_type', blood_type, id))

    contact_info = request.forms.get('contact_info')
    if contact_info != "":
        update_commands.append(update_command.format(TABLE_NAMES[0], 'contact_info', contact_info, id))

    # Check data
    if len(update_commands) == 0:
        invalid_data_flag = True

    # Error handling
    if not invalid_data_flag:
        # Valid data
        # Execute commands
        print(update_commands)
        for cmd in update_commands:
            cur.execute(cmd)
            con.commit()

        # Return home
        html = record_updated_html
    else:
        # Invalid data
        html = "Invalid data provided! ".format(blood_type) + break_html + break_html
        # Acceptable data
        html += "Valid Blood Types - O positive, O negative, A positive, A negative, B positive, B negative, AB positive, AB negative." + break_html + break_html
        html += "All Fields Must Contain Non-Empty/Non-Null Value. Donation ID Must Be Unique." + break_html + break_html

        # Return home
        html += return_to_landing_page_html

    return html

@route('/view/<id>')
def view(id):
    '''
    View record.
    '''
    # Create view command
    view_command = "SELECT * FROM {} WHERE donor_id = {}".format(TABLE_NAMES[0], str(id))

    # View record message
    view_record_message = "Record Request:"
    html = "<h3> {} </h3> <br/> <table>".format(view_record_message)

    # Display table
    display_columns = True
    for row in cur.execute(view_command):
        html += "<tr>"
        if display_columns:
            column_names = ['Donor ID', 'Name', 'Blood Type', 'Blood ID', 'Contact Information']
            for column in column_names:
                html += "<td>" + str(column) + "</td>"
            html += newline_html
            display_columns = False
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
    html += "</table>"

    # Update form
    html += '''
        <form action = "/update/{}" method = "post">
            Donor Name: <input name = "name" type="text" />
            Blood Type: <input name = "blood_type" type="text" />
            Contact Information: <input name = "contact_info" type="text" />
            <input value = "Update!" type = "submit" />
        </form>
    '''.format(str(id))

    # Return home
    html += return_to_landing_page_html

    return html

@route('/showrelation/<id>')
def showrelation(id):
    '''
    Show relation in Donate table with respect to record in Donors.
    '''
    # Create show relation command
    show_relation_command = "SELECT * FROM {} WHERE donor_id = {};".format(TABLE_NAMES[1], str(id))

    # Show relation message
    show_relation_message = "Records of Relation Donate:"
    html = "<h3> {} </h3> <br/> <table>".format(show_relation_message)

    # Display table
    display_columns = True
    for row in cur.execute(show_relation_command):
        html += "<tr>"
        if display_columns:
            column_names = ['Donation ID', 'Donor ID', 'Blood ID', 'Drive ID']
            for column in column_names:
                html += "<td>" + str(column) + "</td>"
            html += newline_html
            display_columns = False
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
    html += "</table>"

    # Return home
    html += return_to_landing_page_html

    return html

@route('/addrelation/<id>')
def addrelation(id):
    '''
    Add relation in Donate table linked to record in Donors table.
    '''
    # Add relation message
    add_relation_message = "Add Record to Donate Linked to Record in Donors:"
    html = "<h3> {} </h3> <br/>".format(add_relation_message)

    # Insert record form
    html += '''
        <form action = "/insertrelation/{}" method = "post">
            Donation ID: <input name = "donate_id" type="text" />
            Drive ID: <input name = "drive_id" type="text" />
            <input value = "Insert!" type = "submit" />
        </form>
    '''.format(str(id))

    # Create show relation command
    show_relation_command = "SELECT * FROM {}".format(TABLE_NAMES[1])

    # Show relation message
    show_relation_message = "Records of Relation Donate:"
    html += "<h3> {} </h3> <br/> <table>".format(show_relation_message)

    # Display table
    display_columns = True
    for row in cur.execute(show_relation_command):
        html += "<tr>"
        if display_columns:
            column_names = ['Donation ID', 'Donor ID', 'Blood ID', 'Drive ID']
            for column in column_names:
                html += "<td>" + str(column) + "</td>"
            html += newline_html
            display_columns = False
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
        html += "<td><a href=\"/linkrelation/{" + str(row[0]) + "}{" + str(id) + "}\">Link</a> </td>"
    html += "</table>"

    # Return home
    html += return_to_landing_page_html

    return html

@route('/linkrelation/<ids>')
def linkrelation(ids):
    '''
    Link record in Donors table.
    '''
    # Get donation and donor ids
    ids = ids.split('}{')
    donation_id, donor_id = ids[0][1:], ids[1][:-1]

    # Get blood id command
    get_blood_id_command = "SELECT * FROM {} WHERE donor_id = {}".format(TABLE_NAMES[0], 
                                                                         donor_id)
    
    # Get blood id
    blood_id = -1
    for row in cur.execute(get_blood_id_command):
        blood_id = row[3]
    # Get drive id
    get_drive_id_command = "SELECT * FROM {} WHERE donation_id = {}".format(TABLE_NAMES[1], 
                                                                         donation_id)
    for row in cur.execute(get_drive_id_command):
        drive_id = row[3]

    # Create update commands
    update_command = "UPDATE {} SET {} = '{}' WHERE donation_id = {} AND drive_id= {};"
    update_commands = []

    updates = {'donor_id':donor_id, 
               'blood_id':blood_id}

    for name, value in updates.items():
        cmd = update_command.format(TABLE_NAMES[1], 
                                    name, 
                                    value, 
                                    donation_id, 
                                    drive_id)
        update_commands.append(cmd)

    # Execute commands
    for cmd in update_commands:
        cur.execute(cmd)
        con.commit()

    # Return home
    html = record_linked_html + break_html + break_html
    # View changes
    html += "<td><a href=\"/showrelation/" + str(donor_id) + "\">Display Donate</a> </td>"

    return html

@post('/insertrelation/<id>')
def insertrelation(id):
    '''
    Insert record in Donors table.
    '''
    # Error flags
    insert_error_flag = False
    non_unique_error_flag = False
    # Get record attributes
    donate_id = request.forms.get('donate_id')
    drive_id = request.forms.get('drive_id')
    donor_id = str(id)
    get_blood_id_command = "SELECT * FROM {} WHERE donor_id = {}".format(TABLE_NAMES[0], 
                                                                         donor_id)
    for row in cur.execute(get_blood_id_command):
        blood_id = row[3]

    data = {'Donation ID':donate_id, 
            'Drive ID':drive_id}

    # Create commands
    get_donate_id_command = "SELECT * FROM {};".format(TABLE_NAMES[1])
    donate_ids = []
    for row in cur.execute(get_donate_id_command):
        donate_ids.append(int(row[0]))

    # Error Handling

    invalid_data = []
    for name, d in data.items():
        if d == "":
            insert_error_flag = True
            invalid_data.append(name)
        for part in d:
            if part not in "0123456789":
                insert_error_flag = True
                invalid_data.append(name)

    if donate_id != "" and not insert_error_flag:
        if int(donate_id) in donate_ids:
            non_unique_error_flag = True

    if (not insert_error_flag) and (not non_unique_error_flag):
        # Valid data
        # Create command
        insert_command = "INSERT INTO {} values ('{}', {}, {}, '{}')".format(TABLE_NAMES[1], 
                                                                             donate_id, 
                                                                             donor_id, 
                                                                             blood_id, 
                                                                             drive_id)

        # Execute command
        cur.execute(insert_command)
        con.commit()

        # Return home
        html = record_inserted_linked_html + newline_html + break_html

        # View changes
        html += "<td><a href=\"/showrelation/" + str(donor_id) + "\">Display Donate</a> </td>"
    else:
        # Invalid data
        html = ""
        if non_unique_error_flag:
            html += "Donation ID chosen was not unique!"
        if insert_error_flag:
            html += "Values Provided For {}".format(invalid_data[0])
            for i in range(1, len(invalid_data)):
                html += ", {}".format(invalid_data[i])
            html += " Are Invalid!"+ break_html + break_html

        # Acceptable data
        html += "All Fields Must Contain Non-Empty/Non-Null Value And Integers. Donation ID Must Be Unique." + break_html + break_html

        # Return home
        html += return_to_landing_page_html

    return html

@route('/insertform/')
def insertform():
    '''
    Insert record to Donors table by getting data through form.
    '''
    insert_message = "Enter Record Values:"
    html = "<h3> {} </h3> <br />".format(insert_message)

    html += '''
        <form action = "/insert" method = "post">
            Name: <input name = "name" type="text" />
            Blood Type: <input name = "blood_type" type="text" />
            Blood ID: <input name = "blood_id" type="text" />
            Contact Information: <input name = "contact_info" type="text" />
            <input value = "Insert!" type = "submit" />
        </form>
    '''

    return html

@post('/insert')
def insert():
    '''
    Insert data into Donors table.
    '''

    # Error flag
    insert_error_flag = False

    # Get data
    name = request.forms.get('name')
    blood_type = request.forms.get('blood_type')
    blood_id = request.forms.get('blood_id')
    contact_info = request.forms.get('contact_info')

    data = {'Name':name, 
            'Blood Type':blood_type, 
            'Blood ID': blood_id, 
            'Contact Information': contact_info}

    # Check data (Error Handling)
    invalid_data = []
    for n, d in data.items():
        if d == "" and n != 'Contact Information':
            insert_error_flag = True
            invalid_data.append(n)

    if blood_type not in blood_types:
        insert_error_flag = True
        invalid_data.append('Blood Type')
    invalid_data = list(set(invalid_data))

    if not insert_error_flag:
        # Valid data
        # Get donor id
        get_donor_id_command = "SELECT * FROM {};".format(TABLE_NAMES[0])
        donor_ids = []
        for row in cur.execute(get_donor_id_command):
            donor_ids.append(int(row[0]))

        # Ensure uniqueness of pkey
        donor_id = max(donor_ids) + 1

        # Create command
        insert_command = "INSERT INTO {} VALUES ('{}', '{}', '{}', '{}', '{}');".format(TABLE_NAMES[0], 
                                                                                       donor_id, 
                                                                                       name, 
                                                                                       blood_type, 
                                                                                       blood_id, 
                                                                                       contact_info)
        print(insert_command)

        # Execute command
        cur.execute(insert_command)
        con.commit()

        # Return home
        html = record_inserted_html
    else:
        # Invalid data
        # Acceptable data must contain
        html = "All Fields Must Contain Non-Empty/Non-Null Value (with the exception of Contact Information)." + break_html + break_html
        html += "Valid Blood Types - O positive, O negative, A positive, A negative, B positive, B negative, AB positive, AB negative." + break_html + break_html

        # Return home
        html += return_to_landing_page_html

    return html

@post('/search')
def search():
    '''
    Search page with search results and links to most other pages (each with its own functionality).
    '''
    # Create search command
    search_command = "SELECT * FROM {} WHERE ".format(TABLE_NAMES[0])
    search_params = []

    # Get and check data
    donor_name = request.forms.get('name')
    if donor_name != "":
        search_params.append(" name = '{}' ".format(donor_name))
    blood_type = request.forms.get('blood_type')
    if blood_type != "":
        search_params.append(" blood_type LIKE '{}' ".format(blood_type))

    # Create sql command
    if len(search_params) == 0:
        empty_search_message = "<h4> {} </h4>".format("You did not search for any specific data, so here's the first 20 records (if 20 exist)")
        search_command = "SELECT * FROM {}".format(TABLE_NAMES[0])
    else:
        empty_search_message = ""
        for i in range(len(search_params)):
            if i == 0:
                search_command += search_params[i]
            else:
                search_command += " AND " + search_params[i]
    search_command += " LIMIT {};".format(SEARCH_LIMIT)

    # Insert records message
    insert_records_x_message = "Insert Records in Donors:"
    html = "<h3> {} </h3> ".format(insert_records_x_message)
    # Insert
    html += "<td><a href=\"/insertform/\">Insert Records Here</a> </td>"

    # Display search results message
    search_results_message = "Search Results Requested (Hard limit of 20 records):"
    html += "<h3> {} </h3> <table>".format(search_results_message)

    html += empty_search_message

    # Display table
    display_columns = True
    for row in cur.execute(search_command):
        html += "<tr>"
        if display_columns:
            column_names = ['Donor ID', 'Name', 'Blood Type', 'Blood ID', 'Contact Information']
            for column in column_names:
                html += "<td>" + str(column) + "</td>"
            html += newline_html
            display_columns = False
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
        html += "<td><a href=\"/view/" + str(row[0]) + "\">View/Update</a> </td>"
        html += "<td><a href=\"/delete/" + str(row[0]) + "\">Delete</a> </td>"
        html += "<td><a href=\"/showrelation/" + str(row[0]) + "\">Display Donate</a> </td>"
        html += "<td><a href=\"/addrelation/" + str(row[0]) + "\">Add Record To Donate</a> </td> {}".format(newline_html)
    html += "</table>"

    # Return home
    html += return_to_landing_page_html

    return html

@route('/')
def landing_page():

    # Welcome message
    html = "<h1> {} </h1> <br/>".format(welcome_message)
    html += break_html

    # Database information
    database_information = "<h4> Database Tables - {}, {}.</h4>".format(TABLE_NAMES[0], TABLE_NAMES[1])
    html += database_information

    # Table message
    table_display_message = "{} Table Information:".format(TABLE_NAMES[0])
    html += "<h3> {} </h3> <table>".format(table_display_message)

    # Display table
    show_all_command = "SELECT * FROM {};".format(TABLE_NAMES[0])
    display_columns = True
    for row in cur.execute(show_all_command):
        html += "<tr>"
        if display_columns:
            column_names = ['Donor ID', 'Name', 'Blood Type', 'Blood ID', 'Contact Information']
            for column in column_names:
                html += "<td>" + str(column) + "</td>"
            html += newline_html
            display_columns = False
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
    html += "</table>"
    html += break_html

    # Search message
    search_display_message = "Donors Search Form:"
    html += "<h3> {} </h3> <br/>".format(search_display_message)

    # Search form
    html += '''
        <form action = "/search" method = "post">
            Donor Name: <input name = "name" type="text" />
            Blood Type*: <input name = "blood_type" type="text" />
            <input value = "Search!" type = "submit" />
        </form>
    '''

    # Wildcard message
    wildcard_message = "* Indicative of wildcard search. User is given the flexibility to use wildcard characters such as %."
    html += "<h4> {} </h4> <br/>".format(wildcard_message)

    # Blood types allowed message
    blood_types_allowed = "Valid Blood Types - O positive, O negative, A positive, A negative, B positive, B negative, AB positive, AB negative." + break_html + break_html
    html += blood_types_allowed

    return html








# Run website

run(host=HOST_NAME, 
    port=PORT_NUMBER, 
    debug = True)