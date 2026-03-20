import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/lushaorong/code/beikedata/xian_xiaoqu_data_tureprice_with_commute.csv')

# 沣东旺城的正确坐标
fengdongwangcheng_lng = 108.761337
fengdongwangcheng_lat = 34.260382

# 导入MCP高德地图API工具
from mcp_amap_maps_maps_direction_driving import mcp_amap_maps_maps_direction_driving

# 处理已经有坐标但驾车时间可能不准确的小区
for index, row in df.iterrows():
    # 检查是否有坐标但没有驾车时间，或者驾车时间可能不准确（大于1000分钟的可能是错误数据）
    if pd.notna(row['community_lng']) and pd.notna(row['community_lat']):
        if pd.isna(row['commute_time_from_fengdongwangcheng']) or row['commute_time_from_fengdongwangcheng'] > 1000:
            try:
                # 计算从沣东旺城到该小区的驾车时间
                origin = f"{fengdongwangcheng_lng},{fengdongwangcheng_lat}"
                destination = f"{row['community_lng']},{row['community_lat']}"
                
                result = mcp_amap_maps_maps_direction_driving(origin=origin, destination=destination)
                
                # 解析结果，获取驾车时间（秒）
                if 'route' in result and 'paths' in result['route'] and len(result['route']['paths']) > 0:
                    duration = result['route']['paths'][0]['duration']
                    # 转换为分钟
                    duration_minutes = duration / 60
                    
                    # 更新CSV文件中的驾车时间
                    df.at[index, 'commute_time_from_fengdongwangcheng'] = duration_minutes
                    print(f"更新小区 {row['name']} 的驾车时间为 {duration_minutes:.2f} 分钟")
            except Exception as e:
                print(f"计算小区 {row['name']} 的驾车时间时出错: {e}")

# 保存更新后的数据
df.to_csv('/Users/lushaorong/code/beikedata/xian_xiaoqu_data_tureprice_with_commute.csv', index=False)
print("更新完成！")
