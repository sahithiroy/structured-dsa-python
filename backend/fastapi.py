'''
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
why we are using fastapi instead of other frameworks because:
1. High Performance: FastAPI is one of the fastest Python frameworks available, on par with Go and Node.js.
2. Automatic Documentation: FastAPI automatically generates interactive API documentation.
3. Type Safety: FastAPI uses Python type hints for automatic validation and serialization.
4. Easy to Use: FastAPI is easy to learn and use, with a simple and intuitive API.
5. Async Support: FastAPI has excellent support for asynchronous programming.

An ASGI (Asynchronous Server Gateway Interface) server is a Python standard that bridges asynchronous web servers and Python frameworks. 
Serving as the modern successor to WSGI, it handles multiple concurrent connections simultaneously. 
It is widely used for real-time applications and protocols like WebSockets.

Components of FastAPI:
1.Endpoints: Define the routes and methods for your API.
2.Request and Response Models: Use Pydantic models to define the structure of your requests and responses.
3.Data Models: Define your data models using Pydantic for validation and serialization. 
pydnatic is a data validation and settings management library for Python, based on Python type annotations. 
It allows you to define data models with type hints, and automatically validates and serializes the data.
example of pydantic model:
```python   
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```
4.Dependency Injection: FastAPI has a built-in dependency injection system that allows you to manage dependencies easily.
Dependencies can be used for authentication, database connections, external services, etc.
how fastapi handles dependency injection:
simple example of dependency injection in fastapi:
Depends write normal function and use it as a dependency in your endpoint function.
like when i create the the function of depends on the owner and user based on the owner and user i can use it in my endpoint function as a dependency.

5.Response Handling: FastAPI provides a flexible way to handle responses, including custom response classes and status codes.

6.middleware: FastAPI allows you to add middleware to your application for tasks like logging, authentication, and more.
what is middleware in fastapi:
Middleware is a function that runs before and/or after each request. It can be used to modify the request or response, perform logging, handle authentication, and more. 
Middleware can be added to the FastAPI application using the `add_middleware` method.



1. The Core Architectural ComponentsFastAPI is not a monolithic framework built from scratch. 
It is an orchestration layer that beautifully synthesizes three core open-source components:   
      ┌────────────────────────────────────────────────────────┐
      │                        FastAPI                         │
      │  (Routing, Dependency Injection, Security, Docs)       │
      └───────────────┬────────────────────────┬───────────────┘
                      │                        │
                      ▼                        ▼
         ┌────────────────────────┐  ┌───────────────────┐
         │        Starlette       │  │     Pydantic      │
         │  (ASGI Engine, HTTP,   │  │  (Data Validation,│
         │   WebSockets, Async)   │  │   Serialization)  │
         └────────────────────────┘  └───────────────────┘
Starlette (The Engine Layer): A lightweight ASGI (Asynchronous Server Gateway Interface) framework. 
It handles all the low-level web routing, HTTP requests, WebSockets, background tasks, and asynchronous lifecycle events.
Pydantic (The Data & Validation Layer): Handles data parsing, serialization (converting Python objects to JSON), and structural validation. 
If a client sends an invalid schema to a FastAPI route, Pydantic intercepts it automatically and rejects it with a 422 Unprocessable Entity error before it ever touches your business logic.
FastAPI (The Orchestration Layer): Adds automatic Swagger/OpenAPI documentation generation, type-hint-driven route parameters, and a powerful, composable Dependency Injection system (using Depends()).
2. The Asynchronous Execution Model (ASGI vs. WSGI)Traditional Python frameworks like Django (historically) or Flask rely on WSGI (Web Server Gateway Interface). 
WSGI is inherently synchronous and follows a thread-per-request model.The WSGI Problem (Flask/Django):If your backend receives a request to process a heavy Map-Reduce LLM summarization pipeline, the server assigns a worker thread to that request. 
If that thread has to wait 5 seconds for the external LLM API to respond, the thread is completely blocked. It sits idle, wasting memory and unable to handle other incoming users. 
To scale, you must spawn hundreds of heavy system threads.  
The ASGI Solution (FastAPI):FastAPI uses ASGI, which communicates via an asynchronous event loop (typically driven by Uvicorn).[Incoming Request] ──► [Event Loop] ──► [Route: async def] ──► [Awaits LLM API/DB]
                             │                                       │
                             │ (Thread released to serve next user)  │
                             ▼                                       ▼
                       [Handles User 2] ◄────────────────────── [Callback: Resumes]
When you define a route using async def and invoke an external API call using await (such as calling an LLM or waiting for a webhook event), the worker thread yields control back to the event loop. The thread does not sit around waiting. Instead, it immediately moves to serve the next user's incoming request. When the external LLM finishes generating text, it triggers an event, and the loop resumes your original function right where it left off.  3. High-Performance Request-Response LifecycleWhen a client hits an endpoint on a production FastAPI backend, the data travels through this multi-layered architectural pipeline:[Client Request JSON Payload]
             │
             ▼
[Uvicorn Server (ASGI Event Loop Middleware)]
             │
             ▼
[Starlette Routing Engine]
             │
             ▼
[Pydantic Validation (Checks Types/Constraints against Request Schema)]
             │
             ▼
[Dependency Injection Layer (Resolves DB sessions, Auth, CORS states)]
             │
             ▼
[Your Application Core Code (Business Logic / Async Functions)]
             │
             ▼
[Pydantic Serialization (Converts Python schemas/objects back to raw JSON)]
             │
             ▼
[Client Response Output Stream]
4. How to Pitch This Architecture in a 30 LPA InterviewIf an interviewer asks:
 "Why did you choose FastAPI for your SummifyWeb project?", structure your answer around performance and engineering efficiency using this script:  "I selected FastAPI over traditional synchronous WSGI frameworks because GenAI workloads are heavily I/O-bound. 
Our platform handles long-running text extraction and Map-Reduce summaries.  
By running an ASGI architecture via Uvicorn, we can leverage Python's native async/await event loop. When the server awaits a response from the external Groq or OpenAI APIs, the main thread is never blocked. 
It is immediately freed up to ingest incoming concurrent requests or stream real-time tokens back to our Chrome Extension UI.  
Additionally, leveraging Pydantic directly at the framework layer ensures that schema validation and response serialization happen at compiling speeds, while providing strict type safety for our LLM-as-a-Judge evaluation data.
'''