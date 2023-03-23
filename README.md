# **Analytics Dashboard for H&M Data**

I have built an analytics dashboard on a set of H&M data about customers, articles, and transactions. The dashboard provides valuable insights into the business by generating KPIs and graphs based on the datasets.

The structure of the project is as follows:

- **API**
  - Python file for the api code using Flask
  - YAML file for deploying to GCP
  - Requirements.txt file for the necessary packages
- **Frontend**
  - Python file for the frontend code using Streamlit
  - YAML file for deploying to GCP
  - Requirements.txt file for the necessary packages

&nbsp;

# **🔗 Rest API**

This section outlines the REST API built using Flask.

### **📦 Required Modules**

---

The api requires the following Python modules to be installed:

- _Flask_
- _Gunicorn_
- _Flask-RESTx_
- _Flask_cors_
- _PyMongo_
- _DNSpython_

To install, nagivate to the api directory and run:

```console
$ pip install -r requirements.txt
```

### **🎯 Endpoints**

---

#### **Customers**

#### **GET /api/customers**`

- Description: Gets all customers
- Authorization: Requires a valid access token
- Response: JSON of customers

#### **Articles**

**GET /api/articles**

- Description: Gets all articles
- Authorization: Requires a valid access token
- Response: JSON of articles

#### **Transactions**

**GET /api/transactions**

- Description: Gets all transactions
- Authorization: Requires a valid access token
- Response: JSON of transactions

### **🔒 Authentication**

---

The API is protected by Bearer Authentication. In order to receive the data, you must provide the bearer token. To receive the token, please contact me.

&nbsp;

# **📊 Frontend**

This section outlines the Frontend built using Streamlit. The analytics dashboard provides valuable insights into the business.

### **📦 Required Modules**

---

The frontend requires the following Python modules to be installed:

- _Pandas_
- _Requests_
- _Streamlit_authenticator_
- _Streamlit_
- _Altair_

To install, nagivate to the frontend directory and run:

```console
$ pip install -r requirements.txt
```

### **🔥 Features**

---

The H&M Analytics Dashboard provides the following features:

1. **Authentication:** Secure access to the dashboard through a login system.
2. **Interactive Filters:** Use multiple filters to find exactly what you need.
3. **Visually Appealing Charts and Graphs:** Gain insights through graphs that provide a visual overview of the data.
4. **KPIs:** View important KPIs to understand H&M's customers and performance of their articles and departments.

### **🔒 Authentication**

---

The frontend is protected by a login window. Users must log in in order to view the dashboard. To receive credentials, please contact me.
