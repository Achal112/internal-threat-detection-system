from database.database import DatabaseManager

db = DatabaseManager()

db.create_tables()

employees = [

    ("Alice","09:00","18:00",0,20,45,"HR"),

    ("Bob","09:00","18:00",0,35,60,"Finance"),

    ("Charlie","00:00","23:59",1,150,220,"IT"),

    ("David","09:00","18:00",0,15,35,"Engineering")

]

for employee in employees:

    db.insert_baseline(*employee)

db.close()

print("Baseline inserted successfully.")