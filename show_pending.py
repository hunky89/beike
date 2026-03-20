import pandas as pd

# 读取CSV文件
df = pd.read_csv('xian_xiaoqu_data_tureprice_with_commute.csv')

# 找出未处理的小区
unprocessed = df[df['commute_time_from_fengdongwangcheng'].isna()]
print(f"总数据量: {len(df)}")
print(f"已处理记录数: {df['commute_time_from_fengdongwangcheng'].notna().sum()}")
print(f"未处理记录数: {len(unprocessed)}")
print()

# 显示接下来要处理的3组小区（共30个）
print("接下来要处理的小区列表：")
print("=" * 80)

for i in range(min(30, len(unprocessed))):
    row = unprocessed.iloc[i]
    group_num = (i // 10) + 1
    idx_in_group = (i % 10) + 1
    print(f"第{group_num}组-{idx_in_group:02d}. {row['name']} (索引: {row.name})")

print("=" * 80)
