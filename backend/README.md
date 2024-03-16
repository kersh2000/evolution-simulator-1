# Evolution Simulator - Backend README File

## Setting Up the Development Environment

To ensure consistency and manage dependencies efficiently, we recommend using a virtual environment for local development. Follow the steps below to set up your development environment.

### Prerequisites

Ensure you have **Python 3.7** or higher and **pip** installed on your machine:

```
python --version
pip --version
```

### Creating a Virtual Environment
Navigate to the backend directory of the project and create a virtual environment:
```
# Navigate to the backend directory
cd path/to/backend

# Create a virtual environment named 'venv'
python -m venv venv
```

### Activating the Virtual Environment
Before installing the dependencies, you need to activate the virtual environment. The activation command differs based on the operating system:

- *Windows*
```
.\venv\Scripts\activate
```

- *Linux*
```
source venv/bin/activate
```
You should now see (venv) prefixed to your command prompt, indicating that the virtual environment is active.

### Confirm Virtual Environment:
In order to confirm the right Python interpreter is being used from the virtual environment, you can check the path of the Python executable:
- *Windows*
```
where python
```
- *Linux*
```
which python
```
The output should point to the Python interpreter within the venv directory of your project.

### Installing Dependencies

With the virtual environment activated, install the required packages using the **requirements.txt** file:
```
pip install -r requirements.txt
```
This command will install all the necessary Python packages listed in **requirements.txt** within your virtual environment.

### Deactivating the Virtual Environment
After you've completed your work or if you need to exit the virtual environment, you can deactivate it by running:
```
deactivate
```

This command will return you to the global Python environment.