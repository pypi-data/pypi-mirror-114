# Flask Scenario Testing
A small library to run load tests against Flask applications using realistic loads.

## How to use

#### Installation
To install using pip, run this:
    
    pip install flask-scenario-testing
    
#### Setup
You need to add the scenario testing endpoints to your application to be able to run simulations against your application. To do this, you need the following steps:

#### Running simulations
To run a simulation you can use the binary `run-simulation` that's included in the package. Example command:

```
run-simulation --hostname 32.152.71.210 --locust-file locustfile.py --port 5000 --config test.json
```

#### Analysis
