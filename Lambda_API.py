import boto3
import requests
import json
from datetime import datetime

def lambda_handler(event, context):
    # Step 1: 抓取比特幣價格 (CoinDesk API)
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(url)
    data = response.json()

    # Step 2: 產生檔案名稱
    filename = f"bitcoin_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Step 3: 上傳到 S3
    s3 = boto3.client("s3")
    bucket_name = "my-data-lake-bucket"  # 替換成你的 S3 bucket 名稱
    s3.put_object(
        Bucket=bucket_name,
        Key=f"raw/{filename}",
        Body=json.dumps(data)
    )

    print(f"✅ Uploaded {filename} to s3://{bucket_name}/raw/")
    return {"status": "success", "file": filename}
