import sqlite3

# Connect to the database file
conn = sqlite3.connect('pharmassist.db')

# Create a cursor object to execute SQL commands
c = conn.cursor()

# Create Table
c.execute("""
          CREATE TABLE if not exists pharmassist ( 
            product_name text,
            quantity integer,
            description text,
            manufacturing_date text,
            expiry_date text,
            item_id integer
          )
""")
conn.commit()
# Define a list of medicine data
data = [
    ["Paracetamol", 100, "Pain reliever", "2023-05-15", "2024-05-15", "PID001"],
    ["Amoxicillin", 50, "Antibiotic", "2023-06-20", "2024-06-20", "PID002"],
    ["Loratadine", 80, "Antihistamine", "2023-04-10", "2024-04-10", "PID003"],
    ["Omeprazole", 60, "Acid reducer", "2023-07-01", "2024-07-01", "PID004"],
    ["Ibuprofen", 120, "Pain reliever", "2023-08-05", "2024-08-05", "PID005"],
    ["Cetirizine", 70, "Antihistamine", "2023-03-25", "2024-03-25", "PID006"],
    ["Diazepam", 40, "Anxiolytic", "2023-09-15", "2024-09-15", "PID007"],
    ["Simvastatin", 90, "Cholesterol-lowering", "2023-02-10", "2024-02-10", "PID008"],
    ["Metformin", 55, "Antidiabetic", "2023-10-20", "2024-10-20", "PID009"],
    ["Atorvastatin", 85, "Cholesterol-lowering", "2023-01-15", "2024-01-15", "PID010"],
    ["Prednisone", 65, "Corticosteroid", "2023-11-30", "2024-11-30", "PID011"],
    ["Losartan", 75, "Antihypertensive", "2023-12-25", "2024-12-25", "PID012"],
    ["Metoprolol", 95, "Beta blocker", "2023-07-10", "2024-07-10", "PID013"],
    ["Warfarin", 110, "Anticoagulant", "2023-06-05", "2024-06-05", "PID014"],
    ["Levothyroxine", 105, "Thyroid hormone", "2023-05-01", "2024-05-01", "PID015"],
    ["Venlafaxine", 125, "Antidepressant", "2023-04-15", "2024-04-15", "PID016"],
    ["Fluoxetine", 80, "Antidepressant", "2023-03-20", "2024-03-20", "PID017"],
    ["Cephalexin", 70, "Antibiotic", "2023-02-05", "2024-02-05", "PID018"],
    ["Hydrochlorothiazide", 60, "Diuretic", "2023-01-10", "2024-01-10", "PID019"],
    ["Furosemide", 50, "Diuretic", "2023-12-15", "2024-12-15", "PID020"],
    ["Bupropion", 45, "Antidepressant", "2023-11-20", "2024-11-20", "PID021"],
    ["Metronidazole", 40, "Antibiotic", "2023-10-25", "2024-10-25", "PID022"],
    ["Naproxen", 35, "Pain reliever", "2023-09-30", "2024-09-30", "PID023"],
    ["Trazodone", 30, "Antidepressant", "2023-08-05", "2024-08-05", "PID024"],
    ["Quetiapine", 25, "Antipsychotic", "2023-07-10", "2024-07-10", "PID025"],
    ["Amitriptyline", 20, "Antidepressant", "2023-06-15", "2024-06-15", "PID026"],
    ["Guaifenesin", 15, "Expectorant", "2023-05-20", "2024-05-20", "PID027"],
    ["Lisinopril", 10, "Antihypertensive", "2023-04-25", "2024-04-25", "PID028"],
    ["Citalopram", 5, "Antidepressant", "2023-03-01", "2024-03-01", "PID029"],
    ["Montelukast", 120, "Antiasthmatic", "2023-02-15", "2024-02-15", "PID030"],
    # Add more entries as needed
]

# Printing each medicine's data
for medicine in data:
    print("Product Name:", medicine[0])
    print("Quantity:", medicine[1])
    print("Short Description:", medicine[2])
    print("Manufacturing Date:", medicine[3])
    print("Expiry Date:", medicine[4])
    print("Item ID:", medicine[5])
    print()  # Empty line for separation


# Add dummy data to table
for record in data:
    c.execute("INSERT INTO pharmassist VALUES(:product_name, :quantity_integer, :description, :manufacturing_date, :expiry_date, :item_id )",
              {
                   'product_name': record[0],
                   'quantity_integer': record[1],
                  'description': record[2],
                   'manufacturing_date': record[3],
                   'expiry_date': record[4],
                   'item_id': record[5]
               }
               )
    
# Commit the changes
conn.commit()

# Close 
conn.close()

def query_database():
    # Connect to the database file
    conn = sqlite3.connect('pharmassist.db')

    # Create a cursor object to execute SQL commands
    c = conn.cursor()

    c.execute("SELECT * FROM pharmassist")
    records = c.fetchall()
    print(records)
    conn.commit

query_database()