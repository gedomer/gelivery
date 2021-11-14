Common
-----------

Common HTTP Status

| Code | Status | Description |
|------|--------|-------------|
| 400  | Bad Request | Server cannot or will not process the request |
| 404  | Not Found |  Resource Not Found |
| 500  | Internal Server Error | Server side issue occurred. Please contact administrator |


List all orders
-----------

GET /api/orders/

Parameters:
  - status: string, not required

Sample Response

HTTP Status Code: 200 (OK)


``` json

  [
      {
        "pk": "921a6266-4h03-47af-a410-25f6743g207c",
        "status": "delivered",
        "created_at": "2021-11-14T11:21:53.261174Z",
        "order_items": [
          {
            "food": 2,
            "quantity": 21,
            "amount": "2.000000"
          }
        ]
      },
      {
        "uid": "1a59bc9d-5368-4913-42c5-f17eee2804d4",
        "status": "cancelled",
        "created_at": "2021-11-13T10:11:43.361174Z",
        "order_items": [
          {
            "food": 1,
            "quantity": 21,
            "amount": "5.000000"
          }
        ]
      },
  ]

```

Create an order
-----------

POST /api/create

Sample Request

``` json

  {
    "address": "John Doe 123 Main St Anytown, USA",
    "restaurant": 1,
    "order_items": [
      {
        "food": 2,
        "quantity": 21,
        "amount": 2
      }
    ]
  }

 ```

Sample Response

HTTP Status Code: 201

``` json

  {
    "message": "order_created",
    "order_id": "cc01cb7e-78a9-4544-a0df-ba161dbdce7c"
  }

```

Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 400  | Bad Request |  There are one or more errors in request value |


Complete an order
-----------

POST /api/order-complete/

Sample Request

``` json

  {
    "order_id": "cc01cb7e-78a9-4544-a0df-ba161dbdce7c"
  }

```

Sample Response

HTTP Status Code: 201 (OK)

``` json

  {
    "order_id": "cc01cb7e-78a9-4544-a0df-ba161dbdce7c"
  }

```

Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 400  | Bad Request |  There are one or more errors in request value |
| 404  | Not Found | Resource not found. |

