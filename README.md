# PointChurner

Point Churner is a user-friendly app designed to help credit card holders optimize their spending strategies. Users can effortlessly build their wallet by adding, editing, and removing credit cards from the database. Once cards are added, users can manage their spending categories by creating new ones, editing existing ones, or removing categories they no longer use. The app then provides a personalized spending strategy on the home page, offering tailored credit card usage suggestions based on the cards in their wallet and their unique spending habits. With a focus on practicality and ease of use, Point Churner aims to become a standout project and a highlight of my portfolio.

# Live Link

https://pointchurner.onrender.com/

## Tech Stack

### Frameworks and Libraries
<div style="display: flex; align-items: center; gap: 10px;">
  <img src="https://img.shields.io/badge/-Python-3776ab?logo=python&logoColor=FFFF66&logoWidth=20" alt="Python" height="25">
  <img src="https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white&logoWidth=20" alt="Flask" height="25">
  <img src="https://img.shields.io/badge/-Javascript-41454A?logo=javascript&logoColor=F7DF1E&logoWidth=20" alt="Javascript" height="25">
  <img src="https://img.shields.io/badge/-React-263238?logo=react&logoColor=61DAFB&logoWidth=20" alt="React" height="25">
  <img src="https://img.shields.io/badge/-Redux-764ABC?logo=redux&logoColor=white&logoWidth=20" alt="Redux" height="25">
  <img src="https://img.shields.io/badge/-CSS3-1572B6?logo=css3&logoColor=white&logoWidth=20" alt="CSS3" height="25">
  <img src="https://img.shields.io/badge/-HTML5-E34F26?logo=HTML5&logoColor=white&logoWidth=20" alt="HTML5" height="25">
</div>

### Database:

<img src="https://img.shields.io/badge/-PostgreSQL-4169E1?logo=postgresql&logoColor=white&logoWidth=20" alt="PostgreSQL" height="25">

### Hosting:

<img src="https://img.shields.io/badge/-Render-23c43e?logo=render&logoColor=white&logoWidth=20" alt="Render" height="25">

### Connect With Me:

[<img align="left" alt="TiffanyTseng | LinkedIn" width="22px" src="https://github.com/itingtseng/pointchurner/blob/main/assets/linkedin-logo.png" style="margin: 5px;" />][tiffany-linkedin]

[tiffany-linkedin]: https://www.linkedin.com/in/ittseng/

[<img align="left" alt="TiffanyTseng | Gmail" width="22px" src="https://github.com/itingtseng/pointchurner/blob/main/assets/email.png" style="margin: 5px;" />][tiffany-email]<br>

[tiffany-email]: mailto:tifny7574@gmail.com

<br></br>

# Index

[Feature List](https://github.com/itingtseng/pointchurner/wiki/Feature-List) | [DB Schema](https://github.com/itingtseng/pointchurner/wiki/DB-Schema) | [User Stories](https://github.com/itingtseng/pointchurner/wiki/User-Stories) | [Wireframes](https://github.com/itingtseng/pointchurner/blob/main/Point_Hacker_wireframe.pdf)

# Landing Page

<img src="https://github.com/Savsou/BopStop/blob/dev/assets/ezgif-5-f6d3c25e08.gif" alt="Demo Animation" width="830">

# Wallet

<img src="https://github.com/Savsou/BopStop/blob/dev/assets/ezgif-5-433f26ddaf.gif" alt="Demo Animation" width="830">

# Spending

<img src="https://github.com/Savsou/BopStop/blob/dev/assets/ezgif-4-d7977fc62c.gif" alt="Demo Animation" width="830">

# **API Routes**

## **Users**

### **User Login**

- **Require authentication**: False  
- **Request**  
  - **Method**: POST  
  - **Route path**: `/api/auth/login`  
  - **Body**:  

    ```json
    {
      "email_or_username": "user@example.com or username",
      "password": "your_password"
    }
    ```

- **Successful Response**  
  - **Status Code**: 200  
  - **Body**:  

    ```json
    {
      "id": 1,
      "username": "username",
      "email": "user@example.com",
      "createdAt": "2024-10-30",
      "updatedAt": "2024-10-30"
    }
    ```

- **Error Response: Invalid credentials**  
  - **Status Code**: 404  
  - **Body**:  

    ```json
    {
      "message": "Invalid login credentials"
    }
    ```

---

### **User Signup**

- **Require authentication**: False  
- **Request**  
  - **Method**: POST  
  - **Route path**: `/api/auth/signup`  
  - **Body**: 

    ```json
    {
      "username": "desired_username",
      "firstname": "FirstName",
      "lastname": "LastName",
      "email": "user@example.com",
      "password": "your_password",
      "confirm_password": "your_password"
    }
    ```

- **Successful Response**  
  - **Status Code**: 201  
  - **Body**:  

    ```json
    {
      "id": 21,
      "username": "desired_username",
      "email": "user@example.com",
      "createdAt": "2024-11-01",
      "updatedAt": "2024-11-01"
    }
    ```

- **Error Response: User already exists**  
  - **Status Code**: 409  
  - **Body**:  

    ```json
    {
      "message": "User with this email or username already exists."
    }
    ```

---

### **User Logout**

- **Require authentication**: True  
- **Request**  
  - **Method**: GET  
  - **Route path**: `/api/auth/logout`  

- **Successful Response**  
  - **Status Code**: 200  
  - **Body**: 

    ```json
    {
      "message": "User logged out successfully."
    }
    ```

---

### **Get Current User**

- **Require authentication**: True  
- **Request**  
  - **Method**: GET  
  - **Route path**: `/api/users/session`  

- **Successful Response**  
  - **Status Code**: 200  
  - **Body**: 

    ```json
    {
      "id": 1,
      "username": "current_username",
      "email": "current_user@example.com",
      "createdAt": "2024-10-30",
      "updatedAt": "2024-10-30"
    }
    ```

- **Error Response**  
  - **Status Code**: 401  
  - **Body**: 

    ```json
    {
      "message": "Unauthorized"
    }
    ```

---

### **Delete User**

- **Require authentication**: True  
- **Request**  
  - **Method**: DELETE  
  - **Route path**: `/api/users/session`  

- **Successful Response**  
  - **Status Code**: 204  
  - **Body**:  

    ```json
    {
      "message": "User deleted successfully."
    }
    ```

- **Error Response: Unauthorized**  
  - **Status Code**: 401  
  - **Body**:  

    ```json
    {
      "message": "Unauthorized"
    }
    ```

---

## **Cards**

### **View All Cards**

- **Method**: GET  
- **Route path**: `/api/cards`  
- **Authentication**: False  

- **Responses**:
  - **200**: 
  - **Body**:

  ```json
  {
    "cards": [
      {
        "id": 1,
        "name": "Blue Business Cash",
        "issuer": "AMERICAN_EXPRESS",
        "image_url": "/images/amex/blue-business-cash.webp",
        "url": "https://www.americanexpress.com/us/credit-cards/card/blue-cash-everyday/"
      }
      // more products...
    ]
  }
  ```

---

### **View Card Details**

- **Method**: GET  
- **Route path**: `/api/cards/:cardId`  
- **Authentication**: False  

- **Parameters**:
  - `card_id` (int): The ID of the card within the wallet.

- **Responses**:
  - **200**: Card details.
  - **Body**:

  ```json
  {
    "cards": [
      {
        "id": 1,
        "name": "Blue Business Cash",
        "issuer": "AMERICAN_EXPRESS",
        "image_url": "/images/amex/blue-business-cash.webp",
        "url": "https://www.americanexpress.com/us/credit-cards/card/blue-cash-everyday/",
        "reward_points": [
          {
          "category_id": "1",
          "bonus_point": "3",
          "multiplier_type": "%",
          },
          // more categories...
        ]
      }
      // more cards...
    ]
  }
  ```

  - **404**: Card not found.

---

## **Wallet**

### **View Wallet**

- **Method**: GET  
- **Route path**: `/api/wallet`  
- **Authentication**: True  

- **Responses**:
  - **200**: User's wallet with all associated cards.
  - **Body**:

  ```json
  {
    "cards": [
      {
        "card_id": 1,
        "wallet_id": 1,
        "name": "Blue Business Cash",
        "issuer": "AMERICAN_EXPRESS",
        "image_url": "/images/amex/blue-business-cash.webp",
        "url": "https://www.americanexpress.com/us/credit-cards/card/blue-cash-everyday/",
        "nickname": "BBC",
        "network": "AMERICAN_EXPRESS",
        "reward_points": [
          {
          "category_id": 1,
          "bonus_point": 1,
          "multiplier_type": "%",
          },
          // more categories...
        ]
      }
      // more cards...
    ]
  }
  ```
  
  - **401**: Unauthorized
  - **404**: User not found

---

### **Get Card Details in Wallet**

- **Method**: GET  
- **Route path**: `/api/wallet/<wallet_id>/cards/<card_id>`  
- **Authentication**: True  

- **Parameters**:
  - `wallet_id` (int): The ID of the wallet.
  - `card_id` (int): The ID of the card within the wallet.

- **Responses**:
  - **200**: Card details in the specified wallet.
    - **Body**:
      ```json
      {
        "card_id": 1,
        "wallet_id": 1,
        "name": "Blue Business Cash",
        "issuer": "AMERICAN_EXPRESS",
        "image_url": "/images/amex/blue-business-cash.webp",
        "url": "https://www.americanexpress.com/us/credit-cards/card/blue-cash-everyday/",
        "nickname": "BBC",
        "network": "AMERICAN_EXPRESS",
        "reward_points": [
          {
            "category_id": 1,
            "bonus_point": 1,
            "multiplier_type": "%"
          }
          // more categories...
        ]
      }
      ```
  - **401**: Unauthorized access.
  - **403**: Unauthorized access to the wallet.
  - **404**: Wallet or card not found.

---

### **Add Card to Wallet**

- **Method**: POST  
- **Route path**: `/api/wallet/cards`  
- **Authentication**: True  
- **Body**:  

  ```json
  {
    "card_id": 1,
    "wallet_id": 1,
    "nickname": "BBC",
    "network": "AMERICAN_EXPRESS",
  }
  ```

- **Responses**:
  - **201**: Card successfully added to the wallet.
  - **Body**:  

  ```json
  {
    "cards":
      {
        "card_id": 1,
        "wallet_id": 1,
        "name": "Blue Business Cash",
        "issuer": "AMERICAN_EXPRESS",
        "image_url": "/images/amex/blue-business-cash.webp",
        "url": "https://www.americanexpress.com/us/credit-cards/card/blue-cash-everyday/",
        "nickname": "BBC",
        "network": "AMERICAN_EXPRESS",
        "reward_points": [
          {
          "category_id": 1,
          "bonus_point": 1,
          "multiplier_type": "%",
          },
          // more categories...
        ]
      }
  }
  ```

  - **404**: Card not found.
  - **409**: Card already exists in wallet.

---

### **Edit Card in Wallet**

- **Method**: PUT  
- **Route path**: `/api/wallet/cards/:cardId`  
- **Authentication**: True  
- **Body**: 

  ```json
  {
    "nickname": "Updated Card Name",
    "network": "Updated Network Name"
  }
  ```

- **Responses**:
  - **200**: Card successfully updated.
  - **404**: Card not found in wallet.

---

### **Delete Card from Wallet**

- **Method**: DELETE  
- **Route path**: `/api/wallet/cards/:cardId`  
- **Authentication**: True  

- **Responses**:
  - **200**: Card successfully removed.
  - **404**: Card not found in wallet.

---

## **Categories**

### **View All Categories**

- **Method**: GET  
- **Route path**: `/api/categories`  
- **Authentication**: True  

- **Responses**:
  - **200**: List of all categories.
  - **Body**:

  ```json
    {
      "categories": [
        {
          "id": 1,
          "name": "dining",
          "parent_categories_id": 1,
        }
        // more categories...
      ]
    }
    ```

---

### **View Category Details**

- **Method**: GET  
- **Route path**: `/api/categories/:categoryId`  
- **Authentication**: False

- **Parameters**:
  - `ccategoryId` (int): The ID of the category.

- **Responses**:
  - **200**: Category details.
  - **Body**:

  ```json
        {
          "id": 1,
          "name": "dining",
          "parent_categories_id": 1,
        }
    ```

    - **404**: Category not found.

---

## **Spending**

### **View Spending**

- **Method**: GET  
- **Route path**: `/api/spending`  
- **Authentication**: True  

- **Responses**:
  - **200**: Spending details and associated categories.
  - **Body**:
  
  ```json
    {
      "categories": [
        {
          "category_id": 1,
          "spending_id": 1,
          "name": "dining",
          "parent_categories_id": 1,
        }
        // more categories...
      ]
    }
    ```

  - **404**: Spending profile not found.

---

### **Get Category Details in Spending**

- **Method**: GET  
- **Route path**: `/api/spendings/<spending_id>/categories/<category_id>`  
- **Authentication**: True  

- **Parameters**:
  - `spending_id` (int): The ID of the spending.
  - `category_id` (int): The ID of the category within the spending.

- **Responses**:
  - **200**: Category details in the specified spending.
    - **Body**:
      ```json
      {
        "category_id": 2,
        "spending_id": 1,
        "name": "Dining",
        "parent_categories_id": null
      }
      ```
  - **401**: Unauthorized access.
  - **403**: Unauthorized access to the spending.
  - **404**: Spending or category not found.

---

### **Add Category to Spending**

- **Method**: POST  
- **Route path**: `/api/spending/categories`  
- **Authentication**: True  
- **Body**:  
  ```json
  {
    "category_id": 1,
  }
  ```

- **Responses**:
  - **201**: Category added to spending profile.

  ```json
    {
      "categories": 
        {
          "category_id": 1,
          "spending_id": 1,
          "name": "dining",
          "parent_categories_id": 1,
        }
    }
    ```
  - **404**: Category not found.
  - **409**: Category already exists in spending profile.

---

### **Delete Category from Spending**

- **Method**: DELETE  
- **Route path**: `/api/spending/categories/:categoryId`  
- **Authentication**: True  

- **Responses**:
  - **200**: Category removed from spending profile.
  - **404**: Category not found in spending profile.

--- 

## Getting started

1. Install dependencies.

   ```bash
   pipenv install -r requirements.txt
   ```

2. Create a __.env__ file based on the example with proper settings for your
   development environment.

3. Make sure the SQLite3 database connection URL is in the __.env__ file.

4. This starter organizes all tables inside the `flask_schema` schema, defined
   by the `SCHEMA` environment variable.  Replace the value for
   `SCHEMA` with a unique name, **making sure you use the snake_case
   convention.**

5. Get into your pipenv, migrate your database, seed your database, and run your
   Flask app:

   ```bash
   pipenv shell
   ```

   ```bash
   flask db upgrade
   ```

   ```bash
   flask seed all
   ```

   ```bash
   flask run
   ```

6. To run the React frontend in development, `cd` into the __react-vite__
   directory and run `npm i` to install dependencies. Next, run `npm run build`
   to create the `dist` folder. The starter has modified the `npm run build`
   command to include the `--watch` flag. This flag will rebuild the __dist__
   folder whenever you change your code, keeping the production version up to
   date.
