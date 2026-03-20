import pandas as pd

df = pd.read_csv("xian_xiaoqu_data_tureprice_with_commute.csv")

community_data = {
    "延兴门延北西区": {"time": 1563, "lng": 109.002251, "lat": 34.232747},
    "金地翔悦天下": {"time": 1925, "lng": 109.014055, "lat": 34.205791},
    "玫瑰庄园": {"time": 1894, "lng": 108.993140, "lat": 34.198351},
    "真爱万科公园华府": {"time": 1801, "lng": 109.016125, "lat": 34.227363},
    "曲江九里西区": {"time": 1947, "lng": 109.017287, "lat": 34.203323},
    "后村嘉园": {"time": 1378, "lng": 108.969432, "lat": 34.226062},
    "孟村小区": {"time": 2013, "lng": 109.000298, "lat": 34.218616},
    "育才大厦": {"time": 1299, "lng": 108.957830, "lat": 34.226272}
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
