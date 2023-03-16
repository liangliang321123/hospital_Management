import pyodbc
from datetime import date

class Patient:
    def __init__(self, name, age, gender, date_of_birth, contact_info):
        self.name = name
        self.age = age
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.contact_info = contact_info

class Hospital:
        def __init__(self, server, database):
            self.connection = pyodbc.connect(f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database}")
            self.cursor = self.connection.cursor()

        def __del__(self):
            self.connection.close()

        def add_patient(self, details):
            query1 = f"INSERT INTO patientTable (name, age, gender, date_of_birth, contact_info) VALUES ('{details.name}', {details.age}, '{details.gender}', CONVERT(DATE, '{details.date_of_birth}', 23), '{details.contact_info}')"
            self.cursor.execute(query1)

            details.id = self.cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]

            query2 = f"INSERT INTO patientVisitTable (id, check_in_date) VALUES ( {details.id}, CONVERT(DATE, '{date.today()}', 23))"
            self.cursor.execute(query2)
            self.connection.commit()

        def view_patient(self):
            query = "SELECT * FROM patientTable"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            if len(rows) == 0:
                print("No data found")
            else:
                print("Result")
                print("--id-----------------")
                for i, row in enumerate(rows):
                    print(f"{i+1}.{row.id} - {row.name} - {row.age} - {row.gender} - {row.date_of_birth} - {row.contact_info}")

        def update_details(self, patient_id, selection):
            if selection == 1:
                re_name = input("Please enter the name.")
                query = f"UPDATE patientTable SET name='{re_name}' WHERE id = {patient_id}"
                self.cursor.execute(query)
                self.connection.commit()
            elif selection == 2:
                re_age = input("Please enter the age.")
                query = f"UPDATE patientTable SET age={re_age} WHERE id = {patient_id}"
                self.cursor.execute(query)
                self.connection.commit()
            elif selection == 3:
                re_gender = input("Please enter the gender.(M/F)").upper()
                query = f"UPDATE patientTable SET gender='{re_gender}' WHERE id = {patient_id}"
                self.cursor.execute(query)
                self.connection.commit()
            elif selection == 4:
                re_birth = input("Please enter the DOB.")
                query = f"UPDATE patientTable SET date_of_birth= CONVERT(DATE, '{re_birth}') WHERE id = {patient_id}"
                self.cursor.execute(query)
                self.connection.commit()
            elif selection == 5:
                re_info = input("Please enter the Contact Info.")
                query = f"UPDATE patientTable SET contact_info='{re_info}' WHERE id = {patient_id}"
                self.cursor.execute(query)
                self.connection.commit()
            else:
                print("Invalid Input")

        def add_patient_status(self, patient_id):

            check_out_date = input("Please enter patient check out date YYYY-MM-DD :")
            patState = input("Please enter patient status ( Stable / Unstable / Danger): ")
            query1 = f"SELECT check_in_date FROM patientVisitTable WHERE id = {patient_id}"
            self.cursor.execute(query1)

            check_in_date = self.cursor.fetchone()[0]

            query2 = f"INSERT INTO patientVisitTable (id ,check_in_date, check_out_date, status) VALUES ({patient_id}, CONVERT(DATE, '{check_in_date}', 23), CONVERT(DATE, '{check_out_date}', 23), '{patState}')"
            self.cursor.execute(query2)
            self.connection.commit()

        def remove_patient(self, patient_id):

            confirmation = input("Do you sure want to remove ? (Y/N)").lower()
            if confirmation == "y":
                query = f"DELETE from patientTable WHERE id={patient_id}"
                self.cursor.execute(query)
                self.connection.commit()

        def search_function(self, searchName=None, searchAge=None, searchGender=None, searchDateOfBirth=None, searchContact=None):
            query = "SELECT * FROM patientTable WHERE 1=1"

            if searchName:
                query += f" AND name LIKE '%{searchName}%'"
            if searchAge:
                query += f" AND age = {searchAge}"
            if searchGender:
                query += f" AND gender = '{searchGender}'"
            if searchDateOfBirth:
                query += f" AND date_of_birth = CONVERT(DATE, '{searchDateOfBirth}',23)"
            if searchContact:
                query += f" AND contact_info = '{searchContact}'"

            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.connection.commit()

            if results:
                print("Search Results:")
                print("---------------")
                for row in results:
                    print(f"ID: {row[0]}")
                    print(f"Name: {row[1]}")
                    print(f"Age: {row[2]}")
                    print(f"Gender: {row[3]}")
                    print(f"Date of Birth: {row[4]}")
                    print(f"Contact Info: {row[5]}")
                    print("-----------------")
            else:
                print("No results found.")


    # search function ( by name, age ,gender, contact )


def main():
    server = "(localdb)\LocalDB"
    database = "patient"

    hospital = Hospital(server, database)

    while True:
        print("Welcome to Hospital Management")
        print("1. Add Patient\n"
              "2. View Patient\n"
              "3. Update Patient details\n"
              "4. Add Patient status\n"
              "5. Delete Patient\n"
              "6. Search Patient\n"
              "7. Quit")

        choice = int(input("Please enter your choice (1-6): "))

        if choice == 1:
            name = input("Enter patient name: ")
            age = int(input("Enter patient age: "))
            gender = input("Enter patient gender (M/F): ").upper()
            date_of_birth = input("Please enter patient date of birth in YYYY-MM-DD format: ")
            contact_info = input("Please enter the patient contact info: ")
            patient = Patient(name, age, gender, date_of_birth, contact_info)
            hospital.add_patient(patient)
            print("Patient details added to database")
        elif choice == 2:
            hospital.view_patient()
        elif choice == 3:
            hospital.view_patient()
            patient_id = int(input("Which patient detail do you want to update ?"))
            selection = int(input("Which part do you want to edit ? \n"
                                  "1. name\n"
                                  "2. age\n"
                                  "3. gender\n"
                                  "4. date Of Birth\n"
                                  "5. contact info"))
            hospital.update_details(patient_id, selection)
        elif choice == 4: # add patient check in check out stat
            #state = int(input("Which selection want to pick ? \n"
             #                 "1. Check-out date. :\n"
               #               "2. Status ( Stable, Unstable, Danger ) :"))
            hospital.view_patient()
            patient_id = int(input("Which patient detail status want to Add On ?"))

            hospital.add_patient_status(patient_id)

        elif choice == 5: # delete patient
            hospital.view_patient()
            patient_id = int(input("Which patient do you want to remove ?"))
            hospital.remove_patient(patient_id)

        elif choice == 6: # search patient
            print("Search")
            print("_______________")
            decide1 = input("Want to search by patient name ? (Y/N )").lower()
            decide2 = input("Want to search by patient age ? (Y/N )").lower()
            decide3 = input("Want to search by patient gender ? (Y/N )").lower()
            decide4 = input("Want to search by patient dob ? (Y/N )").lower()
            decide5 = input("Want to search by patient contact ? (Y/N )").lower()

            searchName = None
            searchAge = None
            searchGender = None
            searchDateOfBirth = None
            searchContact = None

            if decide1 == "y":
                searchName = input("Enter the patient name : ")
            else:
                pass

            if decide2 == "y":
                searchAge = int(input("Enter the patient age :"))
            else:
                pass

            if decide3 == "y":
                searchGender = input("Enter the patient gender ( M / F ) :")
            else:
                pass

            if decide4 == "y":
                searchDateOfBirth = input("Enter the patient date of birth (YYYY-MM-DD) :")
            else:
                pass

            if decide5 == "y":
                searchContact = input("Enter the patient contact :")
            else:
                pass

            hospital.search_function(searchName, searchAge, searchGender, searchDateOfBirth, searchContact)
        elif choice == 7:
            print("Thanks for using hospital Management")
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
