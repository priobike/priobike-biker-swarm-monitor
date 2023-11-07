# Biker Swarm Monitor

A microservice to receive and monitor data from the biker swarm.

## Quickstart

```
docker-compose up
```

## REST Endpoints

#### POST /crashReport/crash/post/

```bash
curl --data "@example-crash-report.json" -X POST -H "Content-Type: application/json" http://localhost/production/biker-swarm-monitor/crashReports/crash/post/
```
Result:
```json
{
    "success": true
}
```

#### POST /crashReport/success/post/

```bash
curl --data "@example-success-report.json" -X POST -H "Content-Type: application/json" http://localhost/production/biker-swarm-monitor/crashReports/success/post/
```
Result:
```json
{
    "success": true
}
```
