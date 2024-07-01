E-Commerce API Documentation
Overview
This API allows users to manage customers, customer accounts, products, and orders within an e-commerce platform. It supports various operations such as creating, reading, updating, and deleting entities, as well as order placement and tracking.

Endpoints
Customers
Create Customer

Endpoint: /customers
Method: POST
Description: Creates a new customer with attributes such as name, email, and phone number.
Read Customer

Endpoint: /customers/<id>
Method: GET
Description: Retrieves details of a specific customer based on their unique identifier (ID).
Update Customer

Endpoint: /customers/<id>
Method: PUT
Description: Updates the details of a customer identified by their ID, including name, email, and phone number.
Delete Customer

Endpoint: /customers/<id>
Method: DELETE
Description: Deletes a customer from the system based on their unique identifier (ID).
Customer Accounts
Create Customer Account

Endpoint: /customer_accounts
Method: POST
Description: Creates a new customer account with a unique username and a secure password.
Read Customer Account

Endpoint: /customer_accounts/<id>
Method: GET
Description: Retrieves details of a specific customer account based on its unique identifier (ID).
Update Customer Account

Endpoint: /customer_accounts/<id>
Method: PUT
Description: Updates the details of a customer account identified by its ID, including the username and password.
Delete Customer Account

Endpoint: /customer_accounts/<id>
Method: DELETE
Description: Deletes a customer account from the system based on its unique identifier (ID).
Products
Create Product

Endpoint: /products
Method: POST
Description: Adds a new product to the e-commerce database with attributes such as name and price.
Read Product

Endpoint: /products/<id>
Method: GET
Description: Retrieves details of a specific product based on its unique identifier (ID).
Update Product

Endpoint: /products/<id>
Method: PUT
Description: Updates the details of a product identified by its ID, including the name and price.
Delete Product

Endpoint: /products/<id>
Method: DELETE
Description: Deletes a product from the system based on its unique identifier (ID).
Orders
Place Order

Endpoint: /orders
Method: POST
Description: Allows customers to place a new order, specifying the products they wish to purchase and providing essential order details.
Retrieve Order

Endpoint: /orders/<id>
Method: GET
Description: Retrieves details of a specific order based on its unique identifier (ID), including the order date and associated products.
Track Order

Endpoint: /orders/<id>/track
Method: GET
Description: Allows customers to track the status and progress of their orders, providing information such as order dates and expected delivery dates.
