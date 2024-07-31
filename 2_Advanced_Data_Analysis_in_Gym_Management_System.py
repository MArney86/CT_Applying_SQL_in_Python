from connect_mysql import connect_database
from mysql.connector import Error

def get_members_in_age_range(start_age, end_age):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to get all columns from Members between the input start and end ages
            query = "SELECT * FROM Members WHERE age BETWEEN %s and %s"

            #Execute query
            cursor.execute(query, (start_age, end_age))
            
            #collect results
            results = cursor.fetchall()

            #Verify there are results to display
            if results:
                #Headings for output
                print(f"Members between {start_age} and {end_age} in age:")
                print("\033[4m|Member ID   | Member Name                  | Member Age |\033[0m")
                
                #formatting and printing results from MySQL
                for result in results:
                    #unpacking results tuple
                    member_id, name, age = result

                    #calculate padding for formatted cells
                    id_cell = 12 - len(str(member_id))
                    name_cell = 30 - len(name)
                    age_cell = 12 - len(str(age))

                    #format and print results
                    formatted = ("|" + str(member_id) + " " * id_cell) +'|' + name + (" " * name_cell) + "|" + str(age) + (" " * age_cell) + "|"
                    print(formatted)
                
            #no results and notification of such to user
            else:
                print(f"There were no results for Members between the ages of {start_age} and {end_age}")
                
        #exceptions
        except Error as e:
            print(f"Error: {e}") #general error
        #close connections
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

get_members_in_age_range(20, 25)