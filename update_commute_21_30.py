import pandas as pd

df = pd.read_csv('xian_xiaoqu_data_tureprice_with_commute.csv')

community_data = {
    '中海观园A区': {'time': 26.1, 'lng': 108.981477, 'lat': 34.221269},
    '大丰真境': {'time': 26.2, 'lng': 108.990740, 'lat': 34.218426},
    '曲江兰亭': {'time': 31.7, 'lng': 108.981526, 'lat': 34.191317},
    '苏格兰风笛': {'time': 26.1, 'lng': 109.004013, 'lat': 34.233310},
    '曲江春晓苑': {'time': 26.9, 'lng': 108.973397, 'lat': 34.191316},
    '植物园家属院': {'time': 25.4, 'lng': 108.957809, 'lat': 34.208562},
    '龙湖紫都城': {'time': 30.9, 'lng': 108.990493, 'lat': 34.216778},
    '曲江城市花园': {'time': 27.2, 'lng': 108.973308, 'lat': 34.188843},
    '曲江海天华庭': {'time': 25.9, 'lng': 108.983464, 'lat': 34.221705},
    '中海观园B区': {'time': 28.3, 'lng': 108.985206, 'lat': 34.219323},
}

for name, data in community_data.items():
    idx = df[df['name'] == name].index
    if len(idx) > 0:
        df.at[idx[0], 'commute_time_from_fengdongwangcheng'] = data['time']
        df.at[idx[0], 'community_lng'] = data['lng']
        df.at[idx[0], 'community_lat'] = data['lat']
        print(f'已更新: {name}')

df.to_csv('xian_xiaoqu_data_tureprice_with_commute.csv', index=False, encoding='utf-8-sig')

processed = df['commute_time_from_fengdongwangcheng'].notna().sum()
print(f'\n总数据量: {len(df)}')
print(f'已处理记录数: {processed}')
print(f'未处理记录数: {len(df) - processed}')
