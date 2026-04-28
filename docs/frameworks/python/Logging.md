# Python Logging Guide: `logging` vs `loguru`

When building Python applications, robust logging is critical. Python's built-in `logging` module is powerful but can be verbose to set up correctly. The third-party library `loguru` attempts to solve this verbosity by providing a pre-configured, colorful, and highly intuitive logging interface out of the box.

This guide explores how to implement both libraries across various operational setups.

## 1. Simple Scripting

For simple, single-file scripts or small automation tasks, you want a logger that is quick to set up and provides immediate feedback.

### Using Built-in `logging`
The built-in module requires basic configuration to set the log level and format. If you don't configure it, `INFO` and `DEBUG` logs will not print to the console by default.

```python
import logging

# Basic configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def process_data(file_path: str):
    logging.info(f"Starting to process {file_path}")
    try:
        # Simulate work
        with open(file_path, "r") as f:
            data = f.read()
        logging.debug(f"Read {len(data)} bytes")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")

process_data("data.csv")
```

### Using `loguru`
`loguru` is practically zero-setup. You just import the `logger` object and start using it. It comes with colored output, sensible default formatting, and automatic traceback formatting.

```python
from loguru import logger
import sys

# Optional: Adjust the default sink if you want to change log level
logger.remove()
logger.add(sys.stderr, level="INFO")

def process_data(file_path: str):
    logger.info(f"Starting to process {file_path}")
    try:
        with open(file_path, "r") as f:
            data = f.read()
        logger.debug(f"Read {len(data)} bytes") # Won't show if level="INFO"
    except FileNotFoundError:
        # loguru automatically captures the exception context nicely
        logger.exception(f"File not found: {file_path}")

process_data("data.csv")
```

## 2. Data Engineering Workflows

In Data Engineering (ETL/ELT pipelines), tracing data transformation steps, recording metric counts, and logging to a central file (or shipping logs) is highly important. You also often need log rotation so log files don't grow infinitely large.

### Using Built-in `logging`
To implement file logging with rotation, we must use file handlers.

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("etl_pipeline")
logger.setLevel(logging.INFO)

# Setup Rotating File Handler (max 5MB per file, keep 3 backups)
handler = RotatingFileHandler("etl_run.log", maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def extract_data():
    logger.info("Extracting data from source DB")
    # code...
    logger.info({"event": "extraction_complete", "rows": 15000})

extract_data()
```

### Using `loguru`
`loguru` handles file rotation and retention natively via the `add()` method, making it extremely easy to manage for data pipelines.

```python
from loguru import logger
import json

# Log to console AND a rotating file
logger.add(
    "logs/etl_run_{time}.log", 
    rotation="500 MB",     # Create new file when size is reached
    retention="10 days",   # Automatically clean up old logs
    compression="zip",     # Compress archived logs
    level="INFO"
)

def extract_data():
    logger.info("Extracting data from source DB")
    # We can easily serialize dictionaries for structured logging down the pipe
    logger.bind(event="extraction_complete", rows=15000).info("Extraction metrics")

extract_data()
```

## 3. API Setup with FastAPI

When building web APIs with FastAPI, logging needs to track request IDs, capture HTTP traffic, and fit into an asynchronous paradigm. FastAPI uses `uvicorn` under the hood, which has its own logging setup, sometimes causing conflicts.

### Using Built-in `logging`
Usually, you configure standard logging at the startup of the FastAPI app and rely on Uvicorn's access logs.

```python
import logging
from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_logger")

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Completed request: {response.status_code}")
    return response

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    logger.debug(f"Fetching item {item_id}")
    return {"item_id": item_id}
```

### Using `loguru`
To truly integrate `loguru` with FastAPI, you often need to intercept standard logging messages (like those generated by `uvicorn.error` and `uvicorn.access`) and pipe them into `loguru`.

```python
import logging
import sys
from fastapi import FastAPI, Request
from loguru import logger

class InterceptHandler(logging.Handler):
    """Intercept standard logging messages and route them to Loguru."""
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

# Setup loguru and intercept standard logs
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
logger.configure(handlers=[{"sink": sys.stdout, "level": "INFO"}])

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Bind contextual request data (like an IP address) seamlessly
    with logger.contextualize(client_ip=request.client.host):
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        return response

@app.get("/items")
async def get_items():
    logger.info("Fetching items from database")
    return {"status": "success"}
```

## 4. AI Engineering Workflows (Langchain / LangGraph)

In AI workflows, logging is crucial for tracking prompt templates, LLM responses, token usage, and complex agent trajectories (spans). Tracing tools (like LangSmith or Arize) often handle the heavy lifting, but standard logging is still needed for the control plane.

### Using Built-in `logging`
Langchain has internal standard logging that can be set to verbose.

```python
import logging
from langchain_core.globals import set_debug, set_verbose

# Enable verbose standard logging for LangChain
set_debug(True) 
set_verbose(True)

# Standard Python logger for your own agent loop logic
logger = logging.getLogger("agent_loop")
logger.setLevel(logging.INFO)

def run_agent():
    logger.info("Initializing LangGraph state")
    # Run graph
    logger.info("Agent execution completed.")

run_agent()
```

### Using `loguru`
`loguru` is helpful here because AI execution traces often involve massive strings (LLM outputs) and complex JSON structures. `loguru` colorizes and safely formats these large objects much better than standard logging.

```python
from loguru import logger
import os

logger.add("ai_traces.log", level="DEBUG", serialize=True) # serialize=True writes logs as JSON

def run_rag_pipeline(query: str):
    logger.info(f"Received query: {query}")
    
    # 1. Retrieve
    logger.debug("Executing vector search")
    docs = [{"id": 1, "text": "AI context"}]
    
    # 2. Generate
    # Using 'bind' to easily track token counts or specific model versions
    model_logger = logger.bind(model="gpt-4o", tokens_used=150)
    model_logger.info("Invoking LLM with retrieved context")
    
    try:
        response = "The answer based on AI context."
        logger.success("Generation successful")
        return response
    except Exception as e:
        logger.exception("LLM Provider failed to respond")
        raise e

run_rag_pipeline("What is AI?")
```

## Summary Recommendation

*   **Stick to `logging` if:** You are writing a distributable third-party library/package (to avoid forcing dependencies on your users), or you are tightly restricted to standard library primitives.
*   **Embrace `loguru` if:** You are building applications (Scripts, Data Pipelines, APIs, LLM Agents) and want a massive developer experience improvement with structured logging, effortless file rotation, beautiful terminal output, and simplified exception tracking.
