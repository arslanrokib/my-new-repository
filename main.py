import json


class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        return f"Name: {self.name}, Age: {self.age}, Address: {self.address}"


class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def display_student_info(self):
        course_list = ", ".join(self.courses)
        grades_list = str(self.grades)
        return (f"Student Information:\n"
                f"Name: {self.name}\n"
                f"ID: {self.student_id}\n"
                f"Age: {self.age}\n"
                f"Address: {self.address}\n"
                f"Enrolled Courses: {course_list}\n"
                f"Grades: {grades_list}")


class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)
            student.enroll_course(self.course_name)

    def display_course_info(self):
        student_list = ", ".join([student.name for student in self.students])
        return (f"Course Information:\n"
                f"Course Name: {self.course_name}\n"
                f"Code: {self.course_code}\n"
                f"Instructor: {self.instructor}\n"
                f"Enrolled Students: {student_list}")


class SystemHandler:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self, name, age, address, student_id):
        if student_id not in self.students:
            new_student = Student(name, age, address, student_id)
            self.students[student_id] = new_student
            print(f"Student {name} (ID: {student_id}) added successfully.")
        else:
            print("Error: Student ID already exists.")

    def add_course(self, course_name, course_code, instructor):
        if course_code not in self.courses:
            new_course = Course(course_name, course_code, instructor)
            self.courses[course_code] = new_course
            print(f"Course {course_name} (Code: {
                  course_code}) created with instructor {instructor}.")
        else:
            print("Error: Course code already exists.")

    def enroll_in_course(self, student_id, course_code):
        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            course = self.courses[course_code]  
            course.add_student(student)
            print(f"Student {student.name} (ID: {student_id}) enrolled in {
                  course.course_name} (Code: {course_code}).")
        else:
            print("Error: Invalid student ID or course code.")

    def add_grade(self, student_id, course_code, grade):
        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            if course_code in student.courses:
                student.add_grade(course_code, grade)
                print(f"Grade {grade} added for {
                      student.name} in {course_code}.")
            else:
                print("Error: Student is not enrolled in this course.")
        else:
            print("Error: Invalid student ID or course code.")

    def display_student_details(self, student_id):
        if student_id in self.students:
            print(self.students[student_id].display_student_info())
        else:
            print("Error: Invalid student ID.")

    def display_course_details(self, course_code):
        if course_code in self.courses:
            print(self.courses[course_code].display_course_info())
        else:
            print("Error: Invalid course code.")

    def save_data(self, filename='data.json'):
        data = {
            "students": {student_id: vars(student) for student_id, student in self.students.items()},
            "courses": {course_code: vars(course) for course_code, course in self.courses.items()},
        }
        with open(filename, 'a') as f:
            json.dump(filename, f)
        print("All student and course data saved successfully.")

    def load_data(self, filename='data.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.students = {student_id: Student(
                    **student) for student_id, student in data['students'].items()}
                self.courses = {course_code: Course(
                    **course) for course_code, course in data['courses'].items()}
                for course_code, course in self.courses.items():
                    for student_id in course['students']:
                        if student_id in self.students:
                            course.add_student(self.students[student_id])
                print("Data loaded successfully.")
        except FileNotFoundError:
            print("Error: Data file not found.")
        except json.JSONDecodeError:
            print("Error: Data file is corrupted.")


def main():
    handle = SystemHandler()

    print(
        "---------------------------------------------\n"
        "+ Wellcome to the student management system +\n"
        "---------------------------------------------")
    while True:
        print(
            "\n1. Add Student\n2. Add New Course\n3. Enroll Student in Course\n4. Add Grade for Student\n"
            "5. Display Student Details\n6. Display Course Details\n7. Save Data to File\n8. Load Data from File\n0. Exit\n"
            )

        option_choice = input("Select an Option: ")

        if option_choice == '1':
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            address = input("Enter Address: ")
            student_id = input("Enter Student ID: ")
            handle.add_student(name, age, address, student_id)

        elif option_choice == '2':
            course_name = input("Enter Course Name: ")
            course_code = input("Enter Course Code: ")
            instructor = input("Enter Instructor Name: ")
            handle.add_course(course_name, course_code, instructor)

        elif option_choice == '3':
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            handle.enroll_in_course(student_id, course_code)

        elif option_choice == '4':
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            grade = input("Enter Grade: ")
            handle.add_grade(student_id, course_code, grade)

        elif option_choice == '5':
            student_id = input("Enter Student ID: ")
            handle.display_student_details(student_id)

        elif option_choice == '6':
            course_code = input("Enter Course Code: ")
            handle.display_course_details(course_code)

        elif option_choice == '7':
            handle.save_data()

        elif option_choice == '8':
            handle.load_data()

        elif option_choice == '0':
            print("System will be terminated, GOOD BYE>>>")
            break
        
        else: print("Invalid Input, Please Try Again...")


if __name__ == "__main__":
    main()
