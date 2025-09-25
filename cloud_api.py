import boto3
import requests
import json
from datetime import datetime

# Step 1: 抓取比特幣即時價格
url = "https://api.coindesk.com/v1/bpi/currentprice.json"
response = requests.get(url)
data = response.json()

# Step 2: 存成檔案
filename = f"bitcoin_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, "w") as f:
    json.dump(data, f)

# Step 3: 上傳到 S3
s3 = boto3.client("s3")
bucket_name = "my-data-lake-bucket"
s3.upload_file(filename, bucket_name, f"raw/{filename}")

print(f"✅ Uploaded to s3://{bucket_name}/raw/{filename}")