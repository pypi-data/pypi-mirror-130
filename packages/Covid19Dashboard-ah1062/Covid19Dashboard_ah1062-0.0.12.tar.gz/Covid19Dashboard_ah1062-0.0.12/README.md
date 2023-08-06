# Covid19Dashboard

---
### DESCRIPTION
---

Covid19Dashboard is a python project that provides a personalised dashboard to present current statistics and news articles for a user.

---
### **PREREQUISITES**
---

Python Version >= 3.9

Installed Packages:

```
uk-covid19
flask
pytest
```

Use the Package Manager [pip](https://pip.pypa.io/en/stable) to install these modules.

```bash
pip install uk-covid19
pip install flask
pip install pytest
```

If modules are currently installed, pip will return a message in response to this, however modules can also be verified by executing line.

```bash
pip list
```

**OR**

```bash
pip show <MODULE_NAME>
```

This lists all currently installed packages and their version, as of the publishing of this package, versions for the prerequisite packages uk-covid19, flask, and pytest are so.

```bash
Versions as of 03/12/2021

uk-covid19  - 1.2.2
Flask       - 2.0.2
pytest      - 6.2.5
```

---
### **INSTALLATION**  
---

To install the Covid19Dashboard, the package can be installed using [pip](https://pip.pypa.io/en/stable), similarly to the prerequisite modules necessary for the package to function. 

```bash
pip install Covid19Dashboard_ah1062
```

---
### **USAGE**
---

If the Package has been imported, the dashboard can be alternatively loaded by calling the run() function created in dashboard.py, as opposed to the execution of app.run() when the module is being run directly.

```python
from Covid19Dashboard_ah1062 import dashboard
dashboard.run()
```

Once the dashboard is running, the local development server can be accessed by web browser, using the url **127.0.0.1:5000**.

### *<u>Testing</u>*

Functionality of the Package can be assessed via the use of pytest, or the calling of a pytest function from within dashboard.py

```bash
cd <path/to/package>
pytest
```

**OR**

```python
from Covid19Dashboard_ah1062 import dashboard
dashboard.test_functions()
```

---
### **DETAILS**
---
