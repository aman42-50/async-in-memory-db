# async-in-memory-db

A lightweight, async Redis-like in-memory key-value store built with Python's asyncio.

## Features

- **Asyncio-based server** - Uses a single-threaded event loop with non-blocking I/O to handle many concurrent client connections without locks, avoiding race conditions and thread-per-connection overhead while keeping command execution atomic
- **TTL support** - Set expiration times on keys with EXPIRE and TTL commands
- **Lazy expiration** - Efficient memory management with automatic cleanup

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)

## Installation

Clone the repository:

```sh
git clone git@github.com:aman42-50/async-in-memory-db.git
cd async-in-memory-db
```

## Usage

### Start the Server

Run the server:

```bash
python server.py
```

You should see:

```
Async KV server running on 127.0.0.1:9876
```

The server is now listening for connections on port 9876.

### Connect with a Client

Open a new terminal and connect using `telnet`:

```bash
telnet 127.0.0.1 9876
```

Or using `nc` (netcat):

```bash
nc 127.0.0.1 9876
```

### Available Commands

This database implements a subset of Redis commands with basic functionality (no options/flags):

- **SET key value** - Store a key-value pair
- **GET key** - Retrieve a value by key
- **DEL key** - Delete a key
- **EXISTS key** - Check if a key exists
- **EXPIRE key seconds** - Set expiration time on a key
- **TTL key** - Get remaining time to live for a key

> **Note:** Commands follow Redis syntax but do not support additional options or flags. For example, `SET` does not support `EX`, `NX`, `XX` options.

### Example Session

```bash
$ telnet 127.0.0.1 9876

SET name Aman
OK

GET name
Aman

EXPIRE name 30
1

TTL name
27

DEL name
1

GET name
(nil)
```
