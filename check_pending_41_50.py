import pandas as pd

df = pd.read_csv('xian_xiaoqu_data_tureprice_with_commute.csv')
unprocessed = df[df['commute_time_from_fengdongwangcheng'].isna()]

print('接下来要处理的第41-50个小区：')
print('='*80)
for i, (idx, row) in enumerate(unprocessed.head(50).iterrows(), 1):
    if 41 <= i <= 50:
        print(f'第{i}个. {row["name"]} (索引: {idx})')
print('='*80)
