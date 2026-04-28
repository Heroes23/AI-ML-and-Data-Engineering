## Introduction to FastAPI

### Description

- `FastAPI` is another web framework in Python that allows an end user to create APIs and web application backend servers.

- FastAPI uses a protocol called `ASGI` which allows it to not only support synchronous workflows on the browser, but also asynchronous workflows on the browser (background queues, coroutines) to enable accelerated experiences for both APIs and web application servings.

- FastAPI depends on another web server technology called `uvicorn`, by default. The alternative option is called `starlette`.

### Installation and Setup

1. Install `fastapi` and `uvicorn` via `pip`.

- Create a `requirements.txt` file.

```txt
uvicorn
fastapi
```

- Run command for installing.

```bash
pip install -r requirements.txt
```

### Basic Usage

1. Create a FastAPI application.

- Create a file called `app.py`.

```python
from fastapi import FastAPI

# Build the app object
app = FastAPI()
```

2. Build routes.

- Build a `GET` route.

```python
...

@app.get(path='/data')
def get_data():
    return {
        'message' : 'This is a test!'
    }
```

- Build a `POST` route.

```python
...

@app.post(path='/register')
def register_user():
    return {
        'user_id' : 1,
        'status' : 'Registered successfully'
    }
```

3. Run the web server

- **Alternative 1**: Use the `uvicorn` CLI command.
    - The first `app` is the name of the Python file.
    - The second `app` is the name of the variable that contains your `FastAPI` class initialized as an object.

```bash
uvicorn app:app --host 0.0.0.0 --port 8003 --reload
```

- **Alternative 2**: Create the web server directly within the Python file.

```python
...

import uvicorn

# Run the web server
uvicorn.run(app=app, host=0.0.0.0, port=8003)
```

- Run the Python script directly.

```bash
python app.py
```

