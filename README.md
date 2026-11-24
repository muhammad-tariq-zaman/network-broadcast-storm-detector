# network-broadcast-storm-detector

Detect broadcast storms on switch ports: the input CSV lists switch, port and broadcast_pps (broadcast packets per second seen on the port) — STORM when over 5x --max-pps (default 100, so over 500 pps — the port is flooding the network), HIGH when over --max-pps but not a storm, OK at or under --max-pps — highest broadcast rate first. Rows with a non-numeric broadcast_pps are reported as skipped, not silently dropped.

Sample input is included (sample.csv with six ports, one invalid row).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
SW-01 Gi0/1: STORM - 1200 pps, over 500 pps storm level
SW-01 Gi0/2: HIGH - 250 pps, over 100 pps limit
SW-02 Gi0/5: HIGH - 180 pps, over 100 pps limit
SW-02 Gi0/6: OK - 95 pps, within 100 pps limit
SW-01 Gi0/3: OK - 40 pps, within 100 pps limit
1 storm port(s), 2 high, 2 ok out of 5 port(s).
Skipped 1 invalid row(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
