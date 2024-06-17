import json
import os
import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

from gui import Ui_MainWindow


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dataset_AllStudentInfo = dict()
        self.dataset_allCourseInfo = dict()
        self.dataset_all_attendance = dict(dict(dict()))
        self.load_dataset()

        # buttons
        self.ui.pushButton_AddNewStudent.clicked.connect(self.add_student)
        self.ui.Button_AddNewCourse.clicked.connect(self.add_new_course)
        self.ui.Button_Present.clicked.connect(self.attendance_present)
        self.ui.Button_Absent.clicked.connect(self.attendance_absent)

        # line edits
        self.ui.lineEdit_NewStudentID.returnPressed.connect(self.ui.lineEdit_NewStudentName.setFocus)
        self.ui.lineEdit_NewStudentID.editingFinished.connect(self.is_ok_student)
        self.ui.lineEdit_NewStudentName.returnPressed.connect(self.ui.lineEdit_Address.setFocus)
        self.ui.lineEdit_Address.returnPressed.connect(self.ui.pushButton_AddNewStudent.click)

        self.ui.lineEdit_NewCourseCode.returnPressed.connect(self.ui.lineEdit_NewCourseName.setFocus)
        self.ui.lineEdit_NewCourseCode.editingFinished.connect(self.is_ok_course)
        self.ui.lineEdit_NewCourseName.returnPressed.connect(self.ui.lineEdit_NewInstructor.setFocus)
        self.ui.lineEdit_NewInstructor.returnPressed.connect(self.ui.lineEdit_NewDepartment.setFocus)
        self.ui.lineEdit_NewDepartment.returnPressed.connect(self.ui.Button_AddNewCourse.click)

        self.ui.table_allCourse.setColumnWidth(0, 90)
        self.ui.table_allCourse.setColumnWidth(3, 90)
        self.ui.tableWidget_allStudents.setColumnWidth(1, 140)

    # loading database
    def load_dataset(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        self.load_dataset_student()
        self.load_dataset_course()
        self.load_dataset_attendance()
        self.update_student_table()
        self.update_course_table()
        self.load_combobox_items()

    def load_dataset_student(self):
        try:
            with open('data/dataset_studentInfo.json', 'r') as f:
                self.dataset_AllStudentInfo = json.load(f)
        except FileNotFoundError:
            f = open('data/dataset_studentInfo.json', 'w')
            f.close()
        except json.decoder.JSONDecodeError:
            return

    def load_dataset_course(self):
        try:
            with open('data/allCourse.json', 'r') as f:
                self.dataset_allCourseInfo = json.load(f)
        except FileNotFoundError:
            f = open('data/allCourse.json', 'w')
            f.close()
        except json.decoder.JSONDecodeError:
            return

    def load_dataset_attendance(self):
        try:
            with open('data/dataset_all_attendance.json', 'r') as f:
                self.dataset_all_attendance = json.load(f)
        except FileNotFoundError:
            f = open('data/dataset_all_attendance.json', 'w')
            f.close()
        except json.decoder.JSONDecodeError:
            return

    def load_combobox_items(self):
        self.ui.comboBox_StudentID.addItems(self.dataset_AllStudentInfo.keys())
        self.ui.comboBox_CourseCode.addItems(self.dataset_allCourseInfo.keys())

    '''
                *** Attendance -> start ***
    '''
    def attendance_present(self):
        self.save_attendance("P")

    def attendance_absent(self):
        self.save_attendance("A")

    def save_attendance(self, val):
        student_id = self.ui.comboBox_StudentID.currentText()
        course_code = self.ui.comboBox_CourseCode.currentText()
        date = self.ui.lineEdit_Date.text()

        if student_id == "" or course_code == "":
            self.ui.label_attendance_alarm.clear()
            self.ui.label_attendance_alarm.setText("!! ID or course should not be empty !!")
            return
        else:
            self.ui.label_attendance_alarm.clear()

        combo_item_no = self.ui.comboBox_StudentID.currentIndex()
        if course_code not in self.dataset_all_attendance:
            self.dataset_all_attendance[course_code] = {}
        if student_id not in self.dataset_all_attendance[course_code]:
            self.dataset_all_attendance[course_code][student_id] = {}
        self.dataset_all_attendance[course_code][student_id][date] = val
        # self.dataset_all_attendance.setdefault(course_code, {}).setdefault(student_id, {})[date] = val
        with open('data/dataset_all_attendance.json', 'w') as f:
            json.dump(self.dataset_all_attendance, f)
        if self.ui.comboBox_StudentID.count() - 1 == combo_item_no:
            self.ui.comboBox_StudentID.setCurrentIndex(0)
        else:
            self.ui.comboBox_StudentID.setCurrentIndex(combo_item_no + 1)

    '''
            *** end ***
    '''

    '''
                *** student info -> start *** 
    '''
    def add_student(self):

        student_id = self.ui.lineEdit_NewStudentID.text()
        student_name = self.ui.lineEdit_NewStudentName.text()
        student_address = self.ui.lineEdit_Address.text()

        if student_id == '' or student_name == '' or student_address == '':
            self.ui.label_alarm_student.setText("!! Please fill up all box !!")
            return

        self.dataset_AllStudentInfo[student_id] = [student_name, student_address]
        self.save_student_dataset()
        self.update_student_table()
        self.ui.comboBox_StudentID.addItem(student_id)

        self.ui.lineEdit_NewStudentID.clear()
        self.ui.lineEdit_NewStudentName.clear()
        self.ui.lineEdit_Address.clear()
        self.ui.label_alarm_student.clear()
        self.ui.lineEdit_NewStudentID.setFocus()

    def update_student_table(self):
        rows_needed = len(self.dataset_AllStudentInfo)
        self.ui.tableWidget_allStudents.setRowCount(rows_needed)
        if rows_needed > 7:
            self.ui.tableWidget_allStudents.setColumnWidth(2, 175)
        else:
            self.ui.tableWidget_allStudents.setColumnWidth(2, 201)
        current_row = 0
        for Id, name in self.dataset_AllStudentInfo.items():
            self.ui.tableWidget_allStudents.setItem(current_row, 0, QTableWidgetItem(Id))
            self.ui.tableWidget_allStudents.setItem(current_row, 1, QTableWidgetItem(name[0]))
            self.ui.tableWidget_allStudents.setItem(current_row, 2, QTableWidgetItem(name[1]))
            current_row += 1

    def save_student_dataset(self):
        with open('data/dataset_studentInfo.json', 'w') as f:
            json.dump(self.dataset_AllStudentInfo, f)

    def is_ok_student(self):
        student_id = self.ui.lineEdit_NewStudentID.text()

        if student_id in self.dataset_AllStudentInfo.keys():
            self.ui.pushButton_AddNewStudent.blockSignals(True)
            self.ui.label_alarm_student.setText("!! Duplicate ID !!")
            self.ui.lineEdit_NewStudentID.setFocus()
        else:
            self.ui.pushButton_AddNewStudent.blockSignals(False)
            self.ui.label_alarm_student.clear()

    '''
            *** end ***
    '''

    '''
            *** course info -> start ***
    '''

    def add_new_course(self):

        course_code = self.ui.lineEdit_NewCourseCode.text()
        course_name = self.ui.lineEdit_NewCourseName.text()
        instructor = self.ui.lineEdit_NewInstructor.text()
        department = self.ui.lineEdit_NewDepartment.text()

        if course_code == '' or course_name == '' or instructor == '' or department == '':
            self.ui.label_alarm_course.setText("!! Please fill up all box !!")
            return

        self.dataset_allCourseInfo[course_code] = [course_code, course_name, instructor, department]
        self.save_course_database()
        self.update_course_table()
        self.ui.comboBox_CourseCode.addItem(course_code)

        self.ui.lineEdit_NewCourseCode.clear()
        self.ui.lineEdit_NewCourseName.clear()
        self.ui.lineEdit_NewInstructor.clear()
        self.ui.lineEdit_NewDepartment.clear()
        self.ui.label_alarm_course.clear()
        self.ui.lineEdit_NewCourseCode.setFocus()

    def save_course_database(self):
        with open('data/allCourse.json', 'w') as f:
            json.dump(self.dataset_allCourseInfo, f)

    def update_course_table(self):
        rows = len(self.dataset_allCourseInfo)
        self.ui.table_allCourse.setRowCount(rows)
        if rows <= 7:
            self.ui.table_allCourse.setColumnWidth(1, 161)
        else:
            self.ui.table_allCourse.setColumnWidth(1, 135)
        row = 0
        for Id, name in self.dataset_allCourseInfo.items():
            self.ui.table_allCourse.setItem(row, 0, QTableWidgetItem(name[0]))
            self.ui.table_allCourse.setItem(row, 1, QTableWidgetItem(name[1]))
            self.ui.table_allCourse.setItem(row, 2, QTableWidgetItem(name[2]))
            self.ui.table_allCourse.setItem(row, 3, QTableWidgetItem(name[3]))
            row += 1

    def is_ok_course(self):
        course_code = self.ui.lineEdit_NewCourseCode.text()
        if course_code in self.dataset_allCourseInfo.keys():
            self.ui.Button_AddNewCourse.blockSignals(True)
            self.ui.label_alarm_course.setText("!! Duplicate ID !!")
            self.ui.lineEdit_NewCourseCode.setFocus()
        else:
            self.ui.Button_AddNewCourse.blockSignals(False)
            self.ui.label_alarm_course.clear()

    """ -> end """


app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec())
