import pandas as pd
import requests

# IPinfo API URL
api_url = "https://ipinfo.io/{}?token=XXX"

# 替换成你的API密钥
api_key = "XXX"

# 读取Excel文件
excel_file = "ip_list.xlsx"

# 加载Excel文件到DataFrame
df = pd.read_excel(excel_file)

# 获取IP地址列
ip_list = df['IP'].tolist()

# 批量查询IP归属地
def get_ip_location(ip, api_key):
    response = requests.get(api_url.format(ip, api_key))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "data": response.text}

# 创建空列表存储查询结果
results = []

for ip in ip_list:
    location_info = get_ip_location(ip, api_key)
    if 'error' in location_info:
        result = {
            "IP": ip,
            "Error": location_info['error'],
            "Message": location_info['data']
        }
    else:
        result = {
            "IP": ip,
            "City": location_info.get("city", "N/A"),
            "Region": location_info.get("region", "N/A"),
            "Country": location_info.get("country", "N/A"),
            "Org": location_info.get("org", "N/A")
        }
    results.append(result)

# 使用pandas创建数据框
result_df = pd.DataFrame(results)

# 将查询结果保存为新的Excel文件
output_file = "ip_locations_result.xlsx"
result_df.to_excel(output_file, index=False)

print(f"Results saved to {output_file}")
