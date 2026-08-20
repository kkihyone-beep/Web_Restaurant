import os
import pandas as pd

file_name = "식품_일반음식점.csv"
if os.path.exists(file_name):
    df = pd.read_csv(file_name, encoding="cp949", low_memory=False)
    address_col = (
        "도로명주소"
        if "도로명주소" in df.columns
        else ("지번주소" if "지번주소" in df.columns else None)
    )
    if address_col:
        filtered_df = df[
            df[address_col]
            .astype(str)
            .str.contains("대전|세종|논산", na=False)
        ].copy()
        filtered_df.to_csv("restaurant.csv", index=False, encoding="cp949")
        print("restaurant.csv 재생성 완료!")