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
          "category_id": "dining",
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
          "category_id": "dining",
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
  
  - **401**: Unauthorized
  - **404**: User not found

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
          "category_id": "dining",
          "bonus_point": "3",
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
          "priority": 1,
          "name": "dining",
          "parent_categories_id": 1,
        }
        // more categories...
      ]
    }
    ```

  - **404**: Spending profile not found.

---

### **Add Category to Spending**

- **Method**: POST  
- **Route path**: `/api/spending/categories`  
- **Authentication**: True  
- **Body**:  
  ```json
  {
    "category_id": 1,
    "priority": 1,
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
          "priority": 1,
          "name": "dining",
          "parent_categories_id": 1,
        }
    }
    ```
  - **404**: Category not found.
  - **409**: Category already exists in spending profile.

---

### **Edit Category in Spending**

- **Method**: PUT  
- **Route path**: `/api/spending/categories/:categoryId`  
- **Authentication**: True  
- **Body**:  
  ```json
  {
    "category_id": 1,
    "priority": 1,
  }
  ```

- **Responses**:
  - **200**: Category updated in spending profile.
  - **404**: Category not found in spending profile.

---

### **Delete Category from Spending**

- **Method**: DELETE  
- **Route path**: `/api/spending/categories/:categoryId`  
- **Authentication**: True  

- **Responses**:
  - **200**: Category removed from spending profile.
  - **404**: Category not found in spending profile.

--- 