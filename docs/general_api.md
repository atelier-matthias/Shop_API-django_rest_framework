## API Flow

##### 1. Login / Registration
##### 2. Add products to bucket
##### 3. Confirm / create order from products in bucket
##### 4. Select payment method card/transfer/PayU
##### 5. Confirm payment

### Authorization and Authentication
Api is using django.auth app to security. 

**HEADERS REQUIRED**

* **CSRFTOKEN**
* **SESSIONID**


### Api General calls 

**User Registration**

*   **URL**
    **POST** <_/api/register_>
    
*   **BODY**

```json
{
	"username": "anakin",
	"password": "obiwansux",
	"first_name": "lord_anakin",
	"email": "a.skywalker@eathstar.im"
}
```
Where:

| Field  | Type | Required | Description  |
|---|---|---|---|
| `username`  | STRING | TRUE |   |
| `password`  | STRING | TRUE |   |
| `first_name`  | STRING | FALSE |   |
| `email`  | STRING | TRUE |   |

* **Success response**
    * **CODE** 200
    
```json
{
    "username": "anakin",
    "password": "pbkdf2_sha256$36000$xvzy4LeTXEol$y/Rkl8Qn8JQ49tc3pIzRjX7+CLEPIzL9RZLoHqVz5n0=",
    "first_name": "lord_anakin",
    "email": "a.skywalker@deathstar.im"
}
```
* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 400 | BAD REQUEST |  | Validation error |  |
| 409 | CONFLICT | 2001 | email/username already used | customer with this email is already in db |



**Login**


*   **URL**
    
    **POST** <_/api/login_>
    
*   **BODY**

```json
{
	"username": "anakin",
	"password": "obiwansux"
}
```

Where:

| Field  | Type | Required | Description  |
|---|---|---|---|
| `username`  | STRING | TRUE |   |
| `password`  | STRING | TRUE |   |


* **Success response**
    * **CODE** 200
    
```json
{
    "status": "OK",
    "user": "8b2de2bf-b04a-4674-bf92-f0e4c727720b"
}
```

* **Error Response**

| HTTP CODE | HTTP RESPONSE | CODE | MESSAGE | DETAILS | DESCRIPTION
|---|---|---|---|---|---|
| 404 | NOT FOUND | 3001 | user or password not match | Wrong password or username |



**Logout**


*   **URL**
    
    **GET** <_/api/logout_>
  
```json
{
    "status": "OK",
    "message": "user logout"
}
```