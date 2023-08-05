# OCPP-ASGI

ocpp-asgi provides **ASGI compliant** interface for implementing **event-driven** **server-side** support for OCPP protocol with Python. It depends on and extends [mobilityhouse/ocpp](https://github.com/mobilityhouse/ocpp). 

The key features are:
* ASGI compliant interface supporting both WebSocket and HTTP protocols.
* Event-driven and "stateless" approach for implementing action handlers for OCPP messages. 
* Highly-scalable and supports serverless (e.g. AWS Lambda) with compatible ASGI server.
* Requires small and straightforward changes from ocpp to action handlers (but is not backwards compatible).

Disclaimer! This library is still in alpha state. It has some rough edges.

# Getting started

## Installation

```
pip install ocpp-asgi
```

Also ASGI server is required e.g. [uvicorn](https://www.uvicorn.org) or [mangum](https://www.uvicorn.org) when deployed to AWS Lambda with API Gateway.
```
pip install uvicorn
```

## Run the examples

There are two kind of examples how to implement central system with ocpp-asgi: standalone and serverless. Both examples use same ocpp action handlers (routers).

### Running standalone example

Run the following commands e.g. in different terminal windows (or run the files within IDE).

Start Central System:
```
python ./examples/central_system/standalone/central_system.py
```

Start Charging Station:
```
python ./examples/charging_station.py
```

### Running serverless example

Run the following commands in different terminal windows (or run the files within IDE).

Start Central System HTTP backend:
```
python ./examples/central_system/serverless/central_system_http.py
```

Start Central System WebSocket proxy:
```
python ./examples/central_system/serverless/central_system_proxy.py
```

Start Charging Station:
```
python ./examples/charging_station.py
```