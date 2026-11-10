import json
import csv

GRADES = ("A", "B", "C", "D", "F")  # Tuple


class Student:
    def __init__(self, roll_no, name, grade, courses):
        self.roll_no = int(roll_no)
        self.name = name
        self.grade = grade
        self.courses = set(courses)  # Set

    def to_dict(self):
        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "grade": self.grade,
            "courses": list(self.courses),
        }


class StudentManager:
    def __init__(self):
        self.students = []  # List
        self.load_json()

    def load_json(self):
        try:
            with open("students.json", "r") as file:
                data = json.load(file)
                self.students = [
                    Student(d["roll_no"], d["name"], d["grade"], d["courses"])
                    for d in data
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            self.students = []

    def save_all(self):
        # 1. Save to JSON
        with open("students.json", "w") as j_file:
            json.dump([s.to_dict() for s in self.students], j_file, indent=2)

        # 2. Save to CSV
        with open("students.csv", "w", newline="") as c_file:
            fields = ["roll_no", "name", "grade", "courses"]
            writer = csv.DictWriter(c_file, fieldnames=fields)
            writer.writeheader()
            for s in self.students:
                writer.writerow({
                    "roll_no": s.roll_no,
                    "name": s.name,
                    "grade": s.grade,
                    "courses": ";".join(s.courses),  # Convert set to string for CSV
                })

    def add_student(self, roll_no, name, grade, courses):
        if grade not in GRADES:
            print(f"Invalid grade! Choose from {GRADES}")
            return
        self.students.append(Student(roll_no, name, grade, courses))
        self.save_all()
        print("Saved to both students.json and students.csv!")

    def view_all(self):
        for s in self.students:
            print(f"Roll: {s.roll_no} | Name: {s.name} | Grade: {s.grade} | Courses: {s.courses}")

    def delete_student(self, roll_no):
        self.students = [s for s in self.students if s.roll_no != roll_no]
        self.save_all()
        print("Deleted and updated JSON & CSV files!")


def main():
    manager = StudentManager()
    while True:
        print("\n1. Add  2. View  3. Delete  4. Exit")
        choice = input("Choose (1-4): ")
        try:
            if choice == "1":
                roll = int(input("Roll No: "))
                name = input("Name: ")
                grade = input("Grade (A-F): ").upper()
                courses = {c.strip() for c in input("Courses (comma-separated): ").split(",") if c.strip()}
                manager.add_student(roll, name, grade, courses)
            elif choice == "2":
                manager.view_all()
            elif choice == "3":
                manager.delete_student(int(input("Roll No to delete: ")))
            elif choice == "4":
                break
        except ValueError:
            print("Error: Roll No must be a number!")


if __name__ == "__main__":
    main()