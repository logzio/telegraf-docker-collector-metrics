# Telegraf Docker Metrics Collector

To simplify shipping metrics from one or many sources, we created Docker Metrics Collector. Docker Metrics Collector is a container that runs Telegraf collector.

## Pull the Docker image of the Telegraf Docker Metrics Collector

```sh
docker pull logzio/telegraf-docker-collector-metrics
```

## Run the Telegraf Docker Metrics Collector

```sh
docker run --name telegraf-docker-collector-metrics \
 --env METRICS_TOKEN="<<METRICS-SHIPPING-TOKEN>>" \
 --env LOGZIO_LISTENER="<<LOGZIO_LISTENER>>" \
 -v /var/run/docker.sock:/var/run/docker.sock \
 logzio/telegraf-docker-collector-metrics:latest
```

If you prefer to store these environment variables in an [`.env` file](./docker.env), run the following command:

```sh
docker run -d --env-file=docker.env -v /var/run/docker.sock:/var/run/docker.sock logzio/telegraf-docker-collector-metrics:latest
```

| Name            | Description                                                                                                                                                                                                                                                                                                                                                                               |
| --------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| METRICS_TOKEN   | Your Logz.io metrics account token. Replace <<METRICS-SHIPPING-TOKEN>> with the token of the account you want to ship to.                                                                                                                                                                                                                                                                 |
| LOGZIO_LISTENER | Your Logz.io listener address, For example: `https://listener.logz.io:8053`.                                                                                                                                                                                                                                                                                                              |
| DOCKER_ENDPOINT | Address to reach the required Docker (default: `unix:///var/run/docker.sock`)Daemon.                                                                                                                                                                                                                                                                                                      |
| TIMEOUT         | The request timeout for any Docker Daemon query ( default: `5s`).                                                                                                                                                                                                                                                                                                                         |
| EXCLUED_IMAGES  | A list of strings, [regexes](https://pkg.go.dev/regexp), or [globs](https://github.com/gobwas/glob) whose referent container image names will not be among the queried containers. !-prefixed negations are possible for all item types to signify that only unmatched container image names should be monitored. For example:`imageNameToExclude1,imageNameToExclude2` ( default: `nil`) |

### Check Logz.io for your metrics

Give your metrics a few minutes to get from your system to ours,
and then open [Logz.io](https://app.logz.io/#/dashboard/metrics).

List of metrics:

-   docker_container_blkio_io_service_bytes_recursive_read
-   docker_container_blkio_io_service_bytes_recursive_write
-   docker_container_cpu_throttling_periods
-   docker_container_cpu_throttling_throttled_periods
-   docker_container_cpu_throttling_throttled_time
-   docker_container_cpu_usage_in_kernelmode
-   docker_container_cpu_usage_in_usermode
-   docker_container_cpu_usage_percent
-   docker_container_cpu_usage_system
-   docker_container_cpu_usage_total
-   docker_container_mem_active_anon
-   docker_container_mem_active_file
-   docker_container_mem_inactive_anon
-   docker_container_mem_inactive_file
-   docker_container_mem_limit
-   docker_container_mem_max_usage
-   docker_container_mem_pgfault
-   docker_container_mem_pgmajfault
-   docker_container_mem_unevictable
-   docker_container_mem_usage
-   docker_container_mem_usage_percent
-   docker_container_net_rx_bytes
-   docker_container_net_rx_dropped
-   docker_container_net_rx_errors
-   docker_container_net_rx_packets
-   docker_container_net_tx_bytes
-   docker_container_net_tx_dropped
-   docker_container_net_tx_errors
-   docker_container_net_tx_packets
-   docker_container_status_exitcode
-   docker_container_status_finished_at
-   docker_container_status_oomkilled
-   docker_container_status_pid
-   docker_container_status_started_at
-   docker_container_status_uptime_ns
-   docker_memory_total
-   docker_n_containers
-   docker_n_containers_paused
-   docker_n_containers_running
-   docker_n_containers_stopped
-   docker_n_cpusdocker_n_goroutines
-   docker_n_images
-   docker_n_listener_events
-   docker_n_used_file_descriptors

## Changelog

1.0.0:

-   Initial Release

## License

Licensed under the [Apache 2.0](http://apache.org/licenses/LICENSE-2.0.txt) License.
