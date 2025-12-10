import pandas as pd
import numpy as np
import cv2

class CleaningOps:
    @staticmethod
    def clean_tabular(df: pd.DataFrame, plan: list) -> pd.DataFrame:
        df_clean = df.copy()
        
        for step in plan:
            action = step.get("action")
            
            if action == "drop_duplicates":
                df_clean.drop_duplicates(inplace=True)
                
            elif action == "impute_or_drop":
                details = step.get("details", {})
                for col, method in details.items():
                    if col not in df_clean.columns: continue
                    
                    if method == "mean":
                        df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                    elif method == "median":
                        df_clean[col].fillna(df_clean[col].median(), inplace=True)
                    elif method == "mode":
                        if not df_clean[col].mode().empty:
                            df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
            
            elif action == "iqr_filter":
                cols = step.get("columns", [])
                for col in cols:
                    if col not in df_clean.columns: continue
                    Q1 = df_clean[col].quantile(0.25)
                    Q3 = df_clean[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    # Filter
                    df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
                    
        return df_clean

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
