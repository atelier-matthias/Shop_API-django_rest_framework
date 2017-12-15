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

TODO

**Remove products to bucket**

TODO

**Create Order**

TODO

**Order Details**

TODO