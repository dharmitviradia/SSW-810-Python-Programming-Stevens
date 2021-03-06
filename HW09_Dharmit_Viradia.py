""" Creating a Data Repository for University """

import os
from collections import defaultdict
from prettytable import PrettyTable
from typing import Dict, DefaultDict, Tuple, List, Iterator
from HW08_Dharmit_Viradia import file_reader


class Repository:
    "Student and Instructor repository"

    def __init__(self, path: str, tables: bool = True) -> None:
        self._path: str = path
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()

        try:
            self._get_students(os.path.join(self._path, 'students.txt'))
            self._get_instructors(os.path.join(self._path, 'instructors.txt'))
            self._get_grades(os.path.join(self._path, 'grades.txt'))

        except (FileNotFoundError, ValueError) as e:
            print(e)

        else:
            if tables:
                print("\nStudent Table ")
                self.student_table()
                print("\nInstructor Table ")
                self.instructor_table()


    def _get_students(self, path) -> None:
        """ Student detail are read using file reading gen and added to dictionary """
        for cwid, name, major in file_reader(path, 3, sep='\t', header=False):
            self._students[cwid] = Student(cwid, name, major)

    def _get_instructors(self, path) -> None:
        """ Instructor detail are read using file reading gen and added to dictionary """
        for cwid, name, dept in file_reader(path, 3, sep='\t', header=False):
            self._instructors[cwid] = Instructor(cwid, name, dept)

    def _get_grades(self, path) -> None:
        """Grades are read using file reading gen and assigned to student and instructor """
        for std_cwid, course, grade, instructor_cwid in file_reader(path, 4, sep='\t', header=False):
            if std_cwid in self._students:
                self._students[std_cwid].add_course(course, grade)
            else:
                print(f'Grades for student is {std_cwid}')

            if instructor_cwid in self._instructors:
                self._instructors[instructor_cwid].add_student(course)
            else:
                print(f'Grades for instructor is {instructor_cwid}')

    def student_table(self) -> None:
        """ Student table """
        table = PrettyTable(field_names=Student.FIELD_NAMES)
        for student in self._students.values():
            table.add_row(student.info())
        print(table)

    def instructor_table(self) -> None:
        """ Instructor table """
        table = PrettyTable(field_names=Instructor.FIELD_NAMES)
        for instructor in self._instructors.values():
            for row in instructor.info():
                table.add_row(row)
        print(table)


class Student:
    """Student Class to store student data"""
    FIELD_NAMES = ['CWID', 'Name', 'Completed Courses']

    def __init__(self, cwid: str, name: str, major: str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()

    def add_course(self, course: str, grade: str) -> None:
        """ Adding course with grade """
        self._courses[course] = grade

    def info(self) -> Tuple[str, str, List[str]]:
        """ return a list of information needed for pretty table """
        return [self._cwid, self._name, sorted(self._courses.keys())]


class Instructor:
    """ Instructor class """
    FIELD_NAMES = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid: str, name: str, dept: str) -> None:

        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int)

    def add_student(self, course: str) -> None:
        """ Number of students taking course with Instructor """
        self._courses[course] += 1

    def info(self) -> Iterator[Tuple[str, str, str, str, int]]:
        """ Yield the row """
        for course, count in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, count]


def main():
    Repository('HW09_Test')


if __name__ == '__main__':
    main()
