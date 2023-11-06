# Biker Swarm Monitor

A microservice to receive and monitor data from the biker swarm.

## Quickstart

```
docker-compose up
```

## REST Endpoints

#### POST /crashReport/post/

```bash
curl --data "@example-crash-report.json" -X POST -H "Content-Type: application/json" http://localhost/production/biker-swarm-monitor/crashReports/post/
```
Result:
```json
{
    "success": true
}
```
