import pandas as pd 

def clean_students_data(df):
    df = df.copy()
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    
    df.drop_duplicates(inplace=True) 
    
    numeric_cols = [
        "age", "avg_daily_usage_hours", "sleep_hours_per_night", 
        "mental_health_score", "addicted_score", "conflicts_over_social_media"
    ] 
    
    for col in numeric_cols: 
        df[col] = pd.to_numeric(df[col], errors="coerce") 
        
    df.fillna(df.median(numeric_only=True), inplace=True)
    
    return df
