import pandas as pd
import numpy as np
import cv2

class CleaningOps:
    @staticmethod
    def clean_tabular(df: pd.DataFrame, plan: list) -> tuple[pd.DataFrame, dict]:
        df_clean = df.copy()
        report = {
            "removed_columns": [],
            "imputed_columns": [],
            "outliers_removed": 0,
            "duplicates_removed": 0,
            "dropped_rows": 0
        }
        
        for step in plan:
            action = step.get("action")
            
            if action == "drop_columns":
                cols = step.get("columns", [])
                df_clean.drop(columns=cols, inplace=True, errors='ignore')
                report["removed_columns"].extend(cols)

            elif action == "drop_duplicates":
                before = len(df_clean)
                df_clean.drop_duplicates(inplace=True)
                report["duplicates_removed"] = before - len(df_clean)
                report["dropped_rows"] += (before - len(df_clean))
                
            elif action == "impute_or_drop":
                details = step.get("details", {})
                for col, method in details.items():
                    if col not in df_clean.columns: continue
                    
                    if method == "mean":
                        df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                        report["imputed_columns"].append(f"{col} (mean)")
                    elif method == "median":
                        df_clean[col].fillna(df_clean[col].median(), inplace=True)
                        report["imputed_columns"].append(f"{col} (median)")
                    elif method == "mode":
                        if not df_clean[col].mode().empty:
                            df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
                            report["imputed_columns"].append(f"{col} (mode)")
            
            elif action == "iqr_filter":
                cols = step.get("columns", [])
                initial_rows = len(df_clean)
                for col in cols:
                    if col not in df_clean.columns: continue
                    Q1 = df_clean[col].quantile(0.25)
                    Q3 = df_clean[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    # Filter
                    df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
                
                removed = initial_rows - len(df_clean)
                report["outliers_removed"] += removed
                report["dropped_rows"] += removed

            elif action == "clean_text":
                cols = step.get("columns", [])
                cleaned_count = 0
                for col in cols:
                    if col not in df_clean.columns: continue
                    # Check if column is object type/string
                    if df_clean[col].dtype == 'object':
                        # We can count how many actually changed, or just do it
                        # For efficiency, we just do it. But to report, let's verify.
                        # Simple approach: applied to all, assume success.
                        # Or precise:
                        # before_hash = df_clean[col].hash_values? No.
                        df_clean[col] = df_clean[col].astype(str).str.strip()
                        cleaned_count += 1
                
                if cleaned_count > 0:
                    report["standardized_columns"] = report.get("standardized_columns", [])
                    report["standardized_columns"].extend(cols)
                    
        return df_clean, report

    @staticmethod
    def clean_image(image_path: str, output_path: str, plan: list):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Image not found")
            
        for step in plan:
            action = step.get("action")
            if action == "fastNlMeansDenoisingColored":
                img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
                
        cv2.imwrite(output_path, img)
        return output_path
