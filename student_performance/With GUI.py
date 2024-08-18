import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import *
from tkinter import messagebox

# Load the data and train the model
data = pd.read_excel("student_data.xlsx")
data['Total_Marks'] = data[
    ['IA 1', 'IA 2', 'IA3', 'External Marks', 'Seminar Marks', 'Mock Test Results', 'Extra Curriculam  Marks',
     'Attendance']].sum(axis=1)
X = data.drop(['USN', 'Name', 'DOB', 'Department', 'Total_Marks'], axis=1)
y = data['Total_Marks']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)


# Function to calculate and display results
def calculate_results():
    usn = usn_entry.get()
    global candidate_data
    candidate_data = data[data['USN'] == usn]
    candidate_features = candidate_data.drop(['USN', 'Name', 'DOB', 'Department', 'Total_Marks'], axis=1)
    predicted_total_marks = model.predict(candidate_features)[0]

    data['Predicted_Total_Marks'] = model.predict(X)
    data_sorted = data.sort_values(by='Predicted_Total_Marks', ascending=False).reset_index(drop=True)
    rank = data_sorted[data_sorted['USN'] == usn].index[0] + 1

    subject_marks = candidate_data[
        ['IA 1', 'IA 2', 'IA3', 'External Marks', 'Seminar Marks', 'Mock Test Results', 'Extra Curriculam  Marks',
         'Attendance']]
    min_subject = subject_marks.idxmin(axis=1).values[0]

    max_marks_per_subject = 100
    total_marks_obtained = sum(candidate_data[
                                   ['IA 1', 'IA 2', 'IA3', 'External Marks', 'Seminar Marks', 'Mock Test Results',
                                    'Extra Curriculam  Marks']].values[0])
    total_possible_marks = max_marks_per_subject * 7
    global overall_performance
    overall_performance = (total_marks_obtained / total_possible_marks) * 100



    # Display results
    rank_label.config(text="Rank of this student: " + str(rank))
    details_label.config(
        text="Candidate Details:\n" + candidate_data[['Name', 'DOB', 'Department', 'Attendance']].to_string(
            index=False))
    improvement_label.config(text="Area of improvement: " + min_subject)

    a_label.config(text ="Predicted Overall Performance: " + str(round(overall_performance)))


def display_graphs():
    var = int(actual_entry.get())
    performance_difference = var - int(overall_performance)

    difference_label.config(
        text="Difference between Actual and Predicted Performance: " + str(round(performance_difference, 2)))


    # Generate and display graphs
    subjects = ['IA 1', 'IA 2', 'IA3', 'External Marks', 'Seminar Marks', 'Mock Test Results',
                'Extra Curriculam  Marks', 'Attendance']
    marks = candidate_data[subjects].values[0]

    fig = plt.figure(figsize=(15, 5))
    ax1 = fig.add_subplot(131)
    ax1.bar(subjects, marks, color='skyblue')
    ax1.set_xlabel('Subjects')
    ax1.set_ylabel('Marks')
    ax1.set_title('Marks Distribution for Candidate')
    plt.xticks(rotation=45, ha='right')

    ax2 = fig.add_subplot(132)
    categories = ['IA Marks', 'External Marks', 'Seminar Marks', 'Mock Test Results', 'Extra Curriculam Marks',
                  'Attendance']
    category_marks = [sum(candidate_data[['IA 1', 'IA 2', 'IA3']].values[0]),
                      candidate_data['External Marks'].values[0],
                      candidate_data['Seminar Marks'].values[0],
                      candidate_data['Mock Test Results'].values[0],
                      candidate_data['Extra Curriculam  Marks'].values[0],
                      candidate_data['Attendance'].values[0]]
    ax2.pie(category_marks, labels=categories, autopct='%1.1f%%', startangle=140)
    ax2.set_title('Marks Distribution among Categories')

    ax3 = fig.add_subplot(133)
    ax3.plot(subjects, marks, marker='o')
    ax3.set_ylim(0, 100)  # Set y-axis limit to start from 0
    ax3.set_xlabel('Subjects')
    ax3.set_ylabel('Marks')
    ax3.set_title('Marks Variation for Candidate')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    # Embed the matplotlib figures in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    # Add matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, graph_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)




# Create the main window
root = Tk()
root.title("Student Performance Analysis")

# Create GUI elements with labels and frames
input_frame = Frame(root, padx=20, pady=20)
input_frame.pack()

label_usn = Label(input_frame, text="Enter USN:")
label_usn.grid(row=0, column=0, padx=0, pady=0)
usn_entry = Entry(input_frame)
usn_entry.grid(row=0, column=1, padx=0, pady=0)



calculate_button = Button(input_frame, text="Calculate", command=calculate_results)
calculate_button.grid(row=2, columnspan=2, pady=0)

result_frame = Frame(root, padx=10, pady=10)
result_frame.pack()

rank_label = Label(result_frame, text="Rank of this student: ")
rank_label.pack()

details_label = Label(result_frame, text="Candidate Details:")
details_label.pack()

improvement_label = Label(result_frame, text="Area of improvement: ")
improvement_label.pack()

a_label = Label(result_frame, text="Predicted Overall Performance: ")
a_label.pack()

label_actual = Label(input_frame, text="Enter Actual Performance:")
label_actual.grid(row=1, column=0, padx=0, pady=0)
actual_entry = Entry(input_frame)
actual_entry.grid(row=1, column=1, padx=0, pady=0)

button2 = Button(input_frame, text="Graph", command=display_graphs)
button2.grid(row=3, columnspan=3, pady=0)

difference_label = Label(result_frame, text="Difference between Actual and Predicted Performance: ")
difference_label.pack()

graph_frame = Frame(root, padx=0, pady=0)
graph_frame.pack(fill=BOTH, expand=YES)

root.mainloop()
