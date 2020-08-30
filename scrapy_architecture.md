# Architecture overview

## Data Flow

![scrapy Architecture ](scrapy_architecture_02.png)

1. Eegine 從 Spider 取得最初要爬取的 Requests (A)

2. Engine 在 Scheduler 中排程 Requests (A)，同時請求 Scheduler 下一個要爬取的 Requests (如果沒有其他 Requests 在排程中，就會是 Requests A，或者是其他的 Requests B)

3. Scheduler 回傳下一個要爬取的 Requests (A/B) 給 Engine

4. Engine 透過 Downloader Middlewares (參見 process_request()) 把 Requests (A/B) 送到 Downloader

5. 一旦頁面下載完成，Downloader 會產生帶有該頁面的 Response，並且透過 Downloader Middlewares (參見 process_response()) 將 Response 傳送給 Engine

6. Engine 接收 Downloader 發送來的 Response，並且透過 Spider Middlewares (參見 process_spider_input) 傳送 Response 到 Spider 進行處理

7. Spider 處理完 Response 之後，將處理完的 items 與後續的的新 Requests (C)，透過 Spider Middlewares (參見 process_spider_output) 回傳給 Engine

8. Engine 傳送處理完的 items 給 Item Pipelines，同時傳送 Spider 回傳的新 Requests (C) 給 Scheduler，並向 Scheduler 請求下一個要爬取的 Requests (D)

9. 重 Step 2 重複整個流程直到 Scheduler 中沒有 Requests

## Components

### Scrapy Engine

+ Engine 負責控制整個系統元件之間的資料流 (Data Flow)，並且當某些行為 (actions) 發生時觸發事件

+ 詳細的訊息可以參考上面的 [Data Flow](#data-flow)

### Scheduler

+ Scheduler 接收 Engine 送來的 Requests，將 Requests 排入佇列中，以便之後 Engine 請求這些 Requests 時，輸送 Requests 到 Engine

### Downloader

+ Downloader 負責獲取網頁，並將網頁書送給 Engine，Engine 在輸送給 Spider

### Spiders

+ Spider 是由 Scrapy 使用者撰寫的自訂類別，來解析 Response 並從 Reponse 中提取 [Item][1]，或者追加額外的 Requests

+ 詳細的訊息可以參考 [Spider][2]

### Item Pipeline

+ 一旦 Items 被 Spider 提取 (或被 scrape)，Item Pipeline 會負責處理 Items

+ 典型的任務包括資料清理、資料驗證、與資料持續性 (Persistence)，像是將 Items 儲存到資料庫

+ 詳細的訊息可以參考 [item Pipeline][3]

### Downloader Middlewares

+ Downloader Middlewares 是位於 Engine 與 Downloader 之間特殊的 [Hooks][4]，負責處理從 Engine 傳遞到 Downloader 的 Requests，以及處理從 Downloader 傳遞到 Engine 的 Response

+ 使用 Downloader Middlewares 時機

    + 在 Requests 發送到 Downloader 之前先進行處理，也就是 Scrapy 發送 Requests 到網站之前

    + 在傳遞給 Sipder 之前改變接收到的 Response

    + 發送新的 Reuqests 取代 傳遞接收的 Response 給 Spider

    + 傳遞 Response 給 Spiser，而沒有獲取網頁

    + 默默的丟棄一些 Requests

+ 詳細的訊息可以參考 [Downloader Middleware][5]

### Spider Middlewares

+ Spider Middlewares 是位於 Engine 與 Spider 之間特殊的 [Hooks][4]，並且可以處理 Spider 的輸入 (Response) 與 輸出 (Item 與 Requests)

+ 使用 Spider Middlewares 時機

    + Spider Callback 輸出的後期處理，改變、新增、刪除 Requests 或 Items

    + start_requests() 的後期處理

    + 處理 Spider 的例外 (Exceptions)

    + 根據 Response 的內容，對某些 Requests 調用 errback 而不是 callback

+ 詳細的訊息可以參考 [Spider Middlewares][6]

[1]: https://docs.scrapy.org/en/latest/topics/items.html#topics-items "Items"

[2]: https://docs.scrapy.org/en/latest/topics/spiders.html#topics-spiders "Spider"

[3]: https://docs.scrapy.org/en/latest/topics/item-pipeline.html#topics-item-pipeline "Item Pipeline"

[4]: https://zh.wikipedia.org/wiki/%E9%92%A9%E5%AD%90%E7%BC%96%E7%A8%8B "Hooking"

[5]: https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#topics-downloader-middleware "Downloader Middleware"

[6]: https://docs.scrapy.org/en/latest/topics/spider-middleware.html#topics-spider-middleware "Spider Middlewares"