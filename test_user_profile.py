from database.database import DatabaseManager


db = DatabaseManager()
db.create_tables()

profile = db.get_user_profile("Alice")

if profile:
    print(dict(profile))
else:
    print("User profile not found.")

db.close()