import pandas as pd

# 读取原始CSV
df = pd.read_csv("xian_xiaoqu_data_tureprice.csv")

# 添加新列
df["commute_time_from_fengdongwangcheng"] = None
df["community_lng"] = None
df["community_lat"] = None

# 已获取的小区数据（使用MCP高德地图API）
community_data = {
    "中航华府": {"lng": 108.855594, "lat": 34.244746, "time": 22},
    "紫薇西棠北区": {"lng": 108.829407, "lat": 34.242841, "time": 19},
    "紫薇西棠南区": {"lng": 108.829715, "lat": 34.240707, "time": 19},
    "铭城国际社区": {"lng": 108.856496, "lat": 34.246765, "time": 22},
    "恒大城": {"lng": 108.865529, "lat": 34.246783, "time": 22},
    "华洲城领誉": {"lng": 108.846997, "lat": 34.250512, "time": 17},
    "金辉高新云璟": {"lng": 108.866262, "lat": 34.240298, "time": 25},
    "恒大阳光馨苑": {"lng": 108.863268, "lat": 34.251705, "time": 18},
    "风度天城": {"lng": 108.868888, "lat": 34.238363, "time": 24},
    "金泰怡景花园": {"lng": 108.847200, "lat": 34.240306, "time": 19},
    "华洲城天峰": {"lng": 108.848347, "lat": 34.244189, "time": 21},
    "宏府麒麟山": {"lng": 108.861713, "lat": 34.246740, "time": 21},
    "绿地国际花都南区": {"lng": 108.840275, "lat": 34.240421, "time": 19},
    "华洲城熙悦都": {"lng": 108.847542, "lat": 34.246778, "time": 20},
    "金辉悦府": {"lng": 108.866631, "lat": 34.251077, "time": 21},
    "三五零七社区": {"lng": 108.865840, "lat": 34.249121, "time": 22},
    "南飞鸿华洲城云顶": {"lng": 108.846116, "lat": 34.242619, "time": 20},
    "南飞鸿玖玺大观": {"lng": 108.850406, "lat": 34.243257, "time": 20},
    "卓越坊": {"lng": 108.832358, "lat": 34.243313, "time": 18},
    "绿地国际花都北区": {"lng": 108.840367, "lat": 34.243281, "time": 18},
    "高芯悦澜": {"lng": 108.851264, "lat": 34.239586, "time": 19},
    "千林郡": {"lng": 108.963495, "lat": 34.180746, "time": 32},
    "金地南湖艺境一期": {"lng": 108.998631, "lat": 34.185330, "time": 35}
}

# 填充数据
for idx, row in df.iterrows():
    name = row["name"]
    if name in community_data:
        data = community_data[name]
        df.at[idx, "commute_time_from_fengdongwangcheng"] = data["time"]
        df.at[idx, "community_lng"] = data["lng"]
        df.at[idx, "community_lat"] = data["lat"]

# 保存结果
output_file = "xian_xiaoqu_data_tureprice_with_commute.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"已保存到 {output_file}")
print("\n前30条数据预览:")
print(df[["name", "district", "commute_time_from_fengdongwangcheng"]].head(30))
print(f"\n已填充 {len(community_data)} 个小区的真实驾车时间")
print("剩余小区需要继续使用MCP高德地图API处理")
