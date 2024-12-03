# **User Stories**

**Spending Strategizer**

---

# **USER**

## **Sign Up**

As an unregistered and unauthorized user, I want to be able to sign up for the app via a sign-up form. When I'm on the `/signup` page:

* I would like to enter my email, username, and password on a clearly laid-out form.
* I would like the app to log me in upon successful completion of the sign-up form, so I can seamlessly access the app’s functionality.
* When I enter invalid data on the sign-up form, I would like the app to inform me of the validations I failed to pass and repopulate the form with my valid entries (except my password). So that I can try again without needing to refill the form for valid data entries.

---

## **Log In**

As a registered and unauthorized user, I want to be able to log in to the app via a log-in form. When I'm on the `/login` page:

* I would like to enter my email and password on a clearly laid-out form.
* I would like the app to log me in upon successful completion of the login form, so I can access the app's functionality.
* When I enter invalid data on the login form, I would like the app to inform me of the validations I failed to pass and repopulate the form with my valid entries (except my password). So that I can try again without needing to refill forms for valid entries.

---

## **Demo User**

As an unregistered and unauthorized user, I want a demo button on both the `/signup` and `/login` pages to explore the app without signing up or logging in. When I'm on either the `/signup` or `/login` pages:

* I can click a "Demo User" button to log me in as a guest user. So that I can test the app's features and functionality without needing to enter credentials.

---

## **Log Out**

As a logged-in user, I want to log out via an easy-to-find "Log Out" button on the navigation bar. While on any page of the app:

* I can log out of my account and be redirected to the landing page. So that I can easily log out and keep my information secure.

---

# **WALLET MANAGEMENT**

## **View Wallet**

As a logged-in user, I want to view all credit cards in my wallet. When I'm on the `/wallet` page:

* I can see all added cards displayed with details such as name, type, and rewards categories. So that I can manage my wallet effectively.

---

## **Add Cards to Wallet**

As a logged-in user, I want to add new credit cards to my wallet. When I'm on the `/wallet/add` page:

* I can select cards from the available card list to add to my wallet. So that I can include the cards I use frequently.

---

## **Edit Wallet**

As a logged-in user, I want to update my wallet. When I'm on the `/wallet/edit` page:

* I can modify the details of my wallet, such as updating or organizing the cards included. So that I can keep my wallet accurate and organized.

---

## **Remove Cards from Wallet**

As a logged-in user, I want to remove credit cards from my wallet. When I'm on the `/wallet` page:

* I can click "Remove" next to a card to delete it from my wallet. So that I can clean up unused cards.

---

# **CATEGORIES IN SPENDING**

## **View Categories**

As a logged-in user, I want to view all categories in my spending profile. When I'm on the `/spending/categories` page:

* I can see all categories displayed, such as dining, grocery, travel, and others. So that I can evaluate my spending needs.

---

## **Add Categories to Spending**

As a logged-in user, I want to add new categories to my spending profile. When I'm on the `/spending/categories/add` page:

* I can select categories from the available category list to add to my spending profile. So that my spending strategy reflects my daily use cases.

---

## **Remove Categories from Spending**

As a logged-in user, I want to remove categories from my spending profile. When I'm on the `/spending/categories` page:

* I can click "Remove" next to a category to delete it from my spending profile. So that I can refine my strategy.

---

# **SUGGESTED SPENDING STRATEGY**

## **View Spending Strategy**

As a logged-in user, I want to see a personalized spending strategy. When I'm on the `/dashboard` page:

* I can view suggestions like "Use Card A for dining to earn 4% cashback" or "Use Card B for gas to earn 3x points." So that I can optimize my credit card rewards.

---

## **Update Spending Strategy**

As a logged-in user, I want my strategy to update dynamically. When I add, edit, or remove cards or categories:

* The app automatically recalculates my strategy and displays updated suggestions. So that I always have the most accurate plan.

---

# **SUGGESTED APPLYING STRATEGY**

## **View Card Applying Strategy**

As a logged-in user, I want to see recommendations for credit cards to apply for. When I'm on the `/dashboard` page:

* I can view suggestions like "Consider applying for Card A to maximize rewards for dining" or "Adding Card B could earn 5x points on travel." So that I can make informed decisions about which cards to apply for next.

---

## **Dynamic Applying Strategy Updates**

As a logged-in user, I want the applying strategy to update dynamically. When I add or remove cards or categories:

* The app recalculates and provides updated card application suggestions. So that I always have accurate and relevant recommendations for expanding my wallet.

---