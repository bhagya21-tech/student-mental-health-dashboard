def add_risk_levels(df):
    df = df.copy()
    
    df["mental_health_risk"] = "Low" 
    df.loc[df["mental_health_score"] <= 4, "mental_health_risk"] = "High" 
    df.loc[(df["mental_health_score"] > 4) & (df["mental_health_score"] <= 7), "mental_health_risk"] = "Moderate" 
    
    return df 

def kpi_metrics(df): 
    return {
        "students": len(df),
        "avg_mental_health": round(df["mental_health_score"].mean(), 2),
        "avg_addiction": round(df["addicted_score"].mean(), 2),
        "high_risk_pct": round((df["mental_health_risk"] == "High").mean() * 100, 2)
        
        
    }