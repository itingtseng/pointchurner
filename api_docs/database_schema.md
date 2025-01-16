# **Database Schema**

## `users`

| column name     | data type | details               |
| --------------- | --------- | --------------------- |
| id              | integer   | not null, primary key |
| username        | string    | not null, unique      |
| firstname       | string    | not null              |
| lastname        | string    | not null              |
| email           | string    | not null, unique      |
| hashedPassword  | string    | not null              |
| createdAt       | datetime  | not null              |
| updatedAt       | datetime  | not null              |

---

## `cards`

| column name       | data type | details               |
| ----------------- | --------- | --------------------- |
| id                | integer   | not null, primary key |
| name              | string    | not null              |
| issuer            | string    |                       |
| image_url         | string    |                       |
| description       | string    |                       |
| annual_fee        | decimal   |                       |
| sign_up_bonus     | string    |                       |
| active            | boolean   |                       |
| created_at        | datetime  | not null              |
| updated_at        | datetime  | not null              |

---

## `categories`

| column name         | data type | details               |
| ------------------- | --------- | --------------------- |
| id                  | integer   | not null, primary key |
| name                | string    | not null, unique      |
| parent_category_id  | integer   | foreign key (nullable)|
| created_at          | datetime  | not null              |
| updated_at          | datetime  | not null              |

- `parent_category_id` references `categories` table (self-referencing)

---

## `reward_points`

| column name      | data type | details               |
| ---------------- | --------- | --------------------- |
| id               | integer   | not null, primary key |
| card_id          | integer   | not null, foreign key |
| category_id      | integer   | not null, foreign key |
| bonus_point      | decimal   |                       |
| multiplier_type  | string    |                       |
| created_at       | datetime  | not null              |
| updated_at       | datetime  | not null              |

- `card_id` references `cards` table  
- `category_id` references `categories` table

---

## `wallets`

| column name | data type | details               |
| ----------- | --------- | --------------------- |
| id          | integer   | not null, primary key |
| user_id     | integer   | not null, foreign key |
| created_at  | datetime  | not null              |
| updated_at  | datetime  | not null              |

- `user_id` references `users` table

---

## `wallets_cards` JOIN TABLE

| column name          | data type | details               |
| -------------------- | --------- | --------------------- |
| wallet_id            | integer   | not null, foreign key |
| card_id              | integer   | not null, foreign key |
| nickname             | string    |                       |
| network              | string    |                       |
| counts_towards_524   | boolean   |                       |
| created_at           | datetime  | not null              |
| updated_at           | datetime  | not null              |

- `wallet_id` references `wallets` table  
- `card_id` references `cards` table

---

## `spendings`

| column name | data type | details               |
| ----------- | --------- | --------------------- |
| id          | integer   | not null, primary key |
| user_id     | integer   | not null, foreign key |
| created_at  | datetime  | not null              |
| updated_at  | datetime  | not null              |

- `user_id` references `users` table

---

## `spendings_categories` JOIN TABLE

| column name      | data type | details               |
| ---------------- | --------- | --------------------- |
| spending_id      | integer   | not null, foreign key |
| category_id      | integer   | not null, foreign key |
| notes            | string    |                       |
| created_at       | datetime  | not null              |
| updated_at       | datetime  | not null              |

- `spending_id` references `spendings` table  
- `category_id` references `categories` table

--- 