#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd

def add_constant(df:pd.DataFrame) -> None:
    df['constant'] = 1
    
    
def add_day_of_week_dummies(df:pd.DataFrame, date_label:str=None):
    if date_label is None:
        dates_index = pd.to_datetime(df.index)
        date_label = '_date'
        df[date_label] = dates_index
        
    else:
        dates_index = pd.to_datetime(df[date_label],format='%Y/%m/%d')
    add_constant(df)
    df['day_of_week'] = dates_index.dt.day_name()
    df['day_of_week'] = df['day_of_week'].str.lower()
    dummies = pd.get_dummies(df['day_of_week'])       
    dummies[date_label] = df['date']
    
    df = pd.merge(df, dummies, left_on=date_label, right_on=date_label, how='left')
    df.drop(['day_of_week'], axis=1, inplace=True)
    df.drop(['date'], axis=1, inplace=True)
    dummies.drop([date_label], axis=1, inplace=True)
    
    return list(dummies.columns), df

