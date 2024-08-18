import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

data = pd.read_excel("student_data.xlsx")

# Assuming 'Rank' is the target variable
data['Total_Marks'] = data[['IA 1', 'IA 2', 'IA3', 'External Marks', 'Seminar Marks', 'Mock Test Results', 'Extra Curriculam  Marks', 'Attendance']].sum(axis=1)
X = data.drop(['USN', 'Name', 'DOB', 'Department', 'Total_Marks'], axis=1)
y = data['Total_Marks']

# Step 2: Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Model Training
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Step 5: Prediction and Rank Calculation
usn = input("Enter the USN of the candidate: ")
candidate_data = data[data['USN'] == usn]
candidate_features = candidate_data.drop(['USN', 'Name', 'DOB', 'Department', 'Total_Marks'], axis=1)
predicted_total_marks = model.predict(candidate_features)[0]

# Finding rank
data['Predicted_Total_Marks'] = model.predict(X)
data = data.sort_values(by='Predicted_Total_Marks', ascending=False).reset_index(drop=True)
rank = data[data['USN'] == usn].index[0] + 1

# Displaying candidate details
candidate_info = candidate_data[['Name', 'DOB', 'Department', 'Attendance']]
print("\nCandidate Details:")
print(candidate_info.to_string(index=False))

print("\nRank of this student:", rank)

# Finding the field with the least marks
subject_marks = candidate_data[['IA 1', 'IA 2', 'IA3', 'External Marks', 'Seminar Marks', 'Mock Test Results', 'Extra Curriculam  Marks', 'Attendance']]
min_subject = subject_marks.idxmin(axis=1).values[0]
min_marks = subject_marks.min(axis=1).values[0]

print("Area of improvement:", min_subject)

# Calculate overall performance
max_marks_per_subject = 100  # Assuming maximum marks per subject is 100
total_marks_obtained = sum(candidate_data[['IA 1', 'IA 2', 'IA3', 'External Marks', 'Seminar Marks', 'Mock Test Results', 'Extra Curriculam  Marks']].values[0])
total_possible_marks = max_marks_per_subject * 7  # Assuming 7 subjects excluding attendance
overall_performance = (total_marks_obtained / total_possible_marks) * 100

print("\nOverall Predicted Performance (0-100):", round(overall_performance, 2))

var = int(input("Enter the actual performance: "))

# Calculate and display the difference between actual and predicted performance
performance_difference = var - overall_performance
print("\nDifference between Actual and Predicted Performance:", round(performance_difference, 2))

# Creating a bar chart for subject marks
subjects = ['IA 1', 'IA 2', 'IA3', 'External Marks', 'Seminar Marks', 'Mock Test Results', 'Extra Curriculam  Marks', 'Attendance']
marks = candidate_data[subjects].values[0]

plt.figure(figsize=(10, 6))
plt.bar(subjects, marks, color='skyblue')
plt.xlabel('Subjects')
plt.ylabel('Marks')
plt.title('Marks Distribution for Candidate')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Creating a pie chart for marks distribution categories
categories = ['IA Marks', 'External Marks', 'Seminar Marks', 'Mock Test Results', 'Extra Curriculam Marks', 'Attendance']
category_marks = [sum(candidate_data[['IA 1', 'IA 2', 'IA3']].values[0]),
                  candidate_data['External Marks'].values[0],
                  candidate_data['Seminar Marks'].values[0],
                  candidate_data['Mock Test Results'].values[0],
                  candidate_data['Extra Curriculam  Marks'].values[0],
                  candidate_data['Attendance'].values[0]]

plt.figure(figsize=(8, 8))
plt.pie(category_marks, labels=categories, autopct='%1.1f%%', startangle=140)
plt.title('Marks Distribution among Categories')
plt.axis('equal')
plt.tight_layout()
plt.show()

# Creating a line graph for marks variation
plt.figure(figsize=(10, 6))
plt.plot(subjects, marks, marker='o')
plt.xlabel('Subjects')
plt.ylabel('Marks')
plt.title('Marks Variation for Candidate')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
