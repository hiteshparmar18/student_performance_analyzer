import pandas as pd
import numpy as np

def assign_grade(score):
    """Convert average score into a grade."""
    if score >= 85:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 35:
        return "D"
    else:
        return "F"

class StudentPerformanceAnalyzer:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)
    
    def clean_data(self):
        """Fill missing values with column means"""
        self.data.fillna(self.data.mean(numeric_only=True), inplace=True)
    
    def subject_averages(self):
        """Return subject-wise averages as dictionary"""
        return self.data.drop("Name", axis=1).mean().to_dict()
    
    def overall_percentiles(self):
        """Calculate percentile rank of each student"""
        self.data["Total"] = self.data.drop("Name", axis=1).sum(axis=1)
        self.data["Percentile"] = self.data["Total"].rank(pct=True) * 100
        return self.data[["Name", "Total", "Percentile"]]
    
    def top_performers(self, n=3):
        """Return top N students"""
        self.data["Total"] = self.data.drop("Name", axis=1).sum(axis=1)
        return self.data.sort_values(by="Total", ascending=False).head(n)
    
    def grade_distribution(self):
        """Return grade counts as dictionary"""
        self.data["Total"] = self.data.drop("Name", axis=1).sum(axis=1)
        self.data["Average"] = self.data["Total"] / (len(self.data.columns) - 2)  # exclude Name, Total
        self.data["Grade"] = self.data["Average"].apply(assign_grade)
        return self.data["Grade"].value_counts().to_dict()
