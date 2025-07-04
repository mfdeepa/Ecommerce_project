## Overview
This project is a fully functional e-commerce platform designed to showcase the implementation of modern software development principles, including the MVT architecture, robust database schema, modular services, and third-party payment gateway integration. The platform includes essential features such as user authentication, product catalog management, shopping cart functionality, order management, and payment processing using Stripe.I have created micro service and interate all with user service and also create Integration service where all service is connected with each other.

## Features
1. **User Management:**
    - User signup
    - User registration and login
    - User logout
    - User validate token
    - Get all user
    - Get user by id
    - Role-based access control

2. **Product Service:**
    - Product catalog with categories and role
    - Category management
    - Get product by all user 
    - Create,Upadte, delete product category is need authentication via user service with token 

3. **Cart Service:**
    - Add, update, and remove items from the cart with token authentication
    - Display cart total and individual item prices

4. **Order Service:**
    - Order placement and summary with token authentication
    - Integration with payment gateway (Stripe) for secure transactions

5. **Payment Service:**0
    - Integrate with user service and authenticate via token 
    - Stripe checkout session integration
    - Handling payment success and failure scenarios

6. **Database Design:**
    - Relational database schema optimized with foreign keys and indexing
    - Scalable and normalized schema for efficient data retrieval

7. **Error Handling:**
    - Custom exceptions for meaningful error messages
    - Graceful handling of runtime errors

## Technologies Used
1. **Backend:**
    - Python
    - Django (MOdel, View, and Template)

2. **Database:**
    - MySQL with relational schema
    - Indexing and foreign key constraints

3. **Payment Gateway:**
    - Stripe for secure and seamless payment processing

4. **Frontend:**
    - Not explicitly implemented, only created html page for getting Oauth token in user service for further validation

5. **Tools and Libraries:**
    - ORM(object management mapper)
    - MVT Architecture (Model, View, Template)
    - Admin Panel
    - Url Routing
    - Middleware
    - Third party liabraries intsalled like Authentication and authorization, django rest framework 
    - Python decouple (.env), django-cors-headers, django-environ, httpx or requests
    - Payment Gateway 



## Folder Structure (Based on MTV Pattern)
```markdown
Ecommerce
├── docs
│   ├── api-docs
│   ├── class-diagram
│   ├── shema-diagram
│   └── postman-collection
├──.idea
|
├── cart
|    ├── .venv
│    ├── cart
│    │   ├── __init__.py
|    |   ├── asgi.py
|    |   ├── setting.py
|    |   ├── urls.py
|    |   ├── wsgi.py
│    ├── carts
│    │   ├── migrations
│    │   │   ├── – -
│    |   ├── serializer
│    │   │   ├── – -
│    │   ├── services
│    |   │   │   ├── – -
│    |   ├── view
│    │   │   ├── – -
│    |   |── __init__.py
│    |   ├── admin.py
│    |   |── models.py
│    |   ├── test.py
│    |   |── urls.py
│    |   |── views.py
│    |   ├── doc
│    │   └──   ├── – -
|    |      
│    |──templates
│    |──.gitignore
│    |──db
│    |──manage.py
|    |          
│    |── README.md
|    |
|    |  
├── integrationService
│   |── integrationService
│   │    ├── .idea
|   |    ├── .venv
│   │    ├────────api
│   │    |      │   ├── migrations
│   │    |      │   │   ├── – -
│   │    |      │   ├── services
│   │    |      │   │   ├── - -
│   │    |      │   ├── views
│   │    |      │   │   ├── - -
│   │    |      │   └── └──
│   │    |      |── __init__.py
│   │    |      ├── admin.py
│   │    |      ├── apps.py
|   |    |      ├── models.py
|   |    |      ├── service_caller.py
|   |    |      ├── test.py
|   |    |      ├── urls.py
|   |    |      └── views.py
│   │    ├──integrationService
│   │    |     ├── __init__.py
|   |    |     ├── asgi.py
|   |    |     ├── models.py
|   |    |     ├── setting.py
|   |    |     ├── urls.py
|   |    |     └── wsgi.py
│   │    |──templates
|   |    ├── db
|   |    ├── manage.py
|   |    └── README.md
|   |
├── orderService
|    ├── .idea
|    ├── .venv
│    ├── orderService
│    │   ├── __init__.py
|    |   ├── asgi.py
|    |   ├── setting.py
|    |   ├── urls.py
|    |   ├── wsgi.py
│    ├── orderServices
│    │   ├── migrations
│    │   │   ├── – -
│    |   ├── serializer
│    │   │   ├── – -
│    │   ├── services
│    |   │   │   ├── – -
│    |   ├── view
│    │   │   ├── – -
│    |   |── __init__.py
│    |   ├── admin.py
│    |   ├── apps.py
│    |   |── models.py
│    |   ├── test.py
│    |   |── urls.py
│    |   |── views.py
│    │   └──   ├── – -
|    |      
│    |──templates
│    |──.gitignore
│    |──db
│    |──manage.py
│    |──requirement.txt           
│    └── README.md
|
├── paymentserEommerce
│   |── paymentSerEcommerce
│   │    ├── .idea
|   |    ├── .venv
│   │    ├── paymentecommerce
│   │    |      │   ├── migrations
│   │    |      │   │   ├── – -
│   │    |      │   ├── models
│   │    |      │   │   ├── – -
│   │    |      │   ├── paymentGateway
│   │    |      │   │   ├── – -
│   │    |      │   ├── serializer
│   │    |      │   │   ├── - -
│   │    |      │   ├── services
│   │    |      │   │   ├── - -
│   │    |      │   ├── views
│   │    |      │   │   ├── - -
│   │    |      │   └── └──
│   │    |      |── __init__.py
│   │    |      ├── admin.py
│   │    |      ├── apps.py
|   |    |      ├── models.py
|   |    |      ├── test.py
|   |    |      ├── urls.py
|   |    |      └── views.py
│   │    ├── paymentSerEcommerce
│   │    |     ├── __init__.py
|   |    |     ├── asgi.py
|   |    |     ├── models.py
|   |    |     ├── setting.py
|   |    |     ├── urls.py
|   |    |     └── wsgi.py
│   │    |──templates
|   |    ├── db
|   |    ├── manage.py
|   |    └── README.md
|   |
├── product
│   |── djangoProduct
│   │    ├── .idea
|   |    ├── .venv
│   │    ├── djangoProject
│   │    |     ├── migrations
│   │    |     ├── __init__.py
│   │    |     ├── admin.py
|   |    |     ├── asgi.py
|   |    |     ├── models.py
|   |    |     ├── setting.py
|   |    |     ├── urls.py
|   |    |     ├── wsgi.py
│   │    ├── productservice
│   │    |      │   ├── adapter
│   │    |      │   │   ├── – -
│   │    |      │   ├── client
│   │    |      │   │   ├── – -
│   │    |      │   ├── exception
│   │    |      │   │   ├── – -
│   │    |      │   ├── migrations
│   │    |      │   │   ├── – -
│   │    |      │   ├── serializers
│   │    |      │   │   ├── - -
│   │    |      │   ├── services
│   │    |      │   │   ├── - -
│   │    |      │   ├── utlis
│   │    |      │   │   ├── - -
│   │    |      │   ├── views
│   │    |      │   │   ├── - -
│   │    |      │   └── └──
│   │    |      |── __init__.py
│   │    |      ├── admin.py
│   │    |      ├── apps.py
|   |    |      ├── models.py
|   |    |      ├── test.py
|   |    |      └── urls.py
│   │    |──templates
│   │    ├──.env 
│   │    ├── .gitignore
|   |    ├── db
|   |    ├── manage.py
|   |    ├── requirements.txt
|   |    └── README.md
│   |     
│   |      
│   |    
├── userService
│   |── userService
│   │    ├── .idea
|   |    ├── .venv
|   |    ├── static
│   │    ├── userService
│   │    |     ├── __int__.py
│   │    |     ├── asgi.py
│   │    |     ├── env.env
|   |    |     ├── setting.py
|   |    |     ├── urls.py
|   |    |     ├── view.py
|   |    |     ├── wsgi.py
│   │    ├── userservices
│   │    |      │   ├── exception
│   │    |      │   │   ├── – -
│   │    |      │   ├── migrations
│   │    |      │   │   ├── – -
│   │    |      │   ├── serializer
│   │    |      │   │   ├── - -
│   │    |      │   ├── services
│   │    |      │   │   ├── - -
│   │    |      │   ├── views
│   │    |      │   │   ├── - -
│   │    |      │   └── 
│   │    |      |── __init__.py
│   │    |      ├── admin.py
│   │    |      ├── apps.py
|   |    |      ├── models.py
|   |    |      ├── sessionStatus.py
|   |    |      ├── test.py
|   |    |      ├── urls.py
|   |    |      ├── utlis.py
|   |    |      └── views.py
│   │    ├──.env 
│   │    ├── .gitignore
|   |    ├── db
|   |    ├── manage.py
|   |    ├── req.txt
|   |    └── test.html
└── README.md
└── 
```
## Key Highlights
1. **Stripe Integration:** Implemented for secure and seamless payment processing.
2. **Scalability:** Database schema is normalized, ensuring efficient data handling as the application grows.
3. **Error Management:** Custom exceptions like `ResourceNotFoundException` and `ProductNotPresentException` improve user experience.
4. **Optimization Techniques:** Usage of caching and database indexing for better performance.

## Limitations
1. **Cost of Stripe:** Stripe's transaction fees may not be feasible for small-scale applications.
2. **Database Scalability:** For extremely high traffic, techniques like sharding or denormalization may need to be explored.
3. **Stale Data in Caching:** Proper cache invalidation strategies need to be implemented to avoid stale data issues.

## Suggestions for Improvement
1. **Multi-Gateway Payments:** Add support for multiple payment gateways for user flexibility.
2. **Advanced Monitoring:** Integrate APM tools like New Relic to monitor system health.

## Conclusion
This project provided hands-on experience in building multiple microservices for an e-commerce platform using modern software development principles. By focusing on scalability, modularity, and real-world integrations like Stripe, the project offers practical insights into developing robust and maintainable applications. While there are some limitations, the system is well-positioned for enhancements and scaling in future iterations.

## Getting Started

### Prerequisites
-Python 3.8 or higher
-pip (Python package manager)
-Django 5.2.3
-install stripe
-MYSQL Database
-Git
-Code Editor(PyCharm)


### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/mfdeepa/Ecommerce_project
    ```
2. Navigate to the project directory:
    ```sh
    Ecommerce_project
    ```
3. Install the dependencies:
    ```
    cryptography==43.0.3
    Django==5.1.1
    django-cors-headers==4.6.0
    django-mysql==4.14.0
    django-oauth-toolkit==3.0.1
    djangorestframework==3.15.2
    djangorestframework-simplejwt==5.3.1
    h11==0.14.0
    httpcore==1.0.6
    httpx==0.27.2
    idna==3.10
    injector==0.22.0
    jwcrypto==1.5.6
    mysqlclient==2.2.4
    oauthlib==3.2.2
    pycparser==2.22
    PyJWT==2.9.0
    python-dotenv==1.1.1
    requests==2.32.3
    sniffio==1.3.1
    sqlparse==0.5.1
    typing_extensions==4.12.2
    tzdata==2024.1
    urllib3==2.2.3

    ```

### Configuration
1. Update the `application.properties` file with your database and Stripe API configurations:
    ```properties
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "service name",
        "USER": 'root',
        "PASSWORD": 'Deepa@123',
        "HOST": '127.0.0.1',
        "PORT": '3306',
    }
    STRIPE_SECRET_KEY=your_stripe_secret_key
    'USER_SERVICE': 'http://localhost:8001',
    'PRODUCT_SERVICE': 'http://localhost:8002',
    'CART_SERVICE': 'http://localhost:8003',
    'ORDER_SERVICE': 'http://localhost:8004',
    'PAYMENT_SERVICE': 'http://localhost:8010',
    'IntegrationService':'http://localhost:8006',
    ```

### Running the Application
1. Start the application:
    ```
    default_auto_field = "django.db.models.BigAutoField"
    name = "service name"
    mvn spring-boot:run
    ```
2. Access the application at different port for different service 
    'USER_SERVICE': 'http://localhost:8001',
    'PRODUCT_SERVICE': 'http://localhost:8002',
    'CART_SERVICE': 'http://localhost:8003',
    'ORDER_SERVICE': 'http://localhost:8004',
    'PAYMENT_SERVICE': 'http://localhost:8010',
    'IntegrationService':'http://localhost:8006' .

## API Endpoints
### Product service 
- `POST /products` - Create a new product
- `GET /products` - get products
- `Get /products/{productId}` - get product via product id
- `POST /category` - Create a new category
- `GET /category` - get category via category id

### User service
- `GET /users/` - Get all users
- `POST /users/ ` - Create a new user
- `GET /users/{pk}` - Get user details by ID
- `PUT /users/{pk}` - Update user details
- `DELETE /users/{pk}` - Delete a user
- `GET /users/{user_id}/roles` - Get roles assigned to a user
- `POST /users/{user_id}/roles` - Assign or update roles for a user 

### Cart service
- `GET /api/cart/` - Retrieve the current cart for the authenticated user
- `POST /api/cart/add/` - Add an item to the cart
- `POST /api/cart/update/{pk}/` - Update the quantity of a cart item (pk = cart item ID)
- `DELETE /api/cart/remove/{pk}/` - Remove a specific item from the cart (pk = cart item ID)
- `POST /api/cart/clear/` - Clear all items from the cart

### order service
- `POST /orders/` - Create a new order
- `GET /orders/history/` - Retrieve the authenticated user's past order history
- `GET /orders/{pk}/` - Get details of a specific order (pk = order ID)
- `GET /orders/{pk}/track/` - Track the status and progress of a specific order
- `POST /orders/{pk}/confirm/` - Confirm a specific order 

### paymentSerEcpmmerce service
- `POST /service/` - Initiate a new payment using the selected payment gateway (e.g., Stripe or Razorpay)
- `POST /webhook/stripe/` - Receive and handle Stripe webhook events 


### Integration service
- `POST /cart/add/` - Add an item to the user's cart
- `POST /orders/place/` -  Place an order using the items in the user's cart
- `POST /payment/initiate/` - Initiate a payment for the placed order

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.