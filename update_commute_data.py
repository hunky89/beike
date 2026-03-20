import pandas as pd

# 第1组小区数据
community_data = {
    'KingMall未来中心': {'time': 1201/60, 'lng': 108.868865, 'lat': 34.251925},
    '大茂城': {'time': 1157/60, 'lng': 108.871904, 'lat': 34.238962},
    '铭城东区': {'time': 1101/60, 'lng': 108.857674, 'lat': 34.247677},
    '城南锦绣': {'time': 1661/60, 'lng': 108.974183, 'lat': 34.228021},
    '民政小区': {'time': 1692/60, 'lng': 108.975004, 'lat': 34.224558},
    '碧水西岸南湖一号': {'time': 2125/60, 'lng': 108.976936, 'lat': 34.200245},
    '湖滨花园': {'time': 2056/60, 'lng': 108.968417, 'lat': 34.202518},
    '丽融大厦': {'time': 1884/60, 'lng': 108.947351, 'lat': 34.207731},
    '香都东岸': {'time': 1945/60, 'lng': 108.993492, 'lat': 34.185362},
    '曲江溪园': {'time': 1983/60, 'lng': 108.965720, 'lat': 34.194199},
}

if not community_data:
    print("请先在脚本中填入小区数据！")
    print("数据格式示例：")
    print("""
community_data = {
    '小区名称1': {'time': 30.5, 'lng': 108.952317, 'lat': 34.259764},
    '小区名称2': {'time': 25.0, 'lng': 108.844863, 'lat': 34.242142},
}
    """)
    exit(1)

# 读取CSV文件
df = pd.read_csv('xian_xiaoqu_data_tureprice_with_commute.csv')

updated_count = 0
for idx, row in df.iterrows():
    name = row['name']
    if name in community_data:
        data = community_data[name]
        df.at[idx, 'commute_time_from_fengdongwangcheng'] = data['time']
        df.at[idx, 'community_lng'] = data['lng']
        df.at[idx, 'community_lat'] = data['lat']
        updated_count += 1

# 保存到CSV
df.to_csv('xian_xiaoqu_data_tureprice_with_commute.csv', index=False, encoding='utf-8-sig')

print(f'更新了 {updated_count} 条记录')
print(f'总数据量: {len(df)}')
processed_count = df['commute_time_from_fengdongwangcheng'].notna().sum()
print(f'已处理记录数: {processed_count}')
print(f'未处理记录数: {len(df) - processed_count}')
