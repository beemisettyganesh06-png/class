import pandas as pd

# User credentials stored in lists (integer IDs and passwords)
STUDENTS = [
    {"id": 1001, "password": 123456, "name": "Alice Johnson"},
    {"id": 1002, "password": 234567, "name": "Bob Smith"},
    {"id": 1003, "password": 345678, "name": "Charlie Brown"},
]

TEACHERS = [
    {"id": 2001, "password": 111111, "name": "Mr. Anderson"},
    {"id": 2002, "password": 222222, "name": "Ms. Williams"},
]

CSV_FILE = "student.csv"

def initialize_csv():
    """Create CSV file with sample data if it doesn't exist."""
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        data = {
            "student_id": [1001, 1002, 1003],
            "name": ["Alice Johnson", "Bob Smith", "Charlie Brown"],
            "fee_dues": [5000, 0, 2500],
            "attendance": [85, 92, 78],
            "marks": [88, 76, 91],
            "notification": ["Fee payment due", "None", "Parent meeting scheduled"]
        }
        df = pd.DataFrame(data)
        df.to_csv(CSV_FILE, index=False)
        print("Initialized student.csv with sample data.\n")

def load_data():
    """Load student data from CSV."""
    return pd.read_csv(CSV_FILE)

def save_data(df):
    """Save student data to CSV."""
    df.to_csv(CSV_FILE, index=False)

def authenticate_student(user_id, password):
    """Check student credentials."""
    for student in STUDENTS:
        if student["id"] == user_id and student["password"] == password:
            return student
    return None

def authenticate_teacher(user_id, password):
    """Check teacher credentials."""
    for teacher in TEACHERS:
        if teacher["id"] == user_id and teacher["password"] == password:
            return teacher
    return None

# ============ STUDENT FUNCTIONS ============
def student_menu(student_id):
    """Display student menu and handle choices."""
    while True:
        print("\n" + "="*40)
        print("       STUDENT PORTAL")
        print("="*40)
        print("1. View My Details")
        print("2. View Fee Dues")
        print("3. View Attendance")
        print("4. View Marks")
        print("5. View Notifications")
        print("6. Logout")
        
        choice = input("\nEnter choice (1-6): ").strip()
        df = load_data()
        student_data = df[df["student_id"] == student_id]
        
        if student_data.empty:
            print("Error: Your record not found in database!")
            continue
            
        row = student_data.iloc[0]
        
        if choice == "1":
            print("\n--- Your Details ---")
            print(f"Student ID: {row['student_id']}")
            print(f"Name: {row['name']}")
            print(f"Fee Dues: Rs.{row['fee_dues']}")
            print(f"Attendance: {row['attendance']}%")
            print(f"Marks: {row['marks']}")
            print(f"Notification: {row['notification']}")
        elif choice == "2":
            print(f"\nFee Dues: Rs.{row['fee_dues']}")
        elif choice == "3":
            print(f"\nAttendance: {row['attendance']}%")
        elif choice == "4":
            print(f"\nMarks: {row['marks']}")
        elif choice == "5":
            print(f"\nNotification: {row['notification']}")
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

# ============ TEACHER FUNCTIONS ============
def view_all_students():
    """Display all student records."""
    df = load_data()
    print("\n--- All Student Records ---")
    print(df.to_string(index=False))

def update_student_field(field_name):
    """Update a specific field for a student."""
    df = load_data()
    try:
        student_id = int(input("Enter Student ID: "))
    except ValueError:
        print("Invalid ID! Please enter a number.")
        return
    
    if student_id not in df["student_id"].values:
        print("Student not found!")
        return
    
    if field_name in ["fee_dues", "attendance", "marks"]:
        try:
            new_value = int(input(f"Enter new {field_name}: "))
        except ValueError:
            print("Invalid input! Please enter an integer.")
            return
    else:
        new_value = input(f"Enter new {field_name}: ").strip()
    
    df.loc[df["student_id"] == student_id, field_name] = new_value
    save_data(df)
    print(f"{field_name} updated successfully!")

def add_student():
    """Add a new student to the system."""
    df = load_data()
    
    try:
        student_id = int(input("Enter new Student ID: "))
    except ValueError:
        print("Invalid ID! Please enter a number.")
        return
        
    if student_id in df["student_id"].values:
        print("Student ID already exists!")
        return
    
    name = input("Enter student name: ").strip()
    try:
        fee_dues = int(input("Enter fee dues: "))
        attendance = int(input("Enter attendance (%): "))
        marks = int(input("Enter marks: "))
    except ValueError:
        print("Invalid input! Please enter integers.")
        return
    notification = input("Enter notification (or 'None'): ").strip()
    
    new_student = {
        "student_id": student_id,
        "name": name,
        "fee_dues": fee_dues,
        "attendance": attendance,
        "marks": marks,
        "notification": notification
    }
    
    df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
    save_data(df)
    
    # Add to credentials list
    try:
        password = int(input("Set password for student (numbers only): "))
    except ValueError:
        print("Invalid password! Using default 000000.")
        password = 000000
    STUDENTS.append({"id": student_id, "password": password, "name": name})
    print(f"Student {name} added successfully!")

def delete_student():
    """Delete a student from the system."""
    df = load_data()
    try:
        student_id = int(input("Enter Student ID to delete: "))
    except ValueError:
        print("Invalid ID! Please enter a number.")
        return
    
    if student_id not in df["student_id"].values:
        print("Student not found!")
        return
    
    confirm = input(f"Are you sure you want to delete {student_id}? (yes/no): ").strip().lower()
    if confirm == "yes":
        df = df[df["student_id"] != student_id]
        save_data(df)
        
        # Remove from credentials list
        for i, student in enumerate(STUDENTS):
            if student["id"] == student_id:
                STUDENTS.pop(i)
                break
        print("Student deleted successfully!")
    else:
        print("Deletion cancelled.")

def teacher_menu(teacher_name):
    """Display teacher menu and handle choices."""
    while True:
        print("\n" + "="*40)
        print(f"    TEACHER PORTAL - {teacher_name}")
        print("="*40)
        print("1. View All Students")
        print("2. Update Fee Dues")
        print("3. Update Attendance")
        print("4. Update Marks")
        print("5. Update Notification")
        print("6. Add New Student")
        print("7. Delete Student")
        print("8. Logout")
        
        choice = input("\nEnter choice (1-8): ").strip()
        
        if choice == "1":
            view_all_students()
        elif choice == "2":
            update_student_field("fee_dues")
        elif choice == "3":
            update_student_field("attendance")
        elif choice == "4":
            update_student_field("marks")
        elif choice == "5":
            update_student_field("notification")
        elif choice == "6":
            add_student()
        elif choice == "7":
            delete_student()
        elif choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

# ============ MAIN PROGRAM ============
def main():
    """Main entry point of the program."""
    initialize_csv()
    
    while True:
        print("\n" + "="*40)
        print("    WELCOME TO STUDENT PORTAL")
        print("="*40)
        print("1. Login as Student")
        print("2. Login as Teacher")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            try:
                user_id = int(input("Enter Student ID: "))
                password = int(input("Enter Password: "))
            except ValueError:
                print("Invalid input! ID and password must be numbers.")
                continue
            student = authenticate_student(user_id, password)
            
            if student:
                print(f"\nWelcome, {student['name']}!")
                student_menu(user_id)
            else:
                print("Invalid credentials!")
                
        elif choice == "2":
            try:
                user_id = int(input("Enter Teacher ID: "))
                password = int(input("Enter Password: "))
            except ValueError:
                print("Invalid input! ID and password must be numbers.")
                continue
            teacher = authenticate_teacher(user_id, password)
            
            if teacher:
                print(f"\nWelcome, {teacher['name']}!")
                teacher_menu(teacher['name'])
            else:
                print("Invalid credentials!")
                
        elif choice == "3":
            print("Thank you for using Student Portal. Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
