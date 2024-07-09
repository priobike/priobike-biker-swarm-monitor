# Biker Swarm Monitor

A microservice to receive and monitor data from the [bikerswarm](https://github.com/priobike/priobike-biker-swarm).

## Quickstart

The easiest way to run the biker swarm monitor is to use the contained `docker-compose`:
```
docker-compose up
```
## API and CLI

### REST Endpoints

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
## Contributing

We highly encourage you to open an issue or a pull request. You can also use our repository freely with the `MIT` license.

Every service runs through testing before it is deployed in our release setup. Read more in our [PrioBike deployment readme](https://github.com/priobike/.github/blob/main/wiki/deployment.md) to understand how specific branches/tags are deployed.

## Anything unclear?

Help us improve this documentation. If you have any problems or unclarities, feel free to open an issue.
