# -*- coding: utf-8 -*-
import pandas as pd

# ファイルを読み込む
df = pd.read_csv('output_result.csv')

# Permission列を抽出し、それぞれの値の出現回数をカウント
permission_counts = df.loc[:, 'Permission':].apply(pd.Series.value_counts).sum(axis=1)

# 結果を表示
permission_counts.to_csv('permission_counts.csv')