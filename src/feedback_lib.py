# feedback_lib.py

# Module Imports
import pandas as pd

from pandas import DataFrame

'''
Filtering Functions
'''

# Filter Feedback Data
def filter_feedback_data(df: DataFrame, feedback_breakdown: str) -> DataFrame:
    ## Base Columns
    base_columns = ['question','question_category','feedback_score']
    ## Resident Type
    if feedback_breakdown.lower() == 'resident_type':
        df = df[['resident_type'] + base_columns]
    ## Resident length
    elif feedback_breakdown.lower() == 'resident_length':
        df = df[['resident_length'] + base_columns]
    ## Building Name
    elif feedback_breakdown.lower() == 'building_name':
        df = df[['building_name'] + base_columns]
    ## Building Floor
    elif feedback_breakdown.lower() == 'building_floor':
        df = df[['building_floor'] + base_columns]
    ## Return
    return df


'''
Summarise Data
'''
# Average - All Feedback - Mean
def feedback_all_mean(df: DataFrame) -> int:
    return round(df["feedback_score"].mean(),1)

# Counts - All - Positive, Neutral, Negative
def feedback_all_nps_counts(df: DataFrame, nps_type: str) -> int:
    if nps_type.lower() == 'positive':
        response_count = len(df[df['feedback_score'] > 4])
    elif nps_type.lower() == 'neutral':
        response_count = len(df[df['feedback_score'].between(3, 4)])
    elif nps_type.lower() == 'negative':
        response_count = len(df[df['feedback_score'] < 3])
    return response_count

# Percentages - All - Positive, Neutral, Negative
def feedback_all_nps_percentages(df: DataFrame, nps_type: str) -> int:
    max_response = len(df['response_id'])
    if nps_type.lower() == 'positive':
        response_count = feedback_all_nps_counts(df, nps_type)
    elif nps_type.lower() == 'neutral':
        response_count = feedback_all_nps_counts(df, nps_type)
    elif nps_type.lower() == 'negative':
        response_count = feedback_all_nps_counts(df, nps_type)
    
    return int(round((response_count/max_response) * 100, 0))

# Questions
def feedback_questions_average(df: DataFrame) -> DataFrame:
    return df.groupby(['question_category']).mean().reset_index()


'''
Sentiment data
'''
# Percentages - Sentiment - Positive, Neutral, Negative
def sentiment_percentages(df: DataFrame, sen_type: str) -> int:
    max_response = len(df['response_id'])
    if sen_type.lower() == 'positive':
        response_count = len(df[df['sentiment'] == 'positive'])
    elif sen_type.lower() == 'neutral':
        response_count = len(df[df['sentiment'] == 'neutral'])
    elif sen_type.lower() == 'negative':
        response_count = len(df[df['sentiment'] == 'negative'])
    
    return int(round((response_count/max_response) * 100, 0))