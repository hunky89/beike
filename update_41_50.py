import pandas as pd

df = pd.read_csv("xian_xiaoqu_data_tureprice_with_commute.csv")

community_data = {
    "地震局家属院": {"time": 1474, "lng": 108.983534, "lat": 34.225493},
    "招旅家属院": {"time": 1606, "lng": 108.946906, "lat": 34.208033},
    "汉华城甜心广场": {"time": 1579, "lng": 108.997896, "lat": 34.207550},
    "盐湖研究所": {"time": 1583, "lng": 108.997437, "lat": 34.231502},
    "沙坡检察院家属院": {"time": 1313, "lng": 108.968525, "lat": 34.225275},
    "水厂家属院": {"time": 1915, "lng": 109.038782, "lat": 34.252887},
    "天地源大都会": {"time": 1739, "lng": 108.994159, "lat": 34.182798},
    "育才路272号": {"time": 1286, "lng": 108.957217, "lat": 34.226430},
    "曲江馨佳苑": {"time": 1751, "lng": 108.970584, "lat": 34.193810}
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

