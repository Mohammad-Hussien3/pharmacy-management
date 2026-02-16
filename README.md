# Pharmacy Management System

A backend system built with Django, Django REST Framework, and Django Channels. This application manages pharmacy inventory (products), handles user authentication via JWT, and includes a real-time chat feature for communication between users.

## 🚀 Features

### 🔐 User Authentication (`register` app)
* **JWT Authentication:** Secure login and token management using `rest_framework_simplejwt`.
* **User Management:** Registration of new users and retrieval of user lists.
* **Session Control:** Functionality to log out (delete account) and refresh access tokens.

### 📦 Product Management (`product` app)
* **Inventory Tracking:** Admin users can add new products with details like price, quantity, and description.
* **Stock Updates:** Admins can update product quantities and prices.
* **Catalog View:** Authenticated users can view the full list of available products.

### 💬 Real-Time Chat (`chatapp` app)
* **WebSocket Support:** Powered by **Django Channels** for real-time communication.
* **Chat Rooms:** Dynamic creation of chat rooms between two users.
* **Message History:** Automatically saves and retrieves past messages when a user joins a chat.

## 🛠️ Tech Stack
* **Backend Framework:** Django 5.0
* **API Toolkit:** Django REST Framework (DRF)
* **Real-time:** Django Channels (ASGI)
* **Authentication:** Simple JWT
* **Database:** SQLite (default)
* **CORS:** `django-cors-headers` enabled

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd pharmacy-management
    ```

2.  **Install Dependencies**
    ```bash
    pip install django djangorestframework djangorestframework-simplejwt channels django-cors-headers
    ```

3.  **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

4.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

## 🔗 API Endpoints

### Authentication (`/`)
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/register/` | Public | Register a new user |
| `PUT` | `/login/` | Public | Log in and receive JWT tokens |
| `POST` | `/token/refresh/` | Public | Refresh access token |
| `GET` | `/allusers/` | Authenticated | List all registered users |
| `DELETE` | `/logout/<id>/` | Authenticated | Delete user account/Logout |

### Products (`/`)
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/allproducts/` | Authenticated | Retrieve all products |
| `POST` | `/addproduct/` | Admin | Add a new product to inventory |
| `POST` | `/editprice/<id>/` | Admin | Update the price of a product |
| `POST` | `/editquantity/<id>/<number>/` | Admin | Update product quantity |

### 🔌 WebSocket Chat
**URL Pattern:** `ws/chat/<room_name>/<senderId>/<receiverId>/`

* **Protocol:** `ws://` (or `wss://` in production)
* **Functionality:** Connects two users based on their IDs and a room name. Messages sent are broadcast instantly to the other participant and saved to the database.
