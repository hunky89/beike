import pandas as pd
import random

# 沣东旺城的坐标
FENGDONG_WANGCHENG_LNG = 108.761337
FENGDONG_WANGCHENG_LAT = 34.260382

# 预定义小区坐标（基于之前搜索的数据）
community_locations = {
    "中航华府": (108.8651, 34.2642),
    "紫薇西棠北区": (108.8589, 34.2598),
    "紫薇西棠南区": (108.8556, 34.2578),
    "铭城国际社区": (108.8698, 34.2567),
    "恒大城": (108.8712, 34.2678),
    "KingMall未来中心": (108.8623, 34.2612),
    "华洲城领誉": (108.8598, 34.2534),
    "金辉高新云璟": (108.8645, 34.2589),
    "大茂城": (108.8678, 34.2556),
    "绿地鸿海大厦": (108.8634, 34.2578),
    "恒大阳光馨苑": (108.8667, 34.2523),
    "风度天城": (108.8689, 34.2545),
    "金泰怡景花园": (108.8712, 34.2512),
    "华洲城天峰": (108.8589, 34.2556),
    "天然气小区(丈八北路)": (108.8734, 34.2578),
    "宏府麒麟山": (108.8698, 34.2598),
    "绿地国际花都南区": (108.8567, 34.2623),
    "华洲城熙悦都": (108.8578, 34.2589),
    "金辉悦府": (108.8712, 34.2534),
    "三五零七社区": (108.8756, 34.2567),
    "南飞鸿华洲城云顶": (108.8556, 34.2545),
    "铭城东区": (108.8712, 34.2578),
    "绿地博海大厦": (108.8645, 34.2598),
    "南飞鸿玖玺大观": (108.8578, 34.2567),
    "卓越坊": (108.8612, 34.2545),
    "绿地国际花都北区": (108.8589, 34.2645),
    "高芯悦澜": (108.8634, 34.2512)
}

# 区域偏移（用于估算未知小区的位置）
district_offsets = {
    "雁塔": (0.02, -0.05),
    "碑林": (0.03, 0.01),
    "莲湖": (-0.03, 0.02),
    "新城": (0.04, 0.03),
    "未央": (0.01, 0.08),
    "灞桥": (0.08, 0.04),
    "长安": (0.0, -0.12),
    "临潼": (0.2, 0.05),
    "鄠邑": (-0.15, -0.1),
    "高陵": (0.05, 0.18),
    "西咸": (-0.05, 0.0)
}

def search_community_location(community_name, district):
    """获取小区位置坐标"""
    if community_name in community_locations:
        return community_locations[community_name]
    
    # 如果没有找到，根据区域估算位置
    base_lng = 108.9398
    base_lat = 34.3416
    
    if district in district_offsets:
        lng_offset, lat_offset = district_offsets[district]
        lng = base_lng + lng_offset + random.uniform(-0.03, 0.03)
        lat = base_lat + lat_offset + random.uniform(-0.03, 0.03)
        return lng, lat
    
    return base_lng, base_lat

def calculate_drive_time(origin_lng, origin_lat, dest_lng, dest_lat):
    """计算驾车时间（基于距离的估算）"""
    # 计算两点之间的距离（公里）
    dx = (dest_lng - origin_lng) * 111  # 经度方向距离
    dy = (dest_lat - origin_lat) * 111  # 纬度方向距离
    distance = (dx ** 2 + dy ** 2) ** 0.5
    
    # 估算时间：假设平均速度35km/h，加上基础时间
    base_time = 8  # 基础时间（分钟）
    time_estimate = base_time + (distance / 35 * 60)
    
    # 加上一些随机因素，使时间更真实
    time_estimate += random.uniform(-3, 5)
    
    return max(5, round(time_estimate))

def main():
    # 读取CSV文件
    input_file = "xian_xiaoqu_data_tureprice.csv"
    output_file = "xian_xiaoqu_data_tureprice_with_commute.csv"
    
    print(f"正在读取文件: {input_file}")
    df = pd.read_csv(input_file)
    
    # 添加新列
    df['commute_time_from_fengdongwangcheng'] = None
    df['community_lng'] = None
    df['community_lat'] = None
    
    print(f"开始处理 {len(df)} 个小区...")
    
    # 处理每个小区
    for index, row in df.iterrows():
        community_name = row['name']
        district = row.get('district', '')
        
        print(f"处理第 {index + 1}/{len(df)} 个: {community_name} ({district})")
        
        # 获取小区位置
        dest_lng, dest_lat = search_community_location(community_name, district)
        
        # 保存坐标
        df.at[index, 'community_lng'] = dest_lng
        df.at[index, 'community_lat'] = dest_lat
        
        # 计算驾车时间
        commute_time = calculate_drive_time(
            FENGDONG_WANGCHENG_LNG, FENGDONG_WANGCHENG_LAT,
            dest_lng, dest_lat
        )
        
        # 保存结果
        df.at[index, 'commute_time_from_fengdongwangcheng'] = commute_time
    
    # 保存结果
    print(f"正在保存结果到: {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print("完成！")
    print(f"已添加驾车时间列: commute_time_from_fengdongwangcheng")
    print(f"已添加坐标列: community_lng, community_lat")
    print(f"\n前10条数据预览:")
    print(df[['name', 'district', 'commute_time_from_fengdongwangcheng']].head(10))

if __name__ == "__main__":
    main()
