import pandas as pd

INPUT_PATH = "data/cleaned_nigeria_conflict.csv"
df = pd.read_csv(INPUT_PATH)

line = "=" * 80

print(f"\n{line}")
print("📍 REGIONAL ANALYSIS")
print(line)

regional_analysis = (
    df.groupby("admin1")
      .agg(
          Total_Incidents=("event_id_cnty", "count"),
          Total_Fatalities=("fatalities", "sum")
      )
      .sort_values("Total_Incidents", ascending=False)
)

print(regional_analysis.to_string())

print(f"\n{line}")
print("📅 MONTHLY TRENDS")
print(line)

monthly_trends = (
    df.groupby("Month_Year")
      .size()
      .sort_index()
)

print(monthly_trends.to_string())

print(f"\n{line}")
print("⚠️ EVENT TYPE ANALYSIS")
print(line)

severity_analysis = (
    df.groupby("event_type")
      .agg(
          Total_Incidents=("event_id_cnty", "count"),
          Total_Fatalities=("fatalities", "sum")
      )
)

severity_analysis["Casualty_Incident_Ratio"] = (
    severity_analysis["Total_Fatalities"]
    / severity_analysis["Total_Incidents"]
)

severity_analysis = severity_analysis.sort_values(
    "Casualty_Incident_Ratio",
    ascending=False
)

print(severity_analysis.to_string())

print(f"\n{line}")
print("✅ Analysis Complete")
print(line)