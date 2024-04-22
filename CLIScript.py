import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Function to establish a connection to the database
def connect_to_db():
    connection = psycopg2.connect( # All the database info
        user="postgres",
        password="Froggy98!",
        host="127.0.0.1",
        port="5432",
        database="postgres"
    )

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # Set connection to autocommit

    return connection

# Function to execute a query
def execute_query(query, args=None):
    connection = None
    try:
        connection = connect_to_db() # Establish new connection
        cursor = connection.cursor() # Create cursor

        if query.strip().upper().startswith('SELECT'):
            if args:
                cursor.execute(query, args)
            else:
                cursor.execute(query)
            results = cursor.fetchall()  # Fetch rows of the query result set and return them
        else:
            if args:
                cursor.execute(query, args)
            else:
                cursor.execute(query)
            results = None  # Otherwise return none

        connection.commit()

        return results
    except psycopg2.DatabaseError as e: # In case of a database error, roll back the transaction
        if connection:
            connection.rollback()
        raise # Reraise the exception to be handled by the calling function

    finally: # Making sure the database connection is closed
        if connection:
            connection.close()

# CLI Interface
def run_cli():
    while True:
        print("""
        Welcome to the F1 Database! 
        
        Records are kept since 1950. Please keep in mind entries are case-sensitive 
        (i.e. if you are searching a driver, make sure to capitalize the first letter)!
        
        1. Add a driver, circuit, or constructor
        2. Delete a driver, circuit, or constructor
        3. Update a driver's home country
        4. Search all races for a driver
        5. Find total points for a team
        6. List drivers or constructors by points
        7. Find drivers and their teams per race
        8. Group drivers by nationality
        9. Find drivers who have completed a race in a higher position than their grid position
        10. Update points for a constructor and driver
        
        Enter any other number to exit. 
        """) # Print options for user to select
        choice = input("\n\t\tEnter the number of the operation you want to perform: ") # Get user choice

        # Invalid number/input check
        try:
            choice_number = int(choice)
        except ValueError: # If inputted value is not a number
            print("\n\t\tInvalid input, not a number. Exiting.")
            break

        if choice_number < 1 or choice_number > 10: # If any other number besides 1-10
            print("\n\t\tThanks for using, goodbye!")
            break

        else: # Proceed with normal operations
            if choice == "1": # Insert Operation (Insert a driver, circuit, or constructor)
                print("""
                1. Add a driver
                2. Add a circuit
                3. Add a constructor""") # Print options for user to select
                choice = input("\n\t\tEnter the number of the operation you want to perform: ")   # Get user choice

                if choice == "1": # Insert a driver
                    try:
                        driverid = input("\n\t\tEnter the driver identification number (ex: 1): ")  # Get driver id
                        forename = input("\t\tEnter the first name of the driver (ex: 'John'): ") # Get driver forename
                        surname = input("\t\tEnter the last name of the driver (ex: 'Doe'): ") # Get driver surname
                        code = input("\t\tEnter the three character driver code (ex: 'DOE'): ") # Get driver code
                        dob = input("\t\tEnter the driver's date of birth (ex: 'YYYY-MM-DD'): ")  # Get driver dob
                        nationality = input("\t\tEnter the driver's nationality (ex: 'American'): ")  # Get driver nationality
                        home = input("\t\tEnter the driver's current country of residence (ex: 'USA'): ")  # Get driver home

                        columns = ['driverid', 'driver_forename', 'driver_surname', 'driver_code', 'driver_dob', 'driver_nationality', 'driver_home'] # Put columns into list for query
                        values = [driverid, forename, surname, code, dob, nationality, home] # Put values into list for query
                        values_str = [f"'{value}'" for value in values]  # Add single quotes around each value

                        # Formulate query to add driver to drivers
                        query = f"INSERT INTO drivers ({', '.join(columns)}) VALUES ({', '.join(values_str)});"

                        print("Columns:", columns)
                        print("Values:", values)
                        print("Query:", query)
                        # Execute query
                        execute_query(query)
                        print(f"\n\t\tDriver {driverid} successfully added!") # Operation success

                    except Exception as e: # If error, notify user
                        print(f"\n\t\tAn error occurred adding a driver: {str(e)}") # Operation failed

                elif choice=="2": # Insert a circuit
                    try:
                        circuitid = input("\n\t\tEnter the circuit identification number (ex: 1): ")  # Get circuit id
                        name = input("\t\tEnter the name of the circuit (ex: 'Silverstone Circuit'): ") # Get circuit name
                        location = input("\t\tEnter the name of the circuit location (ex: 'Silverstone'): ") # Get circuit location
                        country = input("\t\tEnter the name of the circuit country (ex: 'UK'): ") # Get circuit country


                        columns1 = ['circuitid', 'circuit_name']  # Put columns into list for query 1
                        columns2 = ['circuitid', 'circuit_location'] # Put columns into list for query 2
                        columns3 = ['circuitid', 'circuitcountry'] # Put columns into list for query 3

                        values1 = [circuitid, name] # Put values into list for query 1
                        values2 = [circuitid, location] # Put values into list for query 2
                        values3 = [circuitid, country] # Put values into list for query 3

                        values_str1 = [f"'{value}'" for value in values1]  # Add single quotes around each value
                        values_str2 = [f"'{value}'" for value in values2]  # Add single quotes around each value
                        values_str3 = [f"'{value}'" for value in values3]  # Add single quotes around each value

                        # Start the transaction
                        print("\n\t\tStarting a transaction...") # This is a transaction since a circuit has to be added to all 3 tables or none of them
                        connection = connect_to_db()  # Establish new connection
                        cursor = connection.cursor()  # Create cursor
                        connection.autocommit = False  # Turn off autocommit

                        # Formulate query 1 to add circuit to circuits
                        query1 = f"INSERT INTO circuits ({', '.join(columns1)}) VALUES ({', '.join(values_str1)});"

                        cursor.execute(query1)

                        # Formulate query 2 to add circuit to circuitlocation
                        query2 = f"INSERT INTO circuitlocation ({', '.join(columns2)}) VALUES ({', '.join(values_str2)});"

                        cursor.execute(query2)

                        # Formulate query 3 to add circuit to circuitcountry
                        query3 = f"INSERT INTO circuitcountry ({', '.join(columns3)}) VALUES ({', '.join(values_str3)});"

                        cursor.execute(query3)

                        connection.commit() # Execute queries
                        print("\t\tTransaction completed successfully.") # Operation success
                        print(f"\n\t\tCircuit {circuitid} successfully added!")


                    except Exception as e:  # If error, roll back the transaction to revert all changes
                        print(f"\t\tAn error occurred during adding the circuit {circuitid}: {e}") # Operation failed
                        print("\t\tTransaction rolled back.")
                        connection.rollback() # Rollback to revert all changes

                    finally:  # Close the cursor and the connection
                        if cursor:
                            cursor.close()
                        if connection:
                            connection.close()

                elif choice=="3": # Insert a constructor
                    try:
                        constructorid = input("\n\t\tEnter the constructor identification number (ex: 1): ") # Get constructor id
                        name = input("\t\tEnter the constructor name (ex: 'Williams'): ") # Get constructor name
                        home = input("\t\tEnter the constructor home (ex: 'USA'): ")  # Get constructor home

                        columns = ['constructorid', 'constructor_name', 'constructor_home'] # Put columns into list for query
                        values = [constructorid, name, home] # Put values into list for query
                        values_str = [f"'{value}'" for value in values]  # Add single quotes around each value

                        # Formulate query to add constructor to constructors
                        query = f"INSERT INTO constructors ({', '.join(columns)}) VALUES ({', '.join(values_str)});"

                        # Execute query
                        execute_query(query)
                        print(f"\n\t\t{constructorid} successfully added!") # Operation success

                    except Exception as e: # If error, notify user
                        print(f"\n\t\tAn error occurred adding {name}: {str(e)}") # Operation failed

            elif choice == "2": # Delete Operation (Delete a driver, circuit, or constructor)
                print("""
                1. Delete a driver
                2. Delete a circuit
                3. Delete a constructor""") # Print options for user to select
                choice = input("\n\t\tEnter the number of the operation you want to perform: ")  # Get choice from user
                if choice == "1": # Delete a driver
                    try:
                        driverid = input("\n\t\tEnter the driver identification number (ex: 1): ")  # Get driver id

                        # Formulate query to delete driver from drivers
                        query = f"DELETE FROM drivers WHERE driverid={driverid};"

                        # Execute query
                        execute_query(query)

                        print(f"\n\t\tDriver {driverid} removed.")  # Operation success

                    except Exception as e: # If error, notify user
                        print(f"\n\t\tAn error occurred deleting a driver: {e}") # Operation failed

                elif choice == "2": # Delete a circuit
                    try:
                        circuitid = input("\t\tEnter the circuit identification number (ex: 1): ") # Get circuit id

                        # Start the transaction
                        print("\n\t\tStarting a transaction...") # This is a transaction since a circuit has to be deleted from all 3 tables or none of them

                        connection = connect_to_db()  # Establish new connection
                        cursor = connection.cursor()  # Create cursor
                        connection.autocommit = False  # Turn off autocommit

                        # Formulate query 1 to delete circuit from circuits
                        query1 = f"DELETE FROM circuits WHERE circuitid={circuitid};"

                        cursor.execute(query1)

                        # Formulate query 2 to delete circuit from circuitlocation
                        query2 = f"DELETE FROM circuitlocation WHERE circuitid={circuitid};"

                        cursor.execute(query2)

                        # Formulate query 3 to delete circuit from circuitcountry
                        query3 = f"DELETE FROM circuitcountry WHERE circuitid={circuitid};"

                        cursor.execute(query3)

                        connection.commit() # Execute queries
                        print("\t\tTransaction completed successfully.")
                        print(f"\n\t\tCircuit {circuitid} successfully deleted!") # Operation success


                    except Exception as e:  # If error, roll back the transaction to revert all changes
                        print(f"\n\t\tAn error occurred during deleting the circuit {circuitid}: {e}") # Operation failed
                        print("\t\tTransaction rolled back.")
                        connection.rollback() # Rollback to revert all changes

                    finally:  # Close the cursor and the connection
                        if cursor:
                            cursor.close()
                        if connection:
                            connection.close()

                elif choice == "3": # Delete a constructor
                    try:
                        constructorid = input("\n\t\tEnter the constructor identification number (ex: 1): ")  # Get constructor id

                        # Formulate query to delete constructor from constructors
                        query = f"DELETE FROM constructors WHERE constructorid={constructorid};"

                        # Execute query
                        execute_query(query)

                        print(f"\n\t\tConstructor {constructorid} removed.") # Operation success

                    except Exception as e:  # If error, notify user
                        print(f"\n\t\tAn error occurred deleting constructor {constructorid}: {e}") # Operation failed

            elif choice == "3": # Update Operation (Update a driver's home)
                try:
                    driverid = input("\n\t\tEnter the driver identification number (ex: 1): ")  # Get driver id
                    home = input("\t\tEnter the driver's new home (ex: 'Germany'): ") # Get driver home from user

                    # Formulate query to update drivers with new home
                    query = f"UPDATE drivers SET driver_home='{home}' WHERE driverid={driverid};"

                    # Execute query
                    execute_query(query)

                    print(f"\n\t\tUpdate operation completed on driver {driverid}.") # Operation success

                except Exception as e: # If error, notify user
                    print(f"\n\t\tAn error occurred during the updating the driver's home location {e}") # Operation failed

            elif choice == "4": # Search Operation (Find races for a particular driver)
                try:
                    surname = input("\n\t\tEnter the driver's last name (ex: 'Hamilton', case-sensitive): ")  # Get driver surname

                    # Formulate query to select races and circuit name information for the given driver's last name
                    query = f"""
                        SELECT races.*, circuits.circuit_name 
                        FROM races 
                        JOIN circuits ON races.circuitid = circuits.circuitid 
                        JOIN driverresults ON races.raceid = driverresults.raceid
                        JOIN drivers ON driverresults.driverid = drivers.driverid
                        WHERE drivers.driver_surname = '{surname}';
                    """

                    # Execute query, save results
                    results = execute_query(query)

                    if results:  # If results found, print
                        print("\n\t\tRace ID\tYear\tRound\tCircuit ID\tCircuit Name\n")
                        print("\t\t---------------------------------------------------------------------------------------------------")
                        for row in results:
                            raceid, year, round, circuitid, circuit=row
                            print(f"\n\t\t{raceid}\t{year}\t{round}\t{circuitid}\t{circuit}") # Operation success
                    else:  # No results found
                        print("\n\t\tNo races found for that driver.") # Operation success, just no results

                except Exception as e:  # If error, notify user
                    print(f"\n\t\tAn error occurred searching for races: {e}") # Operation failed

            elif choice == "5":  # Aggregate Operations (Find points for a constructor)
                try:
                    name = input("\n\t\tEnter the team name (ex: 'Ferrari', case-sensitive): ")  # Get constructor name

                    # Formulate query to select constructorid and sum of points for the given constructor name
                    query = f"""
                        SELECT cs.constructorid, SUM(cs.points) AS TotalPoints
                        FROM constructorstandings AS cs
                        JOIN constructors AS c ON cs.constructorid = c.constructorid
                        WHERE c.constructor_name = '{name}'
                        GROUP BY cs.constructorid;
                    """

                    # Execute query, save results
                    results = execute_query(query)

                    if results:  # If results found, print
                        for row in results:
                            constructor_id, points = row
                            print(f"\n\t\tTotal points for  {name}: {points}") # Operation success
                    else:
                        print(f"\n\t\tNo points found for '{name}'") # Operation success, just no results.

                except Exception as e:  # If error, notify user
                    print(f"\n\t\tAn error occurred calculating points: {e}") # Operation failed

            elif choice == "6": # Sorting Operation (Sort drivers or constructors by points)
                print("""
                1. Sort by drivers
                2. Sort by constructors""") # Print options for user to select
                choice = input("\n\t\tEnter the number of the operation you want to perform: ")  # Get choice from user

                if choice == "1": # Sort by drivers
                    try:
                        order = input("\n\t\tEnter the sort order ('ASC' for ascending, 'DESC' for descending): ").upper()  # Get sort order choice from user

                        if order.upper() not in ['ASC', 'DESC']: # Checking to make sure order is supported
                            print("\n\t\tInvalid sort order. Please enter 'ASC' or 'DESC'.") # Invalid order choice made by user
                            continue

                        # Formulate query to sort drivers by points
                        query = f"""
                                SELECT d.driver_surname, d.driver_code, COALESCE(ds.TotalPoints, 0) AS TotalPoints
                                FROM drivers AS d
                                LEFT JOIN (
                                    SELECT driverid, SUM(points) AS TotalPoints
                                    FROM driverresults
                                    GROUP BY driverid
                                ) AS ds ON d.driverid = ds.driverid
                                ORDER BY TotalPoints {order};
                            """

                        # Execute query, save results
                        results = execute_query(query)

                        if results:  # If results found, print
                            print("\n\t\tDriver: Points")
                            print("\t\t--------------------------------------")
                            for row in results:
                                driver, code, points = row
                                print(f"\n\t\t{driver}: {points}") # Operation success
                        else:
                            print("\n\t\tNo results found.") # Operation failed

                    except Exception as e: # If error, notify user
                        print(f"\n\t\tAn error occurred during the sorting operation: {e}") # Operation failed

                elif choice == "2": # Sort by constructors
                    try:
                        order = input("\n\t\tEnter the sort order ('ASC' for ascending, 'DESC' for descending): ").upper()  # Get sort order choice from user

                        if order not in ['ASC', 'DESC']:  # Checking to make sure order is supported
                            print("\n\t\tInvalid sort order. Please enter 'ASC' or 'DESC'.") # Invalid order choice made by user
                        else:
                            # Formulate query to sort constructors by points
                            query = f"""
                                SELECT c.constructor_name, COALESCE(cs.TotalPoints, 0) AS TotalPoints
                                FROM constructors AS c
                                LEFT JOIN (
                                    SELECT constructorID, SUM(points) AS TotalPoints
                                    FROM ConstructorStandings
                                    GROUP BY constructorID
                                ) AS cs ON c.constructorID = cs.constructorID
                                ORDER BY TotalPoints {order};
                            """

                            # Execute query, save results
                            results = execute_query(query)

                            if results:  # If results found, print
                                print("\n\t\tConstructor: Points")
                                print("\t\t--------------------------------------")
                                for row in results:
                                    constructor, points = row
                                    print(f"\n\t\t{constructor}: {points}") # Operation success
                            else:
                                print("\n\t\tNo results found.") # Operation failed

                    except Exception as e:  # If error, notify user
                        print(f"\n\t\tAn error occurred during the sorting operation: {e}") # Operation failed

            elif choice == "7": # Join Operation (Find drivers and their constructors for a race)
                try:
                    raceid = input("\n\t\tEnter the race identification number (ex: 1): ")  # Get race id

                    # Formulate query to find drivers and their constructors for a race
                    query = f"""
                        SELECT D.driver_forename, D.driver_surname, C.constructor_name
                        FROM Drivers D
                        JOIN Qualifying Q ON D.driverid = Q.driverid
                        JOIN Constructors C ON Q.constructorid = C.constructorid
                        WHERE Q.raceId = {raceid};
                    """
                    # Execute query, save results
                    results = execute_query(query)

                    if results:  # If results found, print
                        print("\n\t\tName, Constructor")
                        print("\t\t--------------------------------------")
                        for row in results:
                            first, last, team = row
                            print(f"\n\t\t{first} {last}, {team}") # Operation success
                    else:
                        print("\n\t\tNo results found.") # Operation success, just no results.

                except Exception as e: # If error, notify user
                    print(f"\n\t\tAn error occurred finding drivers: {e}") # Operation failed

            elif choice == "8":  # Grouping Operation (Group drivers by nationality and count them)
                try:
                    # Formulate query to group drivers by nationality and count them
                    query = """
                            SELECT driver_nationality, COUNT(*) AS Number_of_Drivers
                            FROM Drivers
                            GROUP BY driver_nationality;
                    """

                    # Execute query, save results
                    results = execute_query(query)

                    if results:  # If results found, print
                        print("\n\t\tNationality: Number of Drivers")
                        print("\t\t--------------------------------------")
                        for row in results:
                            driver_nationality, Number_of_Drivers = row
                            print(f"\n\t\t{driver_nationality}: {Number_of_Drivers}") # Operation success
                    else:
                        print("\n\t\tNo results found.") # Operation success, just no results found.

                except Exception as e: # If error, notify user
                    print(f"\n\t\tAn error occurred grouping drivers: {e}") # Operation failed

            elif choice == "9":  # Subquery Operation
                try:
                    driverid = input("\n\t\tEnter the driver identification number (ex: 1): ")  # Get driver id

                    # Formulate query to get drivers and their race ids
                    query = f"""
                            SELECT d.driver_code, dr.driverid, dr.raceid
                            FROM driverresults AS dr
                            JOIN drivers AS d ON dr.driverid = d.driverid
                            WHERE dr.driverid = {driverid} AND
                                  dr.position < dr.grid_position AND
                                  dr.position IN (
                                      SELECT MIN(position) FROM DriverResults AS sub
                                      WHERE sub.raceid = dr.raceid
                                      GROUP BY raceid
                                  );
                    """

                    # Execute the query, save results
                    results = execute_query(query)

                    if results:  # If results found, print
                        print("\n\t\tDriver Code\t\tRaceID")
                        print("\t\t--------------------------------------")
                        for row in results:
                            driver_code, driverid, raceid = row
                            print(f"\n\t\t{driver_code}\t\t\t\t{raceid}") # Operation success
                    else:
                        print("\n\t\tNo results found.") # Operation success, failed

                except Exception as e: # If error, notify user
                    print(f"\n\t\tAn error occurred during the subquery operation: {e}") # Operation failed

            elif choice == "10": # Transaction Operation (Update driver results and constructor points)
                try:
                    driverid = input("\n\t\tEnter the driver identification number (ex: 1): ")  # Get driver id
                    raceid = input("\t\tEnter the race identification number (ex: 1): ")  # Get race id
                    constructorid = input("\t\tEnter the constructor identification number (ex: 1): ")  # Get constructor id
                    points = input("\t\tEnter the points earned: ")  # Get points

                    # Start the transaction
                    print("\n\t\tStarting a transaction...") # This is a transaction since points are updated for a constructor only if a race was updated for a driver
                    connection = connect_to_db()  # Establish new connection
                    cursor = connection.cursor()  # Create cursor
                    connection.autocommit = False  # Turn off autocommit

                    # Formulate query 1 to update driver results
                    query1 = f"""
                        UPDATE driverresults
                        SET points = points + {points}
                        WHERE driverid = {driverid} AND raceid = {raceid};
                    """
                    cursor.execute(query1)

                    # Formulate query 2 to update constructor standings
                    query2 = f"""
                        UPDATE constructorstandings
                        SET points = points + {points}
                        WHERE constructorID = {constructorid} AND raceID = {raceid};
                    """
                    cursor.execute(query2)

                    # Commit the transaction
                    connection.commit()
                    print("\n\t\tTransaction completed successfully.") # Operation success


                except Exception as e:  # If error, roll back the transaction to revert all changes
                    print(f"\n\t\tAn error occurred during the transaction operation: {e}") # Operation failed
                    print("\t\tTransaction rolled back.")
                    connection.rollback()

                finally:  # Close the cursor and the connection
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()

# Run
run_cli()
