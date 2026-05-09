# -*- coding: utf-8 -*-
"""
Created on Sat May  9 07:40:02 2026

@author: Starlin Mini
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_features  = pd.read_csv("five fundamental features attack sim 2.csv")
threshold = 0.8

# Correlation matrix
corr_matrix = df_features.corr(numeric_only=True)

print(corr_matrix)

# Heatmap
plt.figure(figsize=(12,8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title("Feature Correlation Matrix")
plt.show()