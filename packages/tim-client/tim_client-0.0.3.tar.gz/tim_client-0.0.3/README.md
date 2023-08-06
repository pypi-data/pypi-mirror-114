# TIM Python Client V5

Python SDK to use the V5 Engine of TIM. This include helper methods to:
- upload a dataset
- create a forecast with a dataset
- ...

## Usage

### Installation
To install package run: `pip install tim-client`

### Initiation
```
from tim import Tim

client = Tim(email='',password='')
```

### Methods
Tim provides following helper methods:
- `client.upload_dataset`
- `client.create_forecast`
- `client.execute_forecast`
- `client.get_forecast_results`
- `client.create_and_execute_forecast_job`
- `client.create_anomaly_detection`
- `client.execute_anomaly_detection`
- `client.create_and_execute_anomaly_detection`
- `client.get_anomaly_detection_job_results`

### Error handling
Minimal validation is performed by the tim-client, errors will be raised by the server

### Documentation
Full documentation of the API can be found at: https://docs.tangent.works
