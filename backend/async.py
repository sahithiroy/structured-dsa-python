'''
Async and wait are keywords in Python that allow you to write asynchronous code. 
Asynchronous programming is a programming paradigm that allows you to write code that can perform multiple tasks concurrently, without blocking the execution of other tasks.
Asynchronous function is defined using the async keyword, and it can be paused and resumed using the await keyword.
when we use async and await keywords in python, we can write code that is more efficient and responsive, especially when dealing with I/O-bound operations like network requests or file I/O.
when we not use async and await keywords in python, the code will be executed sequentially, and it will block the execution of other tasks until the current task is completed.
Scenarios for the not use for async and wait keywords in python:
1. CPU-bound operations: If your code is performing CPU-bound operations, such as heavy computations or data processing, using async and await may not provide any performance benefits. In fact, it may even introduce overhead and slow down your code.
2. Simple I/O operations: If your code is performing simple I/O operations, such as reading or writing small files, using async and await may not provide any performance benefits. In fact, it may even introduce complexity and make your code harder to read and maintain.
Scenarios for the use for async and wait keywords in python:
1. Network requests: If your code is making network requests, such as calling APIs or fetching data from a remote server, using async and await can help you avoid blocking the execution of other tasks while waiting for the response.
2. File I/O: If your code is performing file I/O operations, such as reading or writing large files, using async and await can help you avoid blocking the execution of other tasks while waiting for the file operation to complete.

what's the difference b/w parallelism and concurrency:
parallelism is the ability of a system to perform multiple tasks simultaneously,
 while concurrency is the ability of a system to handle multiple tasks at the same time, but not necessarily simultaneously.
 scenarios for the use of parallelism and concurrency:
1. Parallelism: If your code is performing CPU-bound operations, such as heavy computations or data processing, using parallelism can help you take advantage of multiple CPU cores and speed up your code.
2. Concurrency: If your code is performing I/O-bound operations, such as network requests or file I/O, using concurrency can help you avoid blocking the execution of other tasks while waiting for the I/O operation to complete.
can you expalin what is the cpu-bound and I/O-bound operations in python:
CPU-bound operations are tasks that require a lot of processing power from the CPU, such as complex calculations or data processing. These tasks can be parallelized to take advantage of multiple CPU cores and speed up the execution time.
I/O-bound operations are tasks that involve waiting for input/output operations to complete, such as reading from a file or making a network request. These tasks can be made concurrent to avoid blocking the execution of other tasks while waiting for the I/O operation to complete.


what is co-routine in python:
A coroutine is a special type of function in Python that can be paused and resumed, allowing for asynchronous programming. Coroutines are defined using the async keyword and can be paused using the await keyword. When a coroutine is paused, 
it allows other tasks to run concurrently, making it useful for I/O-bound operations.
'''
#Example of async and wait
import asyncio


async def fetch_data():
    # Simulate an asynchronous operation, such as fetching data from an API
    await asyncio.sleep(2)  # Simulating a delay of 2 seconds
    return "Data fetched successfully"


def main():
    return "Starting the program..."

async def run():
    return await main() + " " + await fetch_data()

output = asyncio.run(run())
print(output)



#example async and awit with concurrency and parallelism
import asyncio
async def task1():
    print("Task 1 started")
    await asyncio.sleep(2)
    print("Task 1 completed")

async def task2():
    print("Task 2 started")
    await asyncio.sleep(1)
    print("Task 2 completed")

