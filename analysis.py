import os
print("Saving in:", os.getcwd())
import sqlite3
import pandas as pd

conn = sqlite3.connect('healthcare.db')

# Attendance Rate
attendance = pd.read_sql("""
SELECT Attended, COUNT(*) as Count,
ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM appointments), 2) AS Percentage
FROM appointments
GROUP BY Attended
""", conn)

print("\nAttendance Rate:\n", attendance)

# Gender Analysis
by_gender = pd.read_sql("""
SELECT Gender, Attended, COUNT(*) as Count
FROM appointments
GROUP BY Gender, Attended
""", conn)

print("\nGender Analysis:\n", by_gender)

# Age Group Analysis
by_age = pd.read_sql("""
SELECT AgeGroup, Attended, COUNT(*) as Count
FROM appointments
GROUP BY AgeGroup, Attended
""", conn)

print("\nAge Group Analysis:\n", by_age)

# Waiting Days Impact
waiting = pd.read_sql("""
SELECT
CASE
    WHEN WaitingDays = 0 THEN 'Same Day'
    WHEN WaitingDays <= 7 THEN '1-7 Days'
    WHEN WaitingDays <= 30 THEN '8-30 Days'
    ELSE '30+ Days'
END AS WaitCategory,
Attended,
COUNT(*) as Count
FROM appointments
GROUP BY WaitCategory, Attended
""", conn)

print("\nWaiting Days Impact:\n", waiting)

# Save to Excel

attendance['Category'] = 'Attendance'
attendance['Type'] = attendance['Attended']

by_gender['Category'] = 'Gender'
by_age['Category'] = 'Age'
waiting['Category'] = 'Waiting'

by_gender = by_gender.rename(columns={'Gender': 'Type'})
by_age = by_age.rename(columns={'AgeGroup': 'Type'})
by_age['Type'] = by_age['Type'].fillna('Unknown')
waiting = waiting.rename(columns={'WaitCategory': 'Type'})

attendance = attendance[['Category', 'Type', 'Count', 'Attended']]
by_gender = by_gender[['Category', 'Type', 'Attended', 'Count']]
by_age = by_age[['Category', 'Type', 'Attended', 'Count']]
waiting = waiting[['Category', 'Type', 'Attended', 'Count']]

final_df = pd.concat([attendance, by_gender, by_age, waiting], ignore_index=True)

final_df['Percentage'] = (final_df['Count'] / final_df.groupby(['Category', 'Type'])['Count'].transform('sum')) * 100
final_df['Percentage'] = final_df['Percentage'].round(2)

final_df = final_df.sort_values(by=['Category', 'Type'])

final_df.to_excel('Healthcare_NoShow_Analysis.xlsx', index=False)

conn.close()