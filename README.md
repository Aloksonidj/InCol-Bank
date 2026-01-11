# InCol-Bank

### CS50W Capstone Project

**Author:** Alok Soni
---

## Distinctiveness and Complexity

### **Distinctiveness**

**InCol BANK.in** is a specialized financial ledger application that is entirely distinct from the projects previously completed in CS50W.

* **Vs. Project 4 (Network):** While "Network" was a social platform focused on global public feeds and follower relationships, InCol BANK is a private, secure content management system for financial data. There are no social interactions; instead, users interact with a persistent database to track their personal wealth.
* **Vs. Project 2 (Commerce):** Unlike "Commerce," which managed time-based auctions and bidding, this application manages a real-time banking ledger. It features a unique internal transfer protocol based on a custom-generated 7-digit Account Number (1201100 + Record ID), which serves as the unique identifier for all transactions.
* **Core Purpose:** The application serves as a Personal Finance Manager (PFM). It focuses on financial integrity—ensuring that for every transfer, two statement records are created (debit and credit) to maintain an accurate audit trail.

### **Complexity**

The complexity of this project is demonstrated through its multi-layered security and asynchronous data handling:

* **Asynchronous Interaction (Fetch API):** The "Recent Activity" component on the dashboard is populated using JavaScript `fetch` calls to a JSON endpoint. This allows the user to see their latest five transactions without a page refresh.
* **Session-Based State Management:** I implemented a "PIN-to-Reveal" balance system. This uses Django Sessions to store a temporary "visibility flag". To enhance security, I built a manual "Mask" feature where a JavaScript `fetch` request triggers the server-side deletion of the session flag, followed by a DOM update to hide the balance again.
* **Transaction Logic:** The transfer view handles multiple validation layers, including checks for beneficiary existence, insufficient balance, and PIN verification before committing changes to the database.
* **Responsive Financial Ledger:** The bank statement uses a sophisticated CSS grid with color-coded cash flow indicators (red for debits, green for credits) and is fully mobile-responsive through Bootstrap 5's responsive table classes.

---

## File Documentation

### **Main Project (`InColBank/`)**

* **`views.py`**: Contains the primary high-level logic for the banking system:

* `Home`: Renders the main entry point of the bank, offering options to open a new account or login into an existing one.

* `newAccount`: A complex view that manages user registration. It validates password matches, handles ``IntegrityError`` for unique usernames, and automatically generates a unique 7-digit account number by adding a base value ($1201100$) to the auto-incrementing database ID. It initializes the ``Account`` and ``statement`` models with a ₹2000 starting deposit and automatically logs the user in upon success.

* `check_user`: A multi-path verification view used for security flows like password resets. It allows authenticated users to verify their identity via a password check, or unauthenticated users to verify via account number and mobile number. Upon successful verification, it sets a is_verified flag in the session to authorize sensitive changes.

* `change_password`: Securely updates a user's password. It validates the session-based verification flag from ``check_user``, uses Django's ``set_password()`` for secure hashing, cleans up the temporary session data upon success, and handles conditional redirection based on whether the user is currently authenticated.
  
* **`urls.py`**: The primary routing configuration. It maps the project's root URL to the banking landing page and uses `include()` to delegate sub-routes to the login application. Routes traffic between the main bank landing page and the `login` sub-application.


`templates/Bank.html`: The entry point of the application. It uses a "Glassmorphism" UI design, providing clear navigation to either open a new account or log into an existing one.

`templates/open_Acc.html`: A specialized registration form that captures user details, including mobile numbers. It integrates hidden data fields (#special and #Some) to communicate backend status (like generated account numbers or error messages) to the frontend JavaScript.

`templates/Nav.html`: The global layout file. It implements a responsive Bootstrap navbar, loads FontAwesome icons, and contains the logic to display Django's "Messages Framework" alerts (Success/Error) across all pages.

### **Banking App Logic (`login/`)**

 * `models.py`: The heart of the database architecture.

 * `User`: Inherits from AbstractUser to utilize Django's auth system.

 * `Account`: Linked to User via ForeignKey. Stores balance (BigInteger), status (Boolean), Mobile_no, and pin (Integer, max_length=6).

 * `statement`: Linked to Account. Logs every transaction with After_balance, cash_flow, and detail, serving as an immutable ledger.

 * `views.py`: Manages the high-complexity banking operations:

 * `Login`: Authenticates users using their Account Number (username) and password.

 * `moneyTransfer`: Validates beneficiary existence and sufficient funds. Uses request.session to temporarily store transfer details before PIN confirmation.

 * `confirm_pin`: Acts as a security middleware. It verifies the user's PIN against the database before executing any transfer or revealing sensitive data.

 * `view_statement`: A hybrid view that returns a full HTML page or a JSON response of the last 5 transactions depending on request parameters, supporting the asynchronous dashboard.

 * `hide_balance`: An API endpoint that clears specific session keys to "lock" the balance card.

`urls.py`: Defines the routes for the private banking dashboard, the transaction statement page, and the asynchronous session-clearing endpoints.


`templates/login/account.html`: The user's main dashboard. It uses a custom-styled card layout to show account numbers and balances. It includes the JavaScript fetch logic to retrieve "Recent Activity" without a page reload and dynamically appends transaction rows to the DOM.
## How to Run the Application

1. **Clone the Repo:** `git clone https://github.com/Aloksonidj/InCol-Bank.git`

2. **Install Requirements**: Ensure Python then Django are installed.

* **Run:** **`pip install django`**

3. **Apply Migrations:**

**`python manage.py makemigrations`**
**`python manage.py migrate`**

**Start the Server:**

4. **Run:** `python manage.py runserver`
5. **Access:** Open `http://127.0.0.1:8000/` in your browser.

---
## Additional Information

**Security**: Every transaction requires a 6-digit InCol PIN verification step to proceed, mimicking real-world banking security.

**Initial Balance**: New accounts are auto-credited with ₹2000 to allow for immediate testing of the statement and transfer features.

**Responsive Design**: The application was tested across various screen sizes (Mobile, Tablet, Desktop) to ensure the glassmorphism UI remains functional and aesthetically pleasing.