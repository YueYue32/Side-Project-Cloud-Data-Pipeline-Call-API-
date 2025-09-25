# Side-Project-Cloud-Data-Pipeline-Call-API-
Side Project：雲端資料管線 (Cloud Data Pipeline) 基礎API呼叫使用


## 專案目標
建立一個簡單的 ETL Pipeline：
1. 從公開 API (比特幣價格) 抓取資料
2. 存進雲端儲存桶 (AWS S3)
3. 用查詢服務 (AWS Athena) 查詢

---

## 專案步驟
1.
申請https://aws.amazon.com/free/
  
免費額度：S3、Athena、Glue、QuickSight 都有基礎免費使用額度

---
  
2. 
- 進 AWS Console → 搜尋 **S3** → Create bucket

- Bucket name：`my-data-lake-bucket`

- 預設 設定即可 (記得選 **Region: ap-northeast-1 東京**，比較接近台灣)

---

3.
- 安裝 boto3
  ```
  pip install boto3 requests

執行 cloud_api.py

---
4. 用 Athena 查詢資料

- 進 AWS Console → 搜尋 **Athena**
- 設定 Query Result 存放在剛剛的 `my-data-lake-bucket`
- 建立 Table (Athena SQL)：Athena_sql
- 查詢最新價格：sql_price

---

5. Lambda 自動化 (排程管理)
- 進 AWS Console → 搜尋 **S3** → Create bucket

- Bucket name：`my-data-lake-bucket`

- 預設 設定即可 (記得選 **Region: ap-northeast-1 東京**，比較接近台灣)

- 建立 Lambda Function

- - 進入 **AWS Console → Lambda → Create function**
- 選擇：
    - **Author from scratch**
    - Function name: `fetchBitcoinPrice`
    - Runtime: **Python 3.9** (或更新版本)
- 建立完成後，進到 Lambda 編輯器

- Lambda_API.py 丟進去

- 1. 設定 IAM 權限

Lambda 要能存取 S3，所以要給它正確的 IAM Role：

1. 到 **Lambda → Configuration → Permissions**
2. 點擊 Execution role → Attach policy
3. 加上 **AmazonS3FullAccess**（或針對你特定的 bucket 給更精準的權限）

1. 測試 Lambda
- 點擊 **Test → Configure test event → Create**
- 執行一次 → 成功的話，S3 裡會出現 `raw/bitcoin_xxx.json`

1. 建立 CloudWatch Events (定時觸發)

現在 CloudWatch Events 整合到 **EventBridge**：

1. 到 **Amazon EventBridge → Rules → Create rule**
2. Rule name: `triggerBitcoinLambda`
3. 選擇 **Schedule** → **Cron 表達式**
    - 每 5 分鐘執行一次：`cron(0/5 * * * ? *)`
    - 每小時執行一次：`cron(0 * * * ? *)`
4. Target → 選擇剛剛的 Lambda `fetchBitcoinPrice`
5. 建立完成
