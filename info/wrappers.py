import pandas as pd
from .reference import *

def prepare_debt_dataframe(df):
    old_names = df.columns
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d')
    df['date'] = df['date'].dt.strftime('%d-%m-%Y')
    df.rename(columns={old_names[0]: 'Дата', old_names[1]: debt_indicators_names[old_names[1]]}, inplace=True)
    return df

def prepare_cities_dataframe(df, indicator, state):
    df.drop(['id', 'territory_id'], axis=1, inplace=True)
    old_names = df.columns
    df.rename(columns={old_names[0]: 'Городской округ', old_names[1]: cities_indicators_names[indicator+state]}, inplace=True)
    return df

def prepare_budget_dataframe(df):
    df.drop(['value', 'indicator_id'], axis=1, inplace=True)
    df['report_date'] = pd.to_datetime(df.report_date, format='%Y-%m-%d')
    df['report_date'] = df['report_date'].dt.strftime('%d-%m-%Y')
    old_names = df.columns
    df.rename(columns={old_names[0]: 'Показатель', old_names[1]: 'На дату', old_names[2]: 'Значение, тыс.рублей'}, inplace=True)
    return df

def prepare_struct_dataframe(df):
    df.drop(['struct_id'], axis=1, inplace=True)
    old_names = df.columns
    df.rename(columns={old_names[0]: 'Показатель', old_names[1]: 'Значение, тыс.рублей'}, inplace=True)
    return df
