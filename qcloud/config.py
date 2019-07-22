from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

bucket = 'sirat-1254172731'
secret_id = 'AKIDIUfga3bAYovsjSLZSBlyNfnnbeXNrSnz'
secret_key = 'Wt55yujQzPemmgS8dRBiNrhMXZXlohP1'
region = 'ap-chengdu'  # 替换为用户的region
token = None

# 获取配置对象
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
client = CosS3Client(config)
