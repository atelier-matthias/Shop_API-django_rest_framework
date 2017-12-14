### Api Customer calls 

**Customer Profile**

*   **URL**
    **GET** <_/api/profile_>
    
*   **BODY**

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
    **POST** <_/api/profile/`:customer_uuid`_>
    
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