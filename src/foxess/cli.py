"""Minimal command-line interface.

    fox models                       # list known models from the register map
    fox decode <id> <tbl_hex>        # decode a captured tbl payload offline
    fox read <host> <addr> <id>      # read+decode a live model from a device
    fox scan <host> <addr>           # probe which models a device exposes

JSON output with ``--json``. This is an intentionally small starting CLI; the
full command set (Deliverable #10) builds on it.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .decoder import decode
from .frame import reassemble_hex
from .registry import default_registry


def _print_model(model: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps({f.name: f.value for f in model.fields}, default=str))
        return
    print(f"# addr={model.addr} id={model.id} {model.name}")
    for f in model.fields:
        unit = f" {f.unit}" if f.unit else ""
        print(f"  {f.name:<24}{str(f.value)}{unit}")


def _cmd_models(args: argparse.Namespace) -> int:
    reg = default_registry()
    if args.json:
        print(json.dumps([{"id": m.id, "name": m.name, "fields": len(m.fields)} for m in reg]))
    else:
        for m in reg:
            print(f"{m.id:<7}{m.name:<38} fields={len(m.fields)} start={m.modbus_address}")
    return 0


def _cmd_decode(args: argparse.Namespace) -> int:
    frame = reassemble_hex(args.tbl_hex, validate_crc=not args.no_crc)
    model = decode(frame.payload, args.id)
    _print_model(model, args.json)
    return 0


def _cmd_read(args: argparse.Namespace) -> int:
    from .client import FoxESS

    with FoxESS(args.host) as fox:
        _print_model(fox.read_model(args.addr, args.id), args.json)
    return 0


def _cmd_scan(args: argparse.Namespace) -> int:
    from .client import FoxESS

    with FoxESS(args.host) as fox:
        result = fox.scan(args.addr)
    present = [mid for mid, ok in result.items() if ok]
    if args.json:
        print(json.dumps(result))
    else:
        print(f"addr={args.addr}: {len(present)} models present: {present}")
    return 0


def _cmd_mqtt(args: argparse.Namespace) -> int:
    from .client import FoxESS
    from .mqtt import MqttConfig, MqttPublisher

    cfg = MqttConfig(
        host=args.broker,
        port=args.port,
        username=args.username,
        password=args.password,
        prefix=args.prefix,
        discovery_prefix=args.discovery_prefix,
        interval=args.interval,
    )
    with FoxESS(args.host) as fox:
        try:
            MqttPublisher(fox, cfg).run()
        except KeyboardInterrupt:
            return 0
    return 0


def _cmd_exporter(args: argparse.Namespace) -> int:
    from .client import FoxESS
    from .prometheus import serve

    try:
        import prometheus_client  # noqa: F401
    except ImportError:
        print(
            "fox exporter requires the [prometheus] extra: "
            "pip install 'foxess-local[prometheus]'",
            file=sys.stderr,
        )
        return 2
    with FoxESS(args.host) as fox:
        try:
            serve(fox, host=args.bind, port=args.port)
        except KeyboardInterrupt:
            return 0
    return 0


def _cmd_serve(args: argparse.Namespace) -> int:
    import os

    try:
        import uvicorn
    except ImportError:
        print(
            "fox serve requires the [api] extra: pip install 'foxess-local[api]'", file=sys.stderr
        )
        return 2
    os.environ["FOX_HOST"] = args.host
    from .api import create_app

    uvicorn.run(create_app(), host=args.bind, port=args.port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fox", description="FoxESS local SDK CLI")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("models", help="list models in the register map")

    d = sub.add_parser("decode", help="decode a tbl hex payload offline")
    d.add_argument("id", type=int)
    d.add_argument("tbl_hex")
    d.add_argument("--no-crc", action="store_true", help="skip CRC validation")

    r = sub.add_parser("read", help="read a live model from a device")
    r.add_argument("host")
    r.add_argument("addr", type=int)
    r.add_argument("id", type=int)

    s = sub.add_parser("scan", help="probe which models a device exposes")
    s.add_argument("host")
    s.add_argument("addr", type=int)

    sv = sub.add_parser("serve", help="run the read-only REST API (needs [api] extra)")
    sv.add_argument("host", help="device IP")
    sv.add_argument("--bind", default="127.0.0.1")
    sv.add_argument("--port", type=int, default=8080)

    m = sub.add_parser("mqtt", help="publish to MQTT + Home Assistant (needs [mqtt] extra)")
    m.add_argument("host", help="device IP")
    m.add_argument("--broker", default="localhost", help="MQTT broker host")
    m.add_argument("--port", type=int, default=1883)
    m.add_argument("--username")
    m.add_argument("--password")
    m.add_argument("--prefix", default="fox", help="MQTT topic prefix")
    m.add_argument("--discovery-prefix", default="homeassistant")
    m.add_argument("--interval", type=float, default=15.0, help="publish interval (s)")

    e = sub.add_parser("exporter", help="run the Prometheus exporter (needs [prometheus] extra)")
    e.add_argument("host", help="device IP")
    e.add_argument("--bind", default="0.0.0.0")  # noqa: S104
    e.add_argument("--port", type=int, default=9110)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    dispatch = {
        "models": _cmd_models,
        "decode": _cmd_decode,
        "read": _cmd_read,
        "scan": _cmd_scan,
        "serve": _cmd_serve,
        "mqtt": _cmd_mqtt,
        "exporter": _cmd_exporter,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
