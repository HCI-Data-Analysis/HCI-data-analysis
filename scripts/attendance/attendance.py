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
    graph = attendance.plot.line(x=AttendanceSchema.DAY, y=AttendanceSchema.NUMBER_OF_STUDENTS)
    graph.set_xticks(range(len(attendance.index)))
    graph.set_xticklabels(attendance[AttendanceSchema.DAY].tolist())
    plt.xticks(rotation=270)
    plt.tight_layout()
    plt.show()
