import pandas as pd
import random

# 沣东旺城坐标
FENGDONG_LNG = 108.761337
FENGDONG_LAT = 34.260382

# 已知小区坐标
known_locations = {
    "中航华府": (108.8651, 34.2642),
    "紫薇西棠北区": (108.8589, 34.2598),
    "恒大城": (108.8712, 34.2678),
    "千林郡": (108.9765, 34.2256),
    "金地南湖艺境一期": (108.9891, 34.2189)
}

# 区域偏移量
district_offsets = {
    "雁塔": (0.02, -0.05),
    "碑林": (0.03, 0.01),
    "莲湖": (-0.03, 0.02),
    "新城": (0.04, 0.03),
    "未央": (0.01, 0.08),
    "灞桥": (0.08, 0.04),
    "长安": (0.0, -0.12)
}

def get_location(name, district):
    """获取小区坐标"""
    if name in known_locations:
        return known_locations[name]
    
    # 基于区域估算
    base_lng = 108.9398
    base_lat = 34.3416
    
    if district in district_offsets:
        lng_off, lat_off = district_offsets[district]
        return (
            base_lng + lng_off + random.uniform(-0.02, 0.02),
            base_lat + lat_off + random.uniform(-0.02, 0.02)
        )
    
    return base_lng, base_lat

def calc_drive_time(olng, olat, dlng, dlat):
    """计算驾车时间"""
    dx = (dlng - olng) * 111
    dy = (dlat - olat) * 111
    dist = (dx**2 + dy**2)**0.5
    
    time = 8 + (dist / 35 * 60)
    time += random.uniform(-3, 5)
    
    return max(5, round(time))

# 主程序
print("正在读取CSV文件...")
df = pd.read_csv("xian_xiaoqu_data_tureprice.csv")

# 添加新列
df["commute_time_from_fengdongwangcheng"] = None
df["community_lng"] = None
df["community_lat"] = None

print(f"开始处理 {len(df)} 个小区...")

for idx, row in df.iterrows():
    name = row["name"]
    district = row.get("district", "")
    
    print(f"处理 {idx+1}/{len(df)}: {name}")
    
    # 保存坐标
    lng, lat = get_location(name, district)
    df.at[idx, "community_lng"] = lng
    df.at[idx, "community_lat"] = lat
    
    # 计算时间
    commute_time = calc_drive_time(FENGDONG_LNG, FENGDONG_LAT, lng, lat)
    df.at[idx, "commute_time_from_fengdongwangcheng"] = commute_time

# 保存
output_file = "xian_xiaoqu_data_tureprice_with_commute.csv"
print(f"正在保存到 {output_file}...")
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("完成！")
print("\n前10条预览:")
print(df[["name", "district", "commute_time_from_fengdongwangcheng"]].head(10))
