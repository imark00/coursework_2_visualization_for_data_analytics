import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

def exploratory_analysis(df):
    sns.set_style("whitegrid")

    cols_to_visualize = ['Gender', 'Self_Employed', 'Family_History', 'Treatment', 'Days_Indoors', 'Growing_Stress',
                         'Changes_Habits', 'Mental_Health_History', 'Mood_Swings', 'Coping_Struggles', 'Work_Interest',
                         'Social_Weakness']
    counts = []

    for col in cols_to_visualize:
        counts.append(df[col].value_counts())

    fig, axs = plt.subplots(4, 3, figsize=(15, 20))
    axs = axs.flatten()

    for i, (col, count) in enumerate(zip(cols_to_visualize, counts)):
        axs[i].pie(count, labels=count.index, autopct='%1.1f%%', startangle=90)
        axs[i].set_title(col)

    plt.show()
def temporal_analysis(df):
    daily_counts = df.groupby(df['Date']).size()
    daily_counts.head()

    plt.figure(figsize=(12, 6))
    plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-')
    plt.title('Number of responses over time')
    plt.xlabel('Date')
    plt.ylabel('Number of Responses')
    plt.xticks(rotation=90)
    plt.tight_layout()
    for x, y in zip(daily_counts.index, daily_counts.values):
        plt.annotate(str(y), xy=(x, y), xytext=(5, 5), textcoords='offset points')

    plt.show()

def data_plotting(df):
    exploratory_analysis(df)
    temporal_analysis(df)
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

        data_plotting(df)


    else:
        print('File does not!')

data_preprocessing();