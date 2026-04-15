# 流程圖與路由對照文件 (FLOWCHART) - 校園停車way查詢系統

本文件基於 PRD 的五大核心功能與已經定義的架構，視覺化展現系統的使用者操作體驗 (User Flow) 以及系統底層互動邏輯 (System Flow)，並定出初始的功能 URL 路由表。

---

## 1. 使用者流程圖 (User Flow)

描述使用者進入系統首頁後，根據不同的行車或步行情境所選擇的互動路徑。

```mermaid
flowchart LR
    Start([使用者到達系統首頁 / 綜合地圖]) --> Decide{選擇主要功能？}

    Decide -->|1. 停車查詢繳費| Parking[查詢停車場空位]
    Parking --> Choice_Parking{找到可用車位？}
    Choice_Parking -->|有| Navi_Park[取得至停車場導航]
    Choice_Parking -->|已離場| Pay[線上繳交停車費 / 申請月租]

    Decide -->|2. 車流與路況| Traffic[即時路況圖層切換]
    Traffic --> Route_Plan[自動規劃避走壅塞路段的行駛路線]

    Decide -->|3. 大型活動管制| Event[查看大型活動交通資訊]
    Event --> Event_Guide[獲取進出場特定引導動線或交管區域]

    Decide -->|4. 大眾運具轉乘| Transit[查詢周邊遠端停車場]
    Transit --> Transit_Guide[轉乘大眾接駁公車進入校區]

    Decide -->|5. 行人/商圈導流| Pedestrian[切換為路人導航模式]
    Pedestrian --> Walker_Route[走訪行人專用道避開車潮]
    Walker_Route --> Shopping[引導穿越逢甲商圈兼顧安全與消費]
```

---

## 2. 系統序列圖 (Sequence Diagram)

這裡以「使用者線上繳交停車費」的流程為例，展示前端瀏覽器、後端 Flask 控制器與 SQLite 資料庫間的互動細節。

```mermaid
sequenceDiagram
    actor User as 使用者 (學生)
    participant Browser as 瀏覽器 (前端)
    participant Flask as Flask Route
    participant Model as PaymentModel
    participant DB as SQLite

    User->>Browser: 在系統裡點擊「繳交停車費」並輸入車牌
    Browser->>Flask: POST /parking/pay (帶著車牌資訊)
    Flask->>Model: 查詢此車牌的未繳費紀錄
    Model->>DB: SELECT * FROM payments WHERE license_plate=?
    DB-->>Model: 回傳多筆/單筆未繳費資料
    Model-->>Flask: 計算應繳總額
    Flask-->>Browser: 回傳「確認繳費頁面 (包含金額)」
    User->>Browser: 點選確認並授權第三方支付付款
    Browser->>Flask: POST /parking/pay/confirm
    Flask->>Model: 將對應訂單設定為「已付款」
    Model->>DB: UPDATE payments SET status='paid' ...
    DB-->>Model: 更新成功
    Model-->>Flask: 確認狀態更新
    Flask-->>Browser: 重導向至繳款成功感謝頁
    Browser-->>User: 畫面顯示「繳費成功，謝謝」
```

---

## 3. 功能清單與路由對照表

開發初期依據功能切割，預計的 HTTP 路由、方法及作用。

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **系統首頁 (綜合地圖)** | `/` | GET | 預設視角，呈現地圖介面、基礎路況、鄰近停車場分布 |
| **查看停車場狀態** | `/api/parking/status` | GET | 抓取各個停車場最新資訊（剩餘車位數、費率等） |
| **線上繳交停車費** | `/parking/pay` | GET, POST | GET 顯示車牌輸入介面；POST 處理查詢與確認繳納表單 |
| **智慧行車導航** | `/api/route/drive` | GET | 給定起訖點，回傳避開主要幹道壅塞路段的導航座標 |
| **大眾運輸轉乘建議** | `/api/transit/options` | GET | 查詢距校區較遠的「替代停車點」與「接駁車」資訊 |
| **智慧行人路線推薦** | `/api/route/walk` | GET | 給定起訖點，提供走私房小路/商店街的安全行人專用道路線 |
| **大型活動交管查詢** | `/api/events/traffic` | GET | 取得近期的交管快訊、路障封鎖區域與建議引導路線 |
