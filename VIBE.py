# Megan Nelson
# CIS261
# WK10 Vibe Coding
# Student Grade Calculator

import os
from datetime import datetime


class Student:
    """Represents a student with test scores and calculated grade."""
    
    def __init__(self, name, student_id, test1, test2, test3):
        """Initialize a student with name, ID, and three test scores."""
        self.name = name
        self.student_id = student_id
        self.test1 = test1
        self.test2 = test2
        self.test3 = test3
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()
    
    def calculate_average(self):
        """Calculate the average of the three test scores."""
        return (self.test1 + self.test2 + self.test3) / 3
    
    def calculate_grade(self):
        """Calculate letter grade based on average score."""
        if self.average >= 90:
            return 'A'
        elif self.average >= 80:
            return 'B'
        elif self.average >= 70:
            return 'C'
        elif self.average >= 60:
            return 'D'
        else:
            return 'F'
    
    def to_file_format(self):
        """Return student data in pipe-delimited format."""
        return f"{self.name}|{self.student_id}|{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}"
    
    def __str__(self):
        """Return formatted string representation of student."""
        return f"{self.name:20} | {self.student_id:10} | {self.test1:6.2f} | {self.test2:6.2f} | {self.test3:6.2f} | {self.average:6.2f} | {self.grade:1}"


class GradeManager:
    """Manages student records and related operations."""
    
    FILE_NAME = "student_grades.txt"
    
    def __init__(self):
        """Initialize the grade manager and load existing records."""
        self.students = []
        self.load_students()
    
    def add_student(self):
        """Prompt user to add a new student record."""
        try:
            print("\n" + "="*70)
            print("ADD NEW STUDENT")
            print("="*70)
            
            name = input("Enter student name: ").strip()
            if not name:
                print("Error: Name cannot be empty.")
                return
            
            student_id = input("Enter student ID: ").strip()
            if not student_id:
                print("Error: Student ID cannot be empty.")
                return
            
            # Check for duplicate ID
            if any(s.student_id == student_id for s in self.students):
                print(f"Error: Student ID '{student_id}' already exists.")
                return
            
            # Get test scores
            test1 = self.get_valid_score("Enter Test 1 score (0-100): ")
            test2 = self.get_valid_score("Enter Test 2 score (0-100): ")
            test3 = self.get_valid_score("Enter Test 3 score (0-100): ")
            
            # Create and add student
            student = Student(name, student_id, test1, test2, test3)
            self.students.append(student)
            
            print(f"\n✓ Student '{name}' added successfully!")
            print(f"  Average: {student.average:.2f}")
            print(f"  Grade: {student.grade}")
            
            # Auto-save
            self.save_students()
            
        except ValueError as e:
            print(f"Error: Invalid input. {e}")
    
    def get_valid_score(self, prompt):
        """Get a valid test score from user (0-100)."""
        while True:
            try:
                score = float(input(prompt))
                if 0 <= score <= 100:
                    return score
                else:
                    print("Error: Score must be between 0 and 100.")
            except ValueError:
                print("Error: Please enter a valid number.")
    
    def display_all_students(self):
        """Display all students in a formatted table."""
        if not self.students:
            print("\nNo students in the system yet.")
            return
        
        print("\n" + "="*100)
        print("ALL STUDENTS")
        print("="*100)
        print(f"{'Name':20} | {'ID':10} | {'Test1':>6} | {'Test2':>6} | {'Test3':>6} | {'Average':>6} | Grade")
        print("-"*100)
        
        for student in self.students:
            print(student)
        
        print("="*100)
    
    def display_class_statistics(self):
        """Display class statistics."""
        if not self.students:
            print("\nNo students in the system yet.")
            return
        
        averages = [s.average for s in self.students]
        class_average = sum(averages) / len(averages)
        highest = max(averages)
        lowest = min(averages)
        
        # Find students with highest and lowest averages
        highest_student = next(s for s in self.students if s.average == highest)
        lowest_student = next(s for s in self.students if s.average == lowest)
        
        print("\n" + "="*70)
        print("CLASS STATISTICS")
        print("="*70)
        print(f"Total Students: {len(self.students)}")
        print(f"Class Average: {class_average:.2f}")
        print(f"Highest Average: {highest:.2f} ({highest_student.name})")
        print(f"Lowest Average: {lowest:.2f} ({lowest_student.name})")
        print("="*70)
    
    def search_student(self):
        """Search for a student by name (case-insensitive)."""
        if not self.students:
            print("\nNo students in the system yet.")
            return
        
        search_name = input("\nEnter student name to search: ").strip().lower()
        
        matching_students = [s for s in self.students if search_name in s.name.lower()]
        
        if not matching_students:
            print(f"No students found matching '{search_name}'.")
            return
        
        print("\n" + "="*100)
        print("SEARCH RESULTS")
        print("="*100)
        print(f"{'Name':20} | {'ID':10} | {'Test1':>6} | {'Test2':>6} | {'Test3':>6} | {'Average':>6} | Grade")
        print("-"*100)
        
        for student in matching_students:
            print(student)
        
        print("="*100)
    
    def save_students(self):
        """Save all student records to file in pipe-delimited format."""
        try:
            with open(self.FILE_NAME, 'w') as f:
                for student in self.students:
                    f.write(student.to_file_format() + '\n')
            print(f"✓ Records saved to '{self.FILE_NAME}'")
        except IOError as e:
            print(f"Error saving file: {e}")
    
    def load_students(self):
        """Load student records from file."""
        if not os.path.exists(self.FILE_NAME):
            return
        
        try:
            with open(self.FILE_NAME, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('|')
                        if len(parts) == 7:
                            name, student_id, test1, test2, test3, average, grade = parts
                            try:
                                student = Student(name, student_id, float(test1), 
                                                 float(test2), float(test3))
                                self.students.append(student)
                            except ValueError:
                                print(f"Warning: Skipping invalid record: {line}")
            
            if self.students:
                print(f"✓ Loaded {len(self.students)} student record(s) from '{self.FILE_NAME}'")
        
        except IOError as e:
            print(f"Error loading file: {e}")
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*70)
        print("STUDENT GRADE CALCULATOR")
        print("="*70)
        print("1. Add new student")
        print("2. Display all students")
        print("3. Display class statistics")
        print("4. Search for a student")
        print("5. Save records to file")
        print("6. Exit (or press ESC)")
        print("="*70)
    
    def run(self):
        """Run the main program loop."""
        print("\n" + "="*70)
        print("Welcome to Student Grade Calculator")
        print("="*70)
        
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.display_all_students()
            elif choice == '3':
                self.display_class_statistics()
            elif choice == '4':
                self.search_student()
            elif choice == '5':
                self.save_students()
            elif choice == '6':
                self.exit_program()
            elif choice.lower() == 'esc' or choice == '\x1b':
                self.exit_program()
            else:
                print("Invalid choice. Please enter 1-6.")
    
    def exit_program(self):
        """Exit the program after saving."""
        print("\n" + "="*70)
        self.save_students()
        print("Thank you for using Student Grade Calculator!")
        print("="*70 + "\n")
        exit()


def main():
    """Main entry point for the program."""
    manager = GradeManager()
    manager.run()


if __name__ == "__main__":
    main()