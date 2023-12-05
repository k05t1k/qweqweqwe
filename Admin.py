import sqlite3

class AdminDatabase:
    def __init__(self, db_name="restaurant.db", admin_password="adminpass"):
        self.conn = sqlite3.connect(db_name)
        self.admin_password = admin_password

    def verify_admin_password(self, input_password):
        return input_password == self.admin_password

    def update_user_data(self, user_db, admin_password, user_id, new_data):
        if not self.verify_admin_password(admin_password):
            print("Incorrect admin password. Access denied.")
            return

        user_db.update_user_data(user_id, new_data)
        print(f"User data updated successfully for user ID {user_id}")

    def update_reservation(self, reservation_id, admin_password, date, table_number, price):
        if not self.verify_admin_password(admin_password):
            print("Incorrect admin password. Access denied.")
            return
        
        cursor = self.conn.cursor()
        cursor.execute('UPDATE reservations SET date=?, table_number=?, price=? WHERE id=?',
                    (date, table_number, price, reservation_id))
        self.conn.commit()

    def delete_user(self, user_db, admin_password, user_id):
        if not self.verify_admin_password(admin_password):
            print("Incorrect admin password. Access denied.")
            return

        user_db.delete_user(user_id)
        print(f"User with ID {user_id} deleted successfully.")

    def view_all_users(self, user_db, admin_password):
        if not self.verify_admin_password(admin_password):
            print("Incorrect admin password. Access denied.")
            return

        users = user_db.view_all_users()
        print("All Users:")
        for user in users:
            print(user)

    def close_connection(self):
        self.conn.close()
