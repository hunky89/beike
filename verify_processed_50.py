import pandas as pd

df = pd.read_csv('xian_xiaoqu_data_tureprice_with_commute.csv')

print('已处理的前50个小区：')
print('='*120)
print(f'{"序号":<4} {"小区名称":<30} {"驾车时间(秒)":<15} {"经度":<15} {"纬度":<15}')
print('='*120)

count = 0
for idx, row in df.iterrows():
    if pd.notna(row['commute_time_from_fengdongwangcheng']):
        count += 1
        print(f'{count:<4} {row["name"]:<30} {int(row["commute_time_from_fengdongwangcheng"]):<15} {row["community_lng"]:<15} {row["community_lat"]:<15}')
    if count >= 50:
        break

print('='*120)
print(f'总小区数: {len(df)}')
print(f'已处理: {df["commute_time_from_fengdongwangcheng"].notna().sum()}')
print(f'未处理: {len(df) - df["commute_time_from_fengdongwangcheng"].notna().sum()}')
