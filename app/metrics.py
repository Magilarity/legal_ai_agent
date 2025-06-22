from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter('requests_total', 'Total request count', ['endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['endpoint'])

def init_metrics(port=8000):
    # Start up the server to expose the metrics.
    start_http_server(port)
