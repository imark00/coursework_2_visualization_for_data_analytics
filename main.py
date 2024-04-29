import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio

def create_group_barchart_for_symptoms(param1,df, title):
    # List of columns for which to calculate the percentage of 'Yes' responses
    columns_of_interest = ['Treatment', 'Growing_Stress', 'Changes_Habits', 'Mental_Health_History','Mood_Swings', 'Coping_Struggles', 'Work_Interest', 'Social_Weakness']
    percentage_yes_dict = {}
    for column in columns_of_interest:
        grouped_counts = df.groupby([param1, column]).size().unstack(fill_value=0)
        total_responses = grouped_counts.sum(axis=1)
        yes_count = grouped_counts.get('Yes', 0)
        high_count = grouped_counts.get('High', 0)
        percentage_yes = ((yes_count + high_count) / total_responses) * 100
        percentage_yes_dict[column] = percentage_yes

    percentage_yes_df = pd.DataFrame(percentage_yes_dict)
    print(percentage_yes_df)

    plt.figure(figsize=(12, 9))
    percentage_yes_df.plot(kind='bar', width=0.8, colormap='viridis')
    plt.title(title)
    plt.xlabel(param1)
    plt.ylabel('Percentage of "Yes" Responses')
    plt.xticks(rotation=0,fontsize=6)
    plt.legend(title='Influencing Factors', loc='center left', fontsize=6, bbox_to_anchor=(1, 0.5), borderaxespad=0.)
    plt.tight_layout()

    plt.show()

def create_group_barchart_for_mental_health_interview(param1,df, title):
    columns_of_interest = ['Mental_Health_Interview']
    percentage_no_dict = {}
    for column in columns_of_interest:
        grouped_counts = df.groupby([param1, column]).size().unstack(fill_value=0)
        total_responses = grouped_counts.sum(axis=1)
        no_count = grouped_counts.get('No', 0)
        percentage_no = ((no_count) / total_responses) * 100
        percentage_no_dict[column] = percentage_no

    percentage_no_df = pd.DataFrame(percentage_no_dict)
    print(percentage_no_df)
    plt.figure(figsize=(12, 9))
    percentage_no_df.plot(kind='bar', width=0.8, colormap='viridis', legend=False)
    plt.title(title)
    plt.xlabel(param1)
    plt.ylabel('Percentage of "No" Responses')
    plt.xticks(rotation=0,fontsize=10)
    plt.show()

def create_barchart_for_mental_health_interview(df):
    grouped_counts = df.groupby('Occupation').size()
    total_responses = grouped_counts.sum()
    percentage_responses = (grouped_counts / total_responses) * 100
    print(percentage_responses)
    plt.figure(figsize=(10, 7))
    sns.barplot(x=percentage_responses.index, y=percentage_responses.values, palette='viridis')
    plt.title('Percentage of "No" Responses for Mental Health Interview by Occupation')
    plt.xlabel('Occupation')
    plt.ylabel('Percentage of "No" Responses')
    plt.xticks(rotation=0)
    plt.show()

def barchart_visulization(df):
    create_group_barchart_for_symptoms('Occupation',df,'Occupation x Influencing Factors')
    create_group_barchart_for_symptoms('Self_Employed',df,'Self Employment x Influencing Factors')
    create_group_barchart_for_symptoms('Days_Indoors',df,'Days Indoor x Influencing Factors')
    create_group_barchart_for_mental_health_interview('Occupation',df,'Occupation x Mental Health Interview')
    create_barchart_for_mental_health_interview(df)


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
        return df
    else:
        print('File does not!')
        
def crete_map_for_country_and_yes_care_options(df:pd.DataFrame):
    country_careOptions_df = df.groupby(['country'])['care_options'].value_counts().unstack().reset_index().fillna(0)
    country_careOptions_df.columns = country_careOptions_df.columns.str.strip().str.lower().str.replace(' ', '_')

    country_careOptions_df['yes_percentages'] = round((country_careOptions_df['yes'] / country_careOptions_df['yes'].sum()) * 100, 2)
    country_careOptions_df['no_percentages'] = round((country_careOptions_df['no'] / country_careOptions_df['no'].sum()) * 100, 2)
    country_careOptions_df['not_sure_percentages'] = round((country_careOptions_df['not_sure'] / country_careOptions_df['not_sure'].sum()) * 100, 2)
    
    pio.renderers.default = 'browser'
    fig = px.choropleth(country_careOptions_df, locations='country', locationmode='country names', color='yes_percentages', hover_name='country', hover_data='yes',color_continuous_scale= 'Greens', title='Yes Care Options by Country')
    fig.show() 
    
    
def create_map_for_country_and_yes_family_history(df:pd.DataFrame):
    country_family_history_df = df.groupby(['country'])['family_history'].value_counts().unstack().reset_index().fillna(0)
    country_family_history_df.columns = country_family_history_df.columns.str.strip().str.lower().str.replace(' ', '_')

    country_family_history_df['yes_percentages'] = round((country_family_history_df['yes'] / country_family_history_df['yes'].sum()) * 100, 2)
    country_family_history_df['no_percentages'] = round((country_family_history_df['no'] / country_family_history_df['no'].sum()) * 100, 2)
    
    pio.renderers.default = 'browser'
    fig = px.choropleth(country_family_history_df, locations='country', locationmode='country names', color='yes_percentages', hover_name='country',hover_data='yes', color_continuous_scale= 'Greens',title='Yes Family History by Country')
    fig.show() 


def create_map_for_country_and_yes_mental_health_history(df:pd.DataFrame):
    country_mental_health_history_df = df.groupby(['country'])['mental_health_history'].value_counts().unstack().reset_index().fillna(0)
    country_mental_health_history_df.columns = country_mental_health_history_df.columns.str.strip().str.lower().str.replace(' ', '_')

    country_mental_health_history_df['yes_percentages'] = round((country_mental_health_history_df['yes'] / country_mental_health_history_df['yes'].sum()) * 100, 2)
    country_mental_health_history_df['no_percentages'] = round((country_mental_health_history_df['no'] / country_mental_health_history_df['no'].sum()) * 100, 2)

    pio.renderers.default = 'browser'
    fig = px.choropleth(country_mental_health_history_df, locations='country', locationmode='country names', color='yes_percentages', hover_name='country', hover_data='yes',color_continuous_scale= 'Greens',title='Yes Mental Health History by Country')
    fig.show() 
    
    
def create_map_for_country_and_yes_treatment(df:pd.DataFrame):
    country_treatment_df = df.groupby(['country'])['treatment'].value_counts().unstack().reset_index().fillna(0)
    country_treatment_df.columns = country_treatment_df.columns.str.strip().str.lower().str.replace(' ', '_')

    country_treatment_df['yes_percentages'] = round((country_treatment_df['yes'] / country_treatment_df['yes'].sum()) * 100, 2)
    country_treatment_df['no_percentages'] = round((country_treatment_df['no'] / country_treatment_df['no'].sum()) * 100, 2)
    
    pio.renderers.default = 'browser'
    fig = px.choropleth(country_treatment_df, locations='country', locationmode='country names', color='yes_percentages', hover_name='country', hover_data='yes',color_continuous_scale= 'Greens', title='Yes Treatment by Country')
    fig.show() 
    
    

def map_visualization(df:pd.DataFrame):
    df.columns = df.columns.str.strip().str.lower()
    crete_map_for_country_and_yes_care_options(df)
    create_map_for_country_and_yes_family_history(df)
    create_map_for_country_and_yes_mental_health_history(df)
    create_map_for_country_and_yes_treatment(df)



def data_analysis():
    df = data_preprocessing()
    barchart_visulization(df)
    map_visualization(df)

data_analysis()