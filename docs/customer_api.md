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
