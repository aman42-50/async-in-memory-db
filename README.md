# async-in-memory-db

A lightweight, async Redis-like in-memory key-value store built with Python's asyncio.

## Features

- **Asyncio-based server** - Handle multiple clients concurrently without blocking
- **String operations** - GET, SET, DEL, EXISTS commands
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

**Using telnet:**

```bash
telnet 127.0.0.1 9876
```

### Available Commands

Once connected, you can use the following commands:

#### SET - Store a key-value pair

```
SET key value
```

Response: `OK`

#### GET - Retrieve a value by key

```
GET key
```

Response: `value` (or `(nil)` if key doesn't exist)

#### DEL - Delete a key

```
DEL key
```

Response: `1` (if deleted) or `0` (if key didn't exist)

#### EXPIRE - Set expiration time on a key (in seconds)

```
SET key value
EXPIRE key 10
```

Response: `1` (expiration set) or `0` (key doesn't exist)

After 10 seconds, the key will automatically expire.

#### TTL - Get remaining time to live for a key (in seconds)

```
TTL key
```

Response:

- Remaining seconds (e.g., `8`)
- `-1` if key exists but has no expiration
- `-2` if key doesn't exist

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
