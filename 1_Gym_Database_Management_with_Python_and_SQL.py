from connect_mysql import connect_database
from mysql.connector import Error
import re

#Task 1
def add_member(id, name, age):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #Member information
            new_member = (id, name, age)

            #SQL Query
            query = "INSERT INTO Members (id, name, age) VALUES (%s, %s, %s)" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, new_member)
            conn.commit()
            print("New Member added successfully")

        #exceptions
        except Error as e:
            if e.errno == 1062:
                print("Error: The input Member ID is already in use.")
            elif e.errno == 1048:
                print("Error: The id value cannot be Null.")
            elif e.errno == 1406:
                print("Error: Value for name is too long.")
            elif e.errno == 1264:
                print("Error: Value for age is too large.")
            else:
                print(f"Error: {e}") #general error

        #close connections
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            
#Task 2
def add_workout_session(member_id, session_date, session_time, activity):

    time_verification = r'2[0-3]|[01]?[0-9]:[0-5][0-9]'
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            if re.match(time_verification, session_time): #check that the session time is in the correct format
                #query to get the numerically highest session_id:
                session_query = 'SELECT MAX(session_id) FROM WorkoutSessions'

                #execute the session_id query
                cursor.execute(session_query)
                session_id = cursor.fetchall()[0][0] #recieve the highest session id
                session_id += 1 #increment to serve as the new session_id

                #Member information
                new_workoutsession = (session_id, member_id, session_date, session_time, activity)

                #SQL Query
                query = "INSERT INTO WorkoutSessions (session_id, member_id, session_date, session_time, activity) VALUES (%s, %s, %s, %s, %s)" #iserts the new workout session in the WorkoutSessions table using the information passed to the function

                #Execute query
                cursor.execute(query, new_workoutsession)
                conn.commit()
                print("New Workout Session added successfully")
            else:
                #raise error because of incorrectly formatted time input
                raise Error("The time is not in the correct 24hr time format")

        #exceptions
        except Error as e:
            if e.errno == 1048:
                print("Error: The Workout Session ID value cannot be Null.")
            elif e.errno == 1406:
                index = e.msg.find("'")
                rindex = e.msg.rfind("'")
                index += 1
                column = e.msg[index:rindex]
                print(f"Error: Value for '{column}' is too long.")
            elif e.errno == 1264:
                print("Error: Value for Member ID is too large.")
            elif e.errno == 1452:
                print("Error: The input Member ID for the attempted Workout Session does not exist")
            else:
                print(f"Error: {e}") #general error

        #close connections
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

#Task 3:
def update_member_age(member_id, new_age):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #query to check that member_id is in the Members Table
            member_check = 'SELECT id FROM Members WHERE id = %s'

            #execute check query
            cursor.execute(member_check, (member_id,))

            #Check that member_id is in the Members Table
            if cursor.fetchall():
                #SQL Query
                query = "UPDATE Members SET age = %s WHERE id = %s"

                #Execute query
                cursor.execute(query, (new_age, member_id))
                conn.commit()
                print("Member age updated successfully")
            
            else:
                #raise error because of nonexistent member id
                raise Error("The Member ID input does not exist")

        #exceptions
        except Error as e:
            if e.errno == 1048:
                print("Error: The id value cannot be Null.")
            elif e.errno == 1264:
                print("Error: Value for age is too large.")
            else:
                print(f"Error: {e}") #general error
        #close connections
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

#Task 4
def delete_workout_session(session_id):
        #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #query to check that member_id is in the Members Table
            member_check = 'SELECT session_id FROM WorkoutSessions WHERE session_id = %s'

            #execute check query
            cursor.execute(member_check, (session_id,))

            #Check that member_id is in the Members Table
            if cursor.fetchall():
                #SQL Query
                query = "DELETE FROM WorkoutSessions WHERE session_id = %s"

                #Execute query
                cursor.execute(query, (session_id,))
                conn.commit()
                print("The selected Workout Session was deleted successfully")
            
            else:
                #raise error because of non existent session id
                raise Error("The Workout Session ID input does not exist")

        #exceptions
        except Error as e:
            if e.errno == 1048:
                print("Error: The Session ID value cannot be Null.")
            elif e.errno == 1264:
                print("Error: Value for Session ID is too large.")
            else:
                print(f"Error: {e}") #general error
        #close connections
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()