### Api Customer calls 

**Customer Profile**

*   **URL**
    **GET** <_/api/profile_>

* **Success response**
    * **CODE** 200
    
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "uuid": "a860895f-788d-4bb2-baa7-06c263ed8754",
            "username": "anakin",
            "first_name": "lord_anakin",
            "last_name": "",
            "email": "a.skywalker@deathstar.im",
            "phone": "",
            "city": ""
        }
    ]
}
```
* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 403 | FORBIDDEN | | Authentication credentials were not provided. |  |


**Update Customer Profile**

*   **URL**
    **PUT** <_/api/profile/`:customer_uuid`_>
    
*   **BODY**

```json
{
 
    "username": "anakin",
    "first_name": "lord_anakin",
    "last_name": "",
    "email": "a.skywalker@deathstar.im",
    "phone": "",
    "city": ""
}
```

Where:

| Field  | Type | Required | Description  |
|---|---|---|---|
| `username`  | STRING | TRUE |   |
| `first_name`  | STRING | FALSE |   |
| `email`  | STRING | TRUE |   |
| `phone`  | STRING | FALSE |   |
| `city`  | STRING | FALSE |   |


* **Success response**
    * **CODE** 200
    
```json
{
 
    "username": "anakin",
    "first_name": "lord_anakin",
    "last_name": "",
    "email": "a.skywalker@deathstar.im",
    "phone": "",
    "city": ""
}
```
* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 403 | FORBIDDEN | | Authentication credentials were not provided. |  |
| 400 | BAD REQUEST | | Validation error. |  |
| 409 | BAD REQUEST | 2001 | email already used |  |



**Change Customer Password**

*   **URL**
    **PUT** <_/api/profile/`:customer_uuid`/setpassword_>
    
*   **BODY**

```json
{
    "username": "anakin",
    "old_password": "obiwansux",
    "password": "onlydarkside"
}
```

Where:

| Field  | Type | Required | Description  |
|---|---|---|---|
| `username`  | STRING | TRUE |   |
| `old_password`  | STRING | TRUE |   |
| `password`  | STRING | TRUE |   |


* **Success response**
    * **CODE** 200
    
```json
{
    "password": "pbkdf2_sha256$36000$xA9wvVJPALHV$vQwQ0pdKmn8Yh9dZAZZJzgcdPZIeZVZyllujr0Ztvrc=",
    "username": "anakin"
}
```
* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 403 | FORBIDDEN | | Authentication credentials were not provided. |  |
| 404 | NOT FOUND | 3001 | user or password not match. |  |


**Product list**

*   **URL**
    **GET** <_/api/products?name=`:product_name`&type=`:product_type`_>
    
Where:

| Field  | Type | Required | Description  |
|---|---|---|---|
| `product_name`  | STRING | TRUE | product name  |
| `product_type`  | STRING | TRUE | product type  |
    
   
* **Success response**
    * **CODE** 200
    
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": {
        "561f3505-018f-4352-bcda-c6d00092eea1": {
            "status": "new",
            "name": "telewizor",
            "description": "LED TV",
            "price": "3000.00",
            "product_type": "rtv",
            "quantity": 9
        },
        "c7c6705d-9d18-4a70-a070-004fc5cfbc8e": {
            "status": "new",
            "name": "telefon",
            "description": "telefon komórkowy",
            "price": "1000.00",
            "product_type": "rtv",
            "quantity": 7
        }
    }
}
```


**Customer products in bucket**

*   **URL**
    **GET** <_/api/bucket_>
    
   
* **Success response**
    * **CODE** 200
    
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "quantity": 1,
            "product": "561f3505-018f-4352-bcda-c6d00092eea1",
            "value": "3000.00",
            "bucket_uuid": "dd5bf252-e9c6-47d4-83b4-401d57332337"
        }
    ]
}
```
* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 403 | FORBIDDEN | | Authentication credentials were not provided. |  |


**Add products to bucket**

*   **URL**
    **POST** <_/api/bucket_>
    
*   **BODY**

```json
{
    "quantity": null,
    "product": null
}
```   

Where:

| Field  | Type | Required | Description  |
|---|---|---|---|
| `quantity`  | INT | TRUE | number of quantity which user want to buy  |
| `product`  | STRING | TRUE | product UUID  |


* **Success response**
    * **CODE** 200
    
```json
{
    "customer": "8b2de2bf-b04a-4674-bf92-f0e4c727720b",
    "quantity": 2,
    "product": "c7c6705d-9d18-4a70-a070-004fc5cfbc8e",
    "value": 1000.0
}
```
* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 403 | FORBIDDEN | | Authentication credentials were not provided. |  |
| 409 | CONFLICT | 1042 | Product not avaliable |  |
| 409 | CONFLICT | 1041 | Product already in bucket |  |
| 409 | CONFLICT | 1043 | not enough products in magazines |  |


**Update quantity products to bucket**

*   **URL**
    **POST** <_/api/bucket/`:bucket_uuid`_>
    
*   **BODY**

```json
{
    "quantity": 2
}
```   

Where:

| Field  | Type | Required | Description  |
|---|---|---|---|
| `quantity`  | INT | TRUE | number of quantity which user want to buy  | If value == 0 -> destroy


* **Success response**
    * **CODE** 200
    
```json
{
    "quantity": 2
}
```
* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 403 | FORBIDDEN | | Authentication credentials were not provided. |  |
| 409 | CONFLICT | 1043 | not enough products in magazines |  |


**Remove products from bucket**

*   **URL**
    **DELETE** <_/api/bucket/`:bucket_uuid`_>

* **Success response**
    * **CODE** 200
    
```json
{
    "status": "OK",
    "message": "product removed"
}
```

* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 403 | FORBIDDEN | | Authentication credentials were not provided. |  |
| 404 | NOT FOUND | | not found |  |


**Create Order**

**Update quantity products to bucket**

*   **URL**
    **POST** <_/api/orders_>
    
*   **BODY**

```json
{
  "payment": "cash",
}
```   

Where:

| Field  | Type | Required | Description  |
|---|---|---|---|
| `payment`  | STRING | TRUE | payment method. Avaliable values - `CASH`, `CARD`, `PAYU`  | 


* **Success response**
    * **CODE** 200
    
```json
{
    "order_uuid": "df583417-eab9-4839-9569-001b17e4c785",
    "status": "new",
    "date_created": "2017-12-16T11:04:56.293906Z",
    "date_paid": null,
    "sum": "6000.00",
    "payment": "cash",
    "customer": "8b2de2bf-b04a-4674-bf92-f0e4c727720b"
}
```
* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 403 | FORBIDDEN | | Authentication credentials were not provided. |  |
| 400 | BAD REQUEST |  | invalid payment choice |  |
| 409 | CONFLICT | 1083 | bucket is empty |  |


**Order Details**

*   **URL**
    **GET** <_/api/orders/`:orders_uuid`_>
    

* **Success response**
    * **CODE** 200
    
```json
[
    {
        "order_uuid": "80ad25ca-048c-4a01-9ff7-ed690b9cc00f",
        "status": "new",
        "date_created": "2017-12-16T10:52:53.034063Z",
        "date_paid": null,
        "sum": "6000.00",
        "payment": "cash"
    },
    [
        {
            "order_product_uuid": "f8a4c317-b80c-48cd-9063-daa5069d5ce9",
            "quantity": 1,
            "value": "3000.00",
            "order": "80ad25ca-048c-4a01-9ff7-ed690b9cc00f",
            "product": "561f3505-018f-4352-bcda-c6d00092eea1"
        },
        {
            "order_product_uuid": "4c2a48be-3c40-4fb4-8e21-9b512bd19a9e",
            "quantity": 3,
            "value": "1000.00",
            "order": "80ad25ca-048c-4a01-9ff7-ed690b9cc00f",
            "product": "c7c6705d-9d18-4a70-a070-004fc5cfbc8e"
        }
    ]
]
```
* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 403 | FORBIDDEN | | Authentication credentials were not provided. |  |
| 404 | NOT FOUND |  | not found |  |


**Set Order Status Returned**

**Set Order Status Returned**

*   **URL**
    **POST** <_/api/orders/`:order_uuid`/set_canceled_>
    
*   **NO BODY NEED**
   

Where:

| Field  | Type | Required | Description  |
|---|---|---|---|
| `order_uuid`  | STRING | TRUE | order UUID  | 


* **Success response**
    * **CODE** 200
    
```json
{
    "status": "OK",
    "message": "updated"
}
```
* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 403 | FORBIDDEN | | Authentication credentials were not provided. |  |
| 404 | NOT FOUND |  | not found |  |
| 409 | CONFLICT | 1003 | only status `new`, `to_pay`, `paid` is avaliable to return |  |