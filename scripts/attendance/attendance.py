import pandas as pd
import matplotlib.pyplot as plt

from schemas import AttendanceSchema


def graph_attendance(file_path):
    """
    Graphs the timeline of student attendance over the semester.
    :param file_path: the path to the attendance csv.
    """
    attendance = pd.read_csv(file_path)
    attendance = attendance.dropna(subset=[AttendanceSchema.NUMBER_OF_STUDENTS]).drop(
        columns=[AttendanceSchema.COMMENTS])
    wednesday_attendance = attendance[attendance[AttendanceSchema.DAY].str.contains(AttendanceSchema.WEDNESDAY) == True]
    friday_attendance = attendance[attendance[AttendanceSchema.DAY].str.contains(AttendanceSchema.FRIDAY) == True]

    # Wednesday Graph
    plot_attendance(wednesday_attendance, AttendanceSchema.WEDNESDAY)

    # Friday Graph
    plot_attendance(friday_attendance, AttendanceSchema.FRIDAY)


def plot_attendance(attendance, day):
    graph = attendance.plot.line(x=AttendanceSchema.DAY, y=AttendanceSchema.NUMBER_OF_STUDENTS)
    graph.set_xticks(range(len(attendance.index)))
    graph.set_xticklabels(attendance[AttendanceSchema.DAY].tolist())
    plt.xticks(rotation=270)
    plt.xlabel('Date')
    plt.ylabel('# of Students')
    plt.title(f'# of Students that Attended Class on {day}')
    plt.tight_layout()
    plt.show()
