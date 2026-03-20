import pandas as pd

df = pd.read_csv("xian_xiaoqu_data_tureprice_with_commute.csv")

community_data = {
    "西安热工研究院南院": {"time": 1559, "lng": 109.005378, "lat": 34.233994},
    "塑料厂家属院": {"time": 1164, "lng": 108.924839, "lat": 34.237953},
    "莱安中心": {"time": 1611, "lng": 108.951339, "lat": 34.198553},
    "东八里新村": {"time": 1642, "lng": 108.947513, "lat": 34.208302},
    "陕西省石油化工家属院": {"time": 1752, "lng": 108.952425, "lat": 34.209873},
    "教师小院": {"time": 1571, "lng": 108.948328, "lat": 34.199758},
    "中海曲江大城君尚府": {"time": 2105, "lng": 109.006844, "lat": 34.179316},
    "西安财经学院红专路生活区": {"time": 1366, "lng": 108.955787, "lat": 34.215706},
    "微生物研究所家属院": {"time": 1542, "lng": 108.995845, "lat": 34.231424},
    "曲江首座": {"time": 1644, "lng": 108.961290, "lat": 34.190231}
}

for name, data in community_data.items():
    idx = df[df['name'] == name].index
    if len(idx) > 0:
        df.at[idx[0], 'commute_time_from_fengdongwangcheng'] = data['time']
        df.at[idx[0], 'community_lng'] = data['lng']
        df.at[idx[0], 'community_lat'] = data['lat']

df.to_csv("xian_xiaoqu_data_tureprice_with_commute.csv", index=False, encoding="utf-8-sig")

print("更新完成！")
print(f"总小区数: {len(df)}")
processed = df['commute_time_from_fengdongwangcheng'].notna().sum()
print(f"已处理: {processed}")
print(f"未处理: {len(df) - processed}")
