"""Detect broadcast storms on switch ports.

Usage: python3 main.py broadcast.csv [--max-pps 100]
CSV columns: switch,port,broadcast_pps (broadcast packets
per second seen on the port). Verdicts:
- STORM: over 5x --max-pps (default 100, so over 500) — the
  port is flooding the network.
- HIGH: over --max-pps but not a storm — worth watching.
- OK: at or under --max-pps.
Highest broadcast rate first. Rows with a non-numeric
broadcast_pps are reported as skipped, not silently dropped.
"""
import argparse, csv, sys

STORM_MULTIPLIER = 5

def detect(rows, max_pps=100):
    out = []
    skipped = 0
    for row in rows:
        try:
            switch = row["switch"].strip()
            port = row["port"].strip()
            pps = int(row["broadcast_pps"])
            if not switch or not port:
                raise ValueError("missing value")
        except (KeyError, AttributeError, ValueError, TypeError):
            skipped += 1
            continue
        if pps > STORM_MULTIPLIER * max_pps:
            verdict = "STORM"
            detail = f"{pps} pps, over {STORM_MULTIPLIER * max_pps} pps storm level"
        elif pps > max_pps:
            verdict = "HIGH"
            detail = f"{pps} pps, over {max_pps} pps limit"
        else:
            verdict = "OK"
            detail = f"{pps} pps, within {max_pps} pps limit"
        out.append((switch, port, pps, verdict, detail))
    out.sort(key=lambda r: (-r[2], r[0], r[1]))
    return out, skipped

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--max-pps", type=int, default=100)
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results, skipped = detect(list(csv.DictReader(f)), args.max_pps)
    for switch, port, _, verdict, detail in results:
        print(f"{switch} {port}: {verdict} - {detail}")
    counts = {v: sum(1 for *_, verdict, _ in results if verdict == v)
              for v in ("STORM", "HIGH", "OK")}
    print(f"{counts['STORM']} storm port(s), {counts['HIGH']} high, "
          f"{counts['OK']} ok out of {len(results)} port(s).")
    if skipped:
        print(f"Skipped {skipped} invalid row(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
