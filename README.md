## SplitWise

Steps to run the code:
1. Install Docker In Your System
2. Run Command `docker-compose up`
3. Open your browser and go to [localhost:8000/](http://localhost:8000/)
4. URLs: 
   - To Register, use this URL: [http://localhost:8000/register/](http://localhost:8000/register/)
   - To Login, use the URL: [http://localhost:8000/login/](http://localhost:8000/login/)
   - To Add Expense, use the URL: [http://localhost:8000/members/add-expense/](http://localhost:8000/members/add-expense/)
   - To Show Balances, use the URL: [http://localhost:8000/members/show-balances/](http://localhost:8000/members/show-balances/)
   - To Simplify Expenses, use the URL: [http://localhost:8000/members/simplify-expenses/](http://localhost:8000/members/simplify-expenses/)
   - To Show Passbook, use the URL: [http://localhost:8000/members/show-passbook/](http://localhost:8000/members/show-passbook/)

---

## API Endpoints

### Register
- **URL:** [http://localhost:8000/register/](http://localhost:8000/register/)
- **Method:** POST
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "password": "your_password"
  }
  ```
- **Description:** Register a new user.

### Login
- **URL:** [http://localhost:8000/login/](http://localhost:8000/login/)
- **Method:** POST
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "password": "your_password"
  }
  ```
- **Description:** Authenticate and login an existing user.

### Request Password Reset
- **URL:** [http://localhost:8000/password/reset/](http://localhost:8000/password/reset/)
- **Method:** GET
- **Query Parameters:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Description:** Request a password reset OTP via email.

### Reset Password
- **URL:** [http://localhost:8000/password/reset/](http://localhost:8000/password/reset/)
- **Method:** PUT
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "otp": "123456",
    "new_password": "your_new_password"
  }
  ```
- **Description:** Reset user password using OTP received via email.

### Add Expense
- **URL:** [http://localhost:8000/members/add-expense/](http://localhost:8000/members/add-expense/)
- **Method:** POST
- **Authentication:** Token-based authentication required
- **Payload:**
  ```json
  {
    "name": "Groceries",
    "amount": 50.00,
    "type": "groceries",
    "participants": [1, 2],
    "splits": [25.00, 25.00]
  }
  ```
- **Description:** Add an expense with specified details and participants.

### Show Balances
- **URL:** [http://localhost:8000/members/show-balances/](http://localhost:8000/members/show-balances/)
- **Method:** GET
- **Authentication:** Token-based authentication required
- **Description:** Retrieve balances of the authenticated user.

### Simplify Expenses
- **URL:** [http://localhost:8000/members/simplify-expenses/](http://localhost:8000/members/simplify-expenses/)
- **Method:** PUT
- **Authentication:** Token-based authentication required
- **Description:** Simplify expenses by adjusting splits among participants.

### Show Passbook
- **URL:** [http://localhost:8000/members/show-passbook/](http://localhost:8000/members/show-passbook/)
- **Method:** GET
- **Authentication:** Token-based authentication required
- **Description:** Retrieve the passbook detailing transactions.
