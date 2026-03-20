import pandas as pd
import time

# 沣东旺城坐标
FENGDONG_COORDS = "108.761337,34.260382"

def main():
    # 读取CSV文件
    df = pd.read_csv('xian_xiaoqu_data_tureprice_with_commute.csv')
    
    # 找出未处理的小区
    unprocessed = df[df['commute_time_from_fengdongwangcheng'].isna()]
    print(f"总数据量: {len(df)}")
    print(f"已处理记录数: {df['commute_time_from_fengdongwangcheng'].notna().sum()}")
    print(f"未处理记录数: {len(unprocessed)}")
    print()
    
    # 显示接下来要处理的3组小区（共30个）
    print("接下来要处理的小区列表：")
    print("=" * 80)
    
    for i in range(min(30, len(unprocessed))):
        row = unprocessed.iloc[i]
        group_num = (i // 10) + 1
        idx_in_group = (i % 10) + 1
        print(f"第{group_num}组-{idx_in_group:02d}. {row['name']} (索引: {row.name})")
    
    print("=" * 80)
    print()
    print("提示：")
    print("1. 请使用MCP工具手动获取上述小区的坐标和驾车时间")
    print("2. 获取完成后，创建一个字典包含所有小区数据")
    print("3. 然后运行更新脚本将数据保存到CSV")
    print()

def update_csv(community_data):
    """更新CSV文件的函数"""
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
    
    df.to_csv('xian_xiaoqu_data_tureprice_with_commute.csv', index=False, encoding='utf-8-sig')
    
    print(f'更新了 {updated_count} 条记录')
    print(f'总数据量: {len(df)}')
    processed_count = df['commute_time_from_fengdongwangcheng'].notna().sum()
    print(f'已处理记录数: {processed_count}')
    print(f'未处理记录数: {len(df) - processed_count}')

if __name__ == "__main__":
    main()
