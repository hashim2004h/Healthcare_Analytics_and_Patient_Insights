import pandas as pd

# Load dataset
df = pd.read_csv('KaggleV2-May-2016.csv')

print("Original Shape:", df.shape)

# Rename confusing column
df.rename(columns={'No-show': 'NoShow'}, inplace=True)

# Convert date columns
df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])

# Create waiting days feature
df['WaitingDays'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days

# Remove invalid data
df = df[df['Age'] >= 0]
df = df[df['WaitingDays'] >= 0]

# Create attended column (VERY IMPORTANT)
df['Attended'] = df['NoShow'].map({'No': 'Yes', 'Yes': 'No'})

# Create age groups
bins = [0, 12, 17, 35, 60, 120]
labels = ['Child', 'Teen', 'Young Adult', 'Adult', 'Senior']
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)

# Save cleaned dataset
df.to_csv('cleaned_health.csv', index=False)

print("Cleaned Shape:", df.shape)
print("Cleaning done!")

# -------- SQL DATABASE PART --------
import sqlite3

conn = sqlite3.connect('healthcare.db')

df = pd.read_csv('cleaned_health.csv')

df.to_sql('appointments', conn, if_exists='replace', index=False)

print("Database created successfully!")

conn.close()