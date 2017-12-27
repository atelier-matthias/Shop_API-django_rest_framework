# PAYU API CALLS

**Create Order with PayU payments**

*   **URL**
    **PUT** <_/api/orders/`:order_uuid`/payu_>
    
*   **BODY**


Where:

| Field  | Type | Required | Description  |
|---|---|---|---|
| `order_uuid`  | STRING | TRUE |   |


* **Success response**
    * **CODE** 200
    
```json
{
    "orderId": "3DQNW5RWJH171217GUEST000P01",
    "status": {
        "statusCode": "SUCCESS"
    },
    "redirectUri": "https://merch-prod.snd.payu.com/pl/standard/co/summary?sessionId=UMZrWK2GisNj8nEx6wLAlou5cDIoBGcg&merchantPosId=307891&timeStamp=1513534677858&showLoginDialog=false&apiToken=bca0f27a3d72b5f4702a4c083291559fd8653866ff11d6a49836148b78adcd30"
}
```
* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 403 | FORBIDDEN | | Authentication credentials were not provided. |  |
| 404 | NOT FOUND | | Order not found |  |
