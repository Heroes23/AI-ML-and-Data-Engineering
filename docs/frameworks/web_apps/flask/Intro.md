## Introduction to Flask

### Description

- Flask is a web framework in Python that allows an end user to create a web server, build URL endpoints for users to make requests to, and forward responses back to end users.

### Installation and Setup

1. Install `flask` via `pip`.

```bash
pip install flask
```

2. Test an import.

- Create a Python file called `app.py`.

```python
import flask

# Get the version of the package
v = flask.__version__

print(v)
```

### Basic Usage

1. Create an app object.

- Within your `app.py` file, get the `Flask` class.

```python
from flask import Flask

# Create the app object
app = Flask(__name__)
```

2. Create endpoints.

- `...` implies that we are expanding on the previous code block.

```python
...

# Endpoint to say "Hello, data!"

## Decorator
@app.route(rule='/greeting')
def greeting():
    # Return "Hello, data!"
    return "Hello, data!"
```

3. Run the web server.

```python
...

# Run the web server
app.run(host='0.0.0.0', port=8002, debug=True)
```