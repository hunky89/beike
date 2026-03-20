import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/lushaorong/code/beikedata/xian_xiaoqu_data_tureprice_with_commute.csv')

# 定义小区数据
community_data = {
    "西影社区": {"time": 21.7, "lng": 108.973184, "lat": 34.224321},
    "三迪枫丹": {"time": 26.48, "lng": 109.002568, "lat": 34.188440},
    "招商依云曲江": {"time": 26.7, "lng": 108.999929, "lat": 34.182766},
    "曲江汉华城": {"time": 24.13, "lng": 108.997896, "lat": 34.207550},
    "陕西航天干休所": {"time": 22.18, "lng": 108.956695, "lat": 34.205220}
}

# 更新数据
for name, data in community_data.items():
    idx = df[df['name'] == name].index
    if len(idx) > 0:
        df.at[idx[0], 'commute_time_from_fengdongwangcheng'] = data['time']
        df.at[idx[0], 'community_lng'] = data['lng']
        df.at[idx[0], 'community_lat'] = data['lat']

# 保存更新后的数据
df.to_csv('/Users/lushaorong/code/beikedata/xian_xiaoqu_data_tureprice_with_commute.csv', index=False)

# 输出统计信息
total = len(df)
has_data = len(df