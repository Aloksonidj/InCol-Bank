# InCol-Bank

### CS50W Capstone Project

**Author:** Alok Soni

GitHub Repository: https://github.com/Aloksonidj/InCol-Bank
---
## What Makes This Project Different from Previous CS50 Web Projects?

While previous projects in the course laid the groundwork for web development, InCol BANK.in intentionally shifts away from those paradigms to explore different architectural challenges:

* **From Social to Financial Integrity**: Unlike Project 4 (Network), which managed public, loosely-coupled social data (likes, follows, posts), this project manages strictly private, highly-coupled financial data. In a social network, a missing "like" is a minor bug; in this banking app, a single failed ledger entry results in a critical loss of financial integrity. This necessitated a much more rigorous backend validation logic.

* **Persistent Transaction Snapshots**: In Project 2 (Commerce), data was mostly updated in place (changing a bid). InCol BANK implements a snapshot-based ledger system. Every transaction doesn't just change a balance; it generates an immutable statement record that captures the "After Balance." This allows for historical auditing, which is a significant jump in data modeling complexity.

* **Security-First Session Handling**: While previous projects used basic authentication, this project implements secondary authorization layers. The "Check Balance" and "Money Transfer" features require specific session-state verification (InCol PIN) and temporary session flags (show_balance) that are cleared dynamically via AJAX. This mimics real-world banking security flows rather than simple CRUD operations.

* **Identity Abstraction**: Most course projects used standard incremental IDs as usernames or primary identifiers. This project implements an Identity Protocol that abstracts the database ID into a 7-digit Account Number ($1201100 + id$), forcing the code to handle translation between user-facing identifiers and internal database keys throughout the entire application.

## Distinctiveness and Complexity

### **Distinctiveness**

**InCol BANK.in** is a comprehensive personal banking and financial ledger application. It is designed to solve the problem of private wealth tracking and secure internal funds movement. Unlike previous course projects, it functions as a **Personal Finance Manager (PFM)** where data privacy and transactional integrity are the core objectives.

While it is necessary to differentiate it from previous course work, the project stands on its own as a unique implementation of a banking system:

**Purpose-Built Financial Ledger:** The application is a specialized tool for managing a digital wallet. Its primary goal is the accurate recording of debits and credits within a centralized database, ensuring that every financial event has a corresponding audit trail.

**Unique Identity Protocol:** Upon registration, the system does not simply assign a standard primary key. It implements a custom account generation algorithm ($1201100 + id$) that transforms a standard database record into a professional 7-digit banking identifier. This identifier becomes the unique "handle" for all user interactions, replacing standard usernames for transactions.

**Privacy-First Architecture:** Unlike social applications where data is public, InCol BANK uses restricted access patterns. The "Locked Balance" feature is a deliberate design choice to prevent "shoulder-surfing" (unauthorized viewing in public spaces), mimicking real-world fintech applications like UPI or mobile banking apps.

**Financial Integrity:** The "Transfer" logic is a double-entry transaction. For every internal transfer, the system must simultaneously update the balances of two separate users and generate two distinct statement records to maintain balance consistency—a logic flow not present in social or e-commerce projects.

### **Complexity**

The complexity of this project is demonstrated through its multi-layered security and asynchronous data handling:

* **Asynchronous Interaction (Fetch API):** The "Recent Activity" component on the dashboard is populated using JavaScript `fetch` calls to a JSON endpoint. This allows the user to see their latest five transactions without a page refresh.
* **Session-Based State Management:** I implemented a "PIN-to-Reveal" balance system. This uses Django Sessions to store a temporary "visibility flag". To enhance security, I built a manual "Mask" feature where a JavaScript `fetch` request triggers the server-side deletion of the session flag, followed by a DOM update to hide the balance again.
* **Transaction Logic:** The transfer view handles multiple validation layers, including checks for beneficiary existence, insufficient balance, and PIN verification before committing changes to the database.
* **Responsive Financial Ledger:** The bank statement uses a sophisticated CSS grid with color-coded cash flow indicators (red for debits, green for credits) and is fully mobile-responsive through Bootstrap 5's responsive table classes.

---

## File Documentation

**Root Directory**

* `manage.py`: The standard Django entry point for administrative tasks.

* `db.sqlite3`: The SQLite database containing the schema for users, accounts, and financial statements.

* `requirements.txt`: Lists all necessary Python dependencies, primarily Django 4.2+.

**Main Project Application (`InColBank/`)**

* `urls.py`: The central routing table. It manages top-level paths like Home, New_Account, verify-user, and change-password, while using include() to route banking-specific requests to the login sub-application.

* `views.py`:

    * `Home`: Renders the entry landing page (Bank.html).

    * `newAccount`: Orchestrates new user registration. It validates password matches, handles IntegrityError for unique usernames, generates the unique 7-digit account number, initializes the Account model, and creates an initial ₹2000 credit entry in the statement model.

    * `check_user`: A gateway for sensitive actions like password resets. It verifies identity using account numbers and mobile numbers for guests, or the current password for authenticated users, setting an is_verified flag in the session.

    * `change_password`: Validates the session-based verification flag before allowing a user to hash and save a new password using Django's set_password() method.

* `templates/`:

    * `Bank.html`: The home page template utilizing a high-end "Glassmorphism" UI with clear call-to-action buttons for registration and login.

    * `Nav.html`: The core layout file. It manages the responsive navigation bar, authentication-dependent menu items, and the global Django Messages display logic.

    * `open_Acc.html`: A custom-styled registration form with a frosted glass effect.

    * `check_user.html`: A multi-purpose verification form used for both authenticated password checks and unauthenticated account recovery.

    * `forget_password.html`: The secure interface for entering and confirming a new user password.

* `static/`:

    * `bank.css`: Styles the primary landing page, managing the container flexbox layouts and custom button aesthetics.

    * `Nav.css`: The primary design system file. It implements the "Glassmorphism" effect using backdrop-filter: blur, manages the fixed background image, and defines the interactive hover states for dashboard elements.

    * `open_acc.css`: Defines the unique input styling and button animations for the registration and verification forms.

**Banking Logic Application (`login/`)**

* `models.py`:

    * `User`: Extends AbstractUser to create a custom user model for the application.

    * `Account`: Links to the User model. It stores critical banking data including the current balance (as a BigIntegerField), account status, Mobile_no, and the user's pin for transaction authorization.

    * `statement`: A ledger model that records every transaction. It stores the acc_no (ForeignKey to Account), the After_balance snapshot, the cash_flow (positive for credits, negative for debits), and a detail string describing the transaction.

* `urls.py`: Defines the application-specific routes for authentication (login, logout), dashboard access (account), financial operations (transfer, pin), and balance privacy management (check-balance, hide-balance).

* `views.py`: The core "engine" of the banking application:

    * `Login`: Authenticates users using their 7-digit account number and password.

    * `account_detail`: Renders the primary dashboard with the user's personal information and account status.

    * `moneyTransfer`: Manages the initiation of funds movement. It validates the beneficiary account number (handling the subtraction logic for the custom ID system), checks for sufficient funds, and prepares the transfer data in the session.

    * `confirm_pay`: A high-security view that handles both the setting of a new PIN and the verification of an existing PIN. It executes the final database transaction—updating balances for both sender and receiver and generating dual ledger entries.

    * `view_statement`: A hybrid view that either renders the full historical statement page or returns the five most recent transactions as JSON for the dashboard's asynchronous "Recent Activity" feed.

    * `hide_balance & checkBalance`: Manage the session state for masking or revealing the user's total balance on the dashboard.

* `templates/login/`:

    * `Login.html`: A focused login interface with links to account recovery and registration.

    * `account.html`: The central dashboard. It includes a custom JavaScript section that uses the Fetch API to populate the activity list and manages the "Check Balance" toggle logic.

    * `transfer.html`: An interactive form for initiating transfers, showing the user's current balance and providing validation feedback.

    * `pin.html`: A secure PIN entry interface that adapts its UI based on whether the user is setting a PIN for the first time or verifying a transaction.

    * `Statement.html`: A detailed ledger view utilizing a responsive table to display the full transaction history, with conditional CSS styling for cash flow values.

* `static/login/:`

    * `account.css`: Styles the dashboard cards and transaction list items, implementing a scalable hover effect for a modern feel.

    * `Login.css`: Manages the aesthetics for the login and PIN entry forms, including specialized button styling and alert layouts.

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