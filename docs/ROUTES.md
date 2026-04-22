# 路由設計文件 (ROUTES) - 校園停車way查詢系統

本文件列出系統中所有的頁面路由與 API 介面。

## 1. 路由總覽表格

| 功能模組 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | GET | `/` | `index.html` | 呈現首頁與主要綜合地圖介面 |
| **停車** | GET | `/api/parking/status` | — | 取得所有停車場最新狀態(車位數等)之 JSON |
| **停車** | GET | `/parking/pay` | `parking/pay.html` | 顯示輸入車牌的大型繳費表單 |
| **停車** | POST | `/parking/pay` | — | 接收車牌，查詢應繳金額並重導向確認頁 |
| **停車** | GET | `/parking/pay/confirm` | `parking/confirm.html` | 顯示繳費明細，供使用者點擊授權付款 |
| **停車** | POST | `/parking/pay/confirm`| — | 處理付款，更新 DB 並重導向至完成畫面 |
| **停車** | GET | `/parking/monthly` | `parking/monthly.html`| 顯示停車場月租申請表單 |
| **停車** | POST | `/parking/monthly` | — | 接收申請資料，存入 DB 並重導向 |
| **路況** | GET | `/api/route/drive` | — | 給定起訖點，回傳避開主要幹道壅塞的導航 JSON |
| **交管** | GET | `/api/events/traffic` | — | 取得目前的大型活動、交管封閉範圍的 JSON |
| **大眾運輸** | GET | `/api/transit/options`| — | 取得距校區較遠的替代停車點與接駁車推薦 JSON |
| **行人** | GET | `/api/route/walk` | — | 給定起訖點，回傳經過商店街/行人專用道的導航 JSON |

## 2. 路由詳細說明

### 2.1 主頁面路由 (`main_route.py`)
- **`GET /`**
  - **處理邏輯**：單純渲染首頁。
  - **輸出**：渲染 `index.html`。

### 2.2 停車路由 (`parking_route.py`)
- **`GET /api/parking/status`**
  - **處理邏輯**：呼叫 `ParkingLot.get_all()`。
  - **輸出**：回傳 JSON 格式的車位清單。
- **`GET /parking/pay`**
  - **處理邏輯**：顯示表單頁面。
  - **輸出**：渲染 `parking/pay.html`。
- **`POST /parking/pay`**
  - **輸入**：`license_plate` 表單欄位。
  - **處理邏輯**：在 `Payment` 表查詢該車牌未結清之訂單，計算總額並存入 session (或回傳)。
  - **輸出**：重導向至 `GET /parking/pay/confirm`。
- **`GET /parking/monthly`** 與 **`POST /parking/monthly`**
  - **處理邏輯**：處理月租申請邏輯，並建立 `MonthlyPass` 資料。

### 2.3 交管與車流路徑 (`traffic_route.py`)
- **`GET /api/route/drive`**
  - **輸入**：URL 參數 `origin` 與 `destination`。
  - **處理邏輯**：計算避開校門口與壅塞區域的最佳車行路徑（初期可 Mock 資料）。
  - **輸出**：回傳 JSON 路段點位 array。
- **`GET /api/events/traffic`**
  - **處理邏輯**：呼叫 `Event.get_all()` 獲取當前進行中的活動交管紀錄。
  - **輸出**：JSON 格式之活動清單。

### 2.4 大眾運輸與轉乘 (`transit_route.py`)
- **`GET /api/transit/options`**
  - **處理邏輯**：計算推薦轉乘客運或接駁車的地點。
  - **輸出**：回傳建議轉乘資訊的 JSON。

### 2.5 行人與商圈路徑 (`pedestrian_route.py`)
- **`GET /api/route/walk`**
  - **輸入**：URL 參數 `origin` 與 `destination`。
  - **處理邏輯**：規劃結合周邊商店街，並保障人流安全的步行路線（初期可 Mock 資料）。
  - **輸出**：JSON 路段點位 array。

## 3. Jinja2 模板清單
- `templates/base.html` (提供共通版面、導覽列、側邊欄及導入 Bootstrap/CSS/Map.js)
- `templates/index.html` (主系統地圖視覺化)
- `templates/parking/pay.html`
- `templates/parking/confirm.html`
- `templates/parking/monthly.html`
