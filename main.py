import pandas as pd
import os

def data_preprocessing():
    file_path = 'resources/Mental Health Dataset.csv'
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        df = pd.read_csv(file_path, skiprows=0)
        print(df.size)
        df.dropna(subset=['self_employed'], inplace=True)
        print(df.size)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%m/%d/%Y %H:%M')
        df.sort_values(by='Timestamp', inplace=True)
        column_mappings = {
            'Timestamp': 'Timestamp',
            'Gender': 'Gender',
            'Country': 'Country',
            'Occupation': 'Occupation',
            'self_employed': 'Self_Employed',
            'family_history': 'Family_History',
            'treatment': 'Treatment',
            'Days_Indoors': 'Days_Indoors',
            'Growing_Stress': 'Growing_Stress',
            'Changes_Habits': 'Changes_Habits',
            'Mental_Health_History': 'Mental_Health_History',
            'Mood_Swings': 'Mood_Swings',
            'Coping_Struggles': 'Coping_Struggles',
            'Work_Interest': 'Work_Interest',
            'Social_Weakness': 'Social_Weakness',
            'mental_health_interview': 'Mental_Health_Interview',
            'care_options': 'Care_Options'
        }

        df.rename(columns=column_mappings, inplace=True)

        df['Date'] = df['Timestamp'].dt.date
        df['Time_Of_Day'] = df['Timestamp'].dt.time

        df['Day'] = df['Timestamp'].dt.day
        df['Month'] = df['Timestamp'].dt.month
        df['Year'] = df['Timestamp'].dt.year

    else:
        print('File does not!')

data_preprocessing();