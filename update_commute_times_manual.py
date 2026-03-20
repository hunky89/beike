import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/lushaorong/code/beikedata/xian_xiaoqu_data_tureprice_with_commute.csv')

# 沣东旺城的正确坐标
fengdongwangcheng_lng = 108.761337
fengdongwangcheng_lat = 34.260382

# 检查沣东旺城的坐标是否正确更新
fengdongwangcheng_row = df[df['name'] == '沣东旺城']
if not fengdongwangcheng_row.empty:
    print(f"沣东旺城坐标: lng={fengdongwangcheng_row.iloc[0]['community_lng']}, lat={fengdongwangcheng_row.iloc[0]['community_lat']}")
else:
    print("未找到沣东旺城记录")

# 检查需要更新驾车时间的小区数量
to_update = df[(pd.notna(df['community_lng'])) & (pd.notna(df['community_lat'])) & ((pd.isna(df['commute_time_from_fengdongwangcheng'])) | (df['commute_time_from_fengdongwangcheng'] > 1000))]
print(f"需要更新驾车时间的小区数量: {len(to_update)}")
print("前10个需要更新的小区:")
print(to_update[['name', 'community_lng', 'community_lat', 'commute_time_from_fengdongwangcheng']].head(10))

# 保存更新后的数据（如果有需要）
df.to_csv('/Users/lushaorong/code/beikedata/xian_xiaoqu_data_tureprice_with_commute.csv', index=False)
print("检查完成！")
