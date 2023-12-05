import random

from User import UserDatabase
from Admin import AdminDatabase
from Reservation import ReservationDatabase

def main():
    user_db = UserDatabase()
    reservation_db = ReservationDatabase()
    admin_db = AdminDatabase()

    while True:
        print("\nWelcome to the Restaurant System")
        print("1. Login")
        print("2. Register")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            user_id = user_db.login_user(username, password)

            if user_id is not None:
                role = user_db.get_role(user_id)
                print(f"Login successful. Welcome, {username}!")

                if role == "client":
                    handle_client_actions(user_id, user_db, reservation_db)
                elif role == "admin":
                    handle_admin_actions(user_db, admin_db, reservation_db)
                else:
                    print("Invalid role.")
            else:
                print("Login failed. Incorrect username or password.")

        elif choice == "2":
            username = input("Enter your desired username: ")
            password = input("Enter your desired password: ")
            role = input("Enter your role (client, admin): ")

            user_id = user_db.register_user(username, password, role)
            print(f"Registration successful. Welcome, {username}!")

            if role == "client":
                handle_client_actions(user_id, user_db, reservation_db)
            elif role == "admin":
                handle_admin_actions(user_db, admin_db, reservation_db)

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")

    user_db.close_connection()
    reservation_db.close_connection()
    admin_db.close_connection()


def handle_client_actions(user_id, user_db, reservation_db):
    while True:
        print("\nClient Actions:")
        print("1. Reserve a table")
        print("2. View reservations")
        print("3. Update user data")
        print("4. Logout")

        client_choice = input("Enter your choice: ")

        if client_choice == "1":
            date = input("Enter the reservation date (YYYY-MM-DD): ")
            table_number = int(input("Enter the table number: "))    

            # select random price 1000-5000
            price = int(random.randint(1000, 5000))

            reservation_db.add_reservation(user_id, date, table_number, price)
            print("Reservation successful!")

        elif client_choice == "2":
            reservations = reservation_db.filter_reservations(user_id=user_id)
            print("Your Reservations:")
            for reservation in reservations:
                print(reservation)

        elif client_choice == "3":
            new_username = input("Enter your new username: ")
            new_password = input("Enter your new password: ")

            new_data = {'username': new_username, 'password': new_password}
            user_db.update_user_data(user_id, new_data)
            print("User data updated successfully!")

        elif client_choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")


def handle_admin_actions(user_db, admin_db, reservation_db):
    while True:
        print("\nAdmin Actions:")
        print("1. View all users")
        print("2. Update user data")
        print("3. Delete user")
        print("4. Update reservation data")
        print("5. Delete reservation")
        print("6. Logout")

        admin_choice = input("Enter your choice: ")

        if admin_choice == "1":
            admin_password = input("Enter admin password: ")
            admin_db.view_all_users(user_db, admin_password)

        elif admin_choice == "2":
            admin_password = input("Enter admin password: ")
            user_id = int(input("Enter the user ID to update: "))
            new_username = input("Enter the new username: ")
            new_password = input("Enter the new password: ")

            new_data = {'username': new_username, 'password': new_password}
            admin_db.update_user_data(user_db, admin_password, user_id, new_data)

        elif admin_choice == "3":
            admin_password = input("Enter admin password: ")
            user_id = int(input("Enter the user ID to delete: "))
            admin_db.delete_user(user_db, admin_password, user_id)

        elif admin_choice == "4":
            admin_password = input("Enter admin password: ")
            reservation_id = int(input("Enter the reservation ID to update: "))
            new_date = input("Enter the new reservation date (YYYY-MM-DD): ")
            new_table_number = int(input("Enter the new table number: "))
            new_price = float(input("Enter the new reservation price: "))

            reservation_db.update_reservation(reservation_id, admin_password, new_date, new_table_number, new_price)
            print("Reservation data updated successfully!")

        elif admin_choice == "5":
            admin_password = input("Enter admin password: ")
            reservation_id = int(input("Enter the reservation ID to delete: "))
            reservation_db.delete_reservation(reservation_id)
            print("Reservation deleted successfully!")

        elif admin_choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
