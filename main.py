import pandas as pd

# Đọc dữ liệu (không có dòng tiêu đề nên dùng header=None)
df = pd.read_csv("credit-approval.csv", header=None)