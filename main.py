#  This code generates visualizations for a mental health dataset. First, preprocessing is done on the dataset to clean and format the data. 
# Then, the data is visualized using bar charts, radar charts, and scatter plots to analyze the factors influencing mental health adn people's attitude towards mental health. 
# The libraries used for this code are as follows:
# pandas                       2.2.1
# plotly                       5.21.0
# matplotlib                   3.8.0
# seaborn                      0.13.2 

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os
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


# """Data Preprocessing for Radar Chart: Converting Categorical Data to Numerical Data
# This function will allow us to convert the categorical data to numerical data for the radar chart, with 1 being
# the response we are interested in and 0 being the other responses. This will allow us to plot the radar chart"""
df_mental_health = data_preprocessing();

def data_preprocessing_radar_chart(factor_response, decision_response):
    df_radar_response = df_mental_health.copy() # Copying the original dataframe to a new dataframe
    # Mapping the responses to ensure uniformity 
    df_radar_response["Mood_Swings"] = df_radar_response["Mood_Swings"].map({"High" : "Yes", "Medium" : "Maybe", "Low" : "No"}) 
    df_radar_response["Care_Options"] = df_radar_response["Care_Options"].map({"Yes" : "Yes", "No" : "No", "Not sure" : "Maybe"})

    df_radar_response["Family_History"] = df_radar_response["Family_History"].map({factor_response : 1}).fillna(0)
    df_radar_response["Treatment"] = df_radar_response["Treatment"].map({factor_response : 1}).fillna(0)
    df_radar_response["Growing_Stress"] = df_radar_response["Growing_Stress"].map({factor_response : 1}).fillna(0)
    df_radar_response["Changes_Habits"] = df_radar_response["Changes_Habits"].map({factor_response : 1}).fillna(0)
    df_radar_response["Mental_Health_History"] = df_radar_response["Mental_Health_History"].map({factor_response : 1}).fillna(0)
    df_radar_response["Mood_Swings"] = df_radar_response["Mood_Swings"].map({factor_response : 1}).fillna(0) 
    df_radar_response["Coping_Struggles"] = df_radar_response["Coping_Struggles"].map({factor_response : 1}).fillna(0)
    df_radar_response["Work_Interest"] = df_radar_response["Work_Interest"].map({factor_response : 1}).fillna(0)
    df_radar_response["Social_Weakness"] = df_radar_response["Social_Weakness"].map({factor_response : 1}).fillna(0)
    df_radar_response["Mental_Health_Interview"] = df_radar_response["Mental_Health_Interview"].map({factor_response : 1}).fillna(0)
    df_radar_response["Care_Options"] = df_radar_response["Care_Options"].map({decision_response : 1}).fillna(0)

    return df_radar_response

df_radar_positive_1 = data_preprocessing_radar_chart("Yes", "Yes");
df_radar_positive_2 = data_preprocessing_radar_chart("No", "Yes");
df_radar_positive_3 = data_preprocessing_radar_chart("Maybe", "Yes");

df_radar_negative_1 = data_preprocessing_radar_chart("No", "No");
df_radar_negative_2 = data_preprocessing_radar_chart("Yes", "No");
df_radar_negative_3 = data_preprocessing_radar_chart("Maybe", "No");

df_radar_neutral_1 = data_preprocessing_radar_chart("Yes", "Maybe");
df_radar_neutral_2 = data_preprocessing_radar_chart("No", "Maybe");
df_radar_neutral_3 = data_preprocessing_radar_chart("Maybe", "Maybe");


# """Radar Chart for People Opting for Care Options"""
def radar_plotter(df_radar, response1, response2):
    df_radar.drop(df_radar[df_radar["Care_Options"] == 0].index, inplace = True)
    radar_dict = dict(
                    score = [(df_radar["Family_History"].mean()), (df_radar["Treatment"].mean()),
                    (df_radar["Growing_Stress"].mean()), (df_radar["Changes_Habits"].mean()),
                    (df_radar["Mental_Health_History"].mean()), (df_radar["Mood_Swings"].mean()),
                    (df_radar["Coping_Struggles"].mean()), (df_radar["Work_Interest"].mean()),
                    (df_radar["Social_Weakness"].mean()), (df_radar["Mental_Health_Interview"].mean())],
                    names = ["Family History", "Treatment", "Growing Stress", "Changes Habits", "Mental Health History", "Mood Swings", "Coping Struggles",
                    "Work Interest", "Social Weakness", "Mental Health Interview"]
                    )

    fig_radar = px.line_polar(radar_dict, r = 'score', theta = 'names', line_close = True)
    fig_radar.update_traces(fill = 'toself')
    fig_radar.update_layout(
                            title = ("Radar Chart for People Opting " + response1 + " for Care Options and " + response2 + " for Influencing Factors"), 
                            title_x = 0.5,
                            polar = dict(
                                        radialaxis = dict(
                                                        visible = True,
                                                        range = [0, 1],
                                                        tickmode = 'array',
                                                        tickvals = [i/10 for i in range(11)]
                                                        )
                                        )
                            )
    fig_radar.show() 


radar_plotter(df_radar_positive_1, "Yes", "Yes")
radar_plotter(df_radar_positive_2, "Yes", "No")
radar_plotter(df_radar_positive_3, "Yes", "Maybe")
radar_plotter(df_radar_negative_1, "No", "No")
radar_plotter(df_radar_negative_2, "No", "Yes")
radar_plotter(df_radar_negative_3, "No", "Maybe")
radar_plotter(df_radar_neutral_1, "Maybe", "Yes")
radar_plotter(df_radar_neutral_2, "Maybe", "No")
radar_plotter(df_radar_neutral_3, "Maybe", "Maybe")


# """Scatter Plot for Prevalence of Factors Influencing Mental Health by Gender"""
# Mapping for Factors Influencing Mental Health
def data_mapping_scatterplot(response):
    df_mapped = df_mental_health.copy() # Copying the original dataframe to a new dataframe
    # Mapping the responses to ensure uniformity 
    df_mapped["Mood_Swings"] = df_mapped["Mood_Swings"].map({"High" : "Yes", "Medium" : "Maybe", "Low" : "No"}) 
    df_mapped["Care_Options"] = df_mapped["Care_Options"].map({"Yes" : "Yes", "No" : "No", "Not sure" : "Maybe"})

    df_mapped["Family_History"] = df_mapped["Family_History"].map({response : 1}).fillna(0)
    df_mapped["Treatment"] = df_mapped["Treatment"].map({response : 1}).fillna(0)
    df_mapped["Growing_Stress"] = df_mapped["Growing_Stress"].map({response : 1}).fillna(0)
    df_mapped["Changes_Habits"] = df_mapped["Changes_Habits"].map({response : 1}).fillna(0)
    df_mapped["Mental_Health_History"] = df_mapped["Mental_Health_History"].map({response : 1}).fillna(0)
    df_mapped["Mood_Swings"] = df_mapped["Mood_Swings"].map({response : 1}).fillna(0) 
    df_mapped["Coping_Struggles"] = df_mapped["Coping_Struggles"].map({response : 1}).fillna(0)
    df_mapped["Work_Interest"] = df_mapped["Work_Interest"].map({response : 1}).fillna(0)
    df_mapped["Social_Weakness"] = df_mapped["Social_Weakness"].map({response : 1}).fillna(0)
    df_mapped["Mental_Health_Interview"] = df_mapped["Mental_Health_Interview"].map({response : 1}).fillna(0)
    df_mapped["Care_Options"] = df_mapped["Care_Options"].map({response : 1}).fillna(0)

    return df_mapped

df_mapped_yes = data_mapping_scatterplot("Yes")

# Prevalence of Factors Influencing Mental Health
factors = ["Family_History", "Treatment", "Growing_Stress", "Changes_Habits", "Mental_Health_History", "Mood_Swings", "Coping_Struggles", 
                "Work_Interest", "Social_Weakness", "Mental_Health_Interview", "Care_Options"] # List of factors and decisions influencing mental health

def prevalence_by_gender(df, gender):
    df_mapped_copy = df.copy() # Copying the original dataframe to a new dataframe
    prevalence = [] # List to store the prevalence of each gender
    df_mapped_copy.drop(df_mapped_copy[df_mapped_copy["Gender"] != gender].index, inplace = True) # Filtering the dataframe by gender

    for factor in factors:
        prevalence.append(df_mapped_copy[factor].mean()) # Calculating the prevalence of each factor

    return prevalence

prevalence_male = prevalence_by_gender(df_mapped_yes, "Male")
prevalence_female = prevalence_by_gender(df_mapped_yes, "Female")

# Creating new dataframe for scatter plot
df_prevalence = pd.DataFrame({"Factor": factors, "Male": prevalence_male, "Female": prevalence_female})

# Scatter Plot 
plt.figure(figsize = (10, 5))
for i in range(df_prevalence.shape[0]):
    plt.scatter(df_prevalence['Male'][i], df_prevalence['Female'][i], s = 50)

limits = (0, 1)
plt.plot(limits, limits, color = "black", linestyle = "dashed") # Adding a dashed line to split the plot in half and show the difference between the genders

plt.xlabel("Prevalence in Males")
plt.ylabel("Prevalence in Females")
plt.title("Prevalence of Factors Influencing Mental Health by Gender")
plt.legend(factors)
plt.grid(True)
plt.show()