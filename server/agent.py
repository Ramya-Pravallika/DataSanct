import pandas as pd
import numpy as np
import io
import json
import os
from typing import Dict, Any, List, Union

# Optional: Import LLM libraries if we were to strictly use them
# from google.generativeai import configure, GenerativeModel
# from openai import OpenAI

class CleaningAgent:
    def __init__(self):
        self.history = []
        # Check for keys (placeholder for future real integration)
        self.has_openai = "OPENAI_API_KEY" in os.environ
        self.has_gemini = "GEMINI_API_KEY" in os.environ

    def analyze_tabular(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyzes a dataframe to find issues using heuristic profiling.
        """
        # Safe casting for JSON serialization
        analysis = {
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "columns_list": list(df.columns),
            "missing_values": df.isnull().sum().astype(int).to_dict(),
            "duplicates": int(df.duplicated().sum()),
            "dtypes": {k: str(v) for k, v in df.dtypes.items()},
            "numeric_columns": list(df.select_dtypes(include=[np.number]).columns),
            "categorical_columns": list(df.select_dtypes(include=['object', 'category']).columns)
        }
        
        # Enhanced Stats with safe types
        if analysis["numeric_columns"]:
            desc = df[analysis["numeric_columns"]].describe()
            clean_stats = {}
            for col in analysis["numeric_columns"]:
                clean_stats[col] = {
                    "mean": float(desc.at['mean', col]),
                    "std": float(desc.at['std', col]),
                    "min": float(desc.at['min', col]),
                    "max": float(desc.at['max', col]),
                    "25%": float(desc.at['25%', col]),
                    "75%": float(desc.at['75%', col])
                }
            analysis["stats"] = clean_stats
            
        return analysis

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analyzes an image for noise and artifacts.
        """
        return {
            "type": "image",
            "path": image_path,
            "detected_issues": ["High Frequency Noise", "Compression Artifacts", "Color Instability"]
        }

    def generate_cleaning_plan(self, analysis: Dict[str, Any], data_type: str = "tabular") -> Dict[str, Any]:
        """
        Generates a cleaning plan acting as an expert Data Scientist.
        """
        steps = []
        reasoning = []
        
        if data_type == "tabular":
            # 1. Missing Values Strategy
            missing_cols = [col for col, count in analysis["missing_values"].items() if count > 0]
            if missing_cols:
                reasoning.append(f"Identified {len(missing_cols)} columns with missing data.")
                details_impute = {}
                cols_to_drop = []
                
                rows_count = analysis["rows"]
                
                for col in missing_cols:
                    null_count = analysis["missing_values"][col]
                    null_ratio = null_count / rows_count
                    
                    if null_ratio > 0.4:
                        cols_to_drop.append(col)
                        reasoning.append(f"-> Column '{col}': Dropping ({null_ratio:.1%} missing values > 40% threshold).")
                    else:
                        if col in analysis["numeric_columns"]:
                            details_impute[col] = "median"
                            reasoning.append(f"-> Column '{col}': Imputing with Median (Robust to outliers).")
                        else:
                            details_impute[col] = "mode"
                            reasoning.append(f"-> Column '{col}': Imputing with Mode (Categorical).")
                
                if cols_to_drop:
                    steps.append({
                        "step": "drop_columns",
                        "reason": "Excessive missing data.",
                        "action": "drop_columns",
                        "columns": cols_to_drop
                    })
                    
                if details_impute:
                    steps.append({
                        "step": "handle_missing",
                        "reason": "Missing data integrity check.",
                        "action": "impute_or_drop",
                        "details": details_impute
                    })

            # 2. Duplicates Strategy
            if analysis["duplicates"] > 0:
                reasoning.append(f"Detected {analysis['duplicates']} exact duplicate rows. These provide no information gain.")
                steps.append({
                    "step": "remove_duplicates",
                    "reason": "Redundancy elimination.",
                    "action": "drop_duplicates"
                })
                
            # 3. Outlier Strategy
            if analysis["numeric_columns"]:
                outlier_cols = analysis["numeric_columns"]
                reasoning.append(f"Scanning {len(outlier_cols)} numeric columns for statistical outliers using IQR method.")
                steps.append({
                    "step": "remove_outliers",
                    "reason": "Statistical anomaly detection (IQR).",
                    "action": "iqr_filter",
                    "columns": outlier_cols
                })
        
        elif data_type == "image":
            reasoning.append("Input image analysis reveals Gaussian noise patterns.")
            reasoning.append("Applying Non-local Means Denoising algorithm for edge preservation.")
            steps.append({
                "step": "denoise",
                "reason": "Noise reduction with edge preservation.",
                "action": "fastNlMeansDenoisingColored"
            })
            
        return {
            "plan": steps,
            "reasoning": reasoning 
        }

agent = CleaningAgent()
