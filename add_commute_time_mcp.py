import pandas as pd
import time

# 沣东旺城坐标
FENGDONG_LNG = 108.761337
FENGDONG_LAT = 34.260382

def get_community_location(name, district):
    """使用MCP高德地图获取小区坐标"""
    try:
        address = f"西安{district}{name}"
        result = mcp_amap-maps_maps_geo(address=address, city="西安")
        if result and result.get("geocodes") and len(result["geocodes"]) > 0:
            location = result["geocodes"][0]["location"]
            lng, lat = map(float, location.split(","))
            return lng, lat
    except Exception as e:
        print(f"    获取坐标失败: {e}")
    return None, None

def get_drive_time(olng, olat, dlng, dlat):
    """使用MCP高德地图获取驾车时间"""
    try:
        origin = f"{olng},{olat}"
        destination = f"{dlng},{dlat}"
        result = mcp_amap-maps_maps_direction_driving(origin=origin, destination=destination)
        if result and result.get("route") and result["route"].get("paths") and len(result["route"]["paths"]) > 0:
            duration = result["route"]["paths"][0]["duration"]
            return round(duration / 60)
    except Exception as e:
        print(f"    获取驾车时间失败: {e}")
    return None

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
    
    # 获取小区坐标
    lng, lat = get_community_location(name, district)
    if lng and lat:
        df.at[idx, "community_lng"] = lng
        df.at[idx, "community_lat"] = lat
        
        # 计算驾车时间
        commute_time = get_drive_time(FENGDONG_LNG, FENGDONG_LAT, lng, lat)
        if commute_time:
            df.at[idx, "commute_time_from_fengdongwangcheng"] = commute_time
            print(f"    驾车时间: {commute_time}分钟")
    else:
        print(f"    无法获取坐标")
    
    # 避免请求过快
    time.sleep(0.5)

# 保存
output_file = "xian_xiaoqu_data_tureprice_with_commute.csv"
print(f"正在保存到 {output_file}...")
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("完成！")
print("\n前10条预览:")
print(df[["name", "district", "commute_time_from_fengdongwangcheng"]].head(10))
