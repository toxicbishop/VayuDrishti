#!/usr/bin/env python3
"""Unified Demo Runner for VayuDrishti.

Runs the full demo environment (Next.js web application + Streamlit research dashboard)
concurrently in a single terminal with unified logging and graceful shutdown.
Optionally runs or updates the synthetic simulation pipeline beforehand.

Usage:
    python scripts/run_demo.py               # Run web app + dashboard
    python scripts/run_demo.py --pipeline    # Run simulation pipeline first, then start demo
    python scripts/run_demo.py --no-dashboard # Run only the Next.js web app
    python scripts/run_demo.py --no-web      # Run only the Streamlit dashboard
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import signal
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IS_WINDOWS = platform.system() == "Windows"


def log(prefix: str, msg: str, color_code: str = "36"):
    """Print formatted message with prefix."""
    # ANSI escape colors
    colored_prefix = f"\033[1;{color_code}m[{prefix}]\033[0m"
    print(f"{colored_prefix} {msg}", flush=True)


def check_node_modules():
    """Verify frontend dependencies exist; if not, instruct or run pnpm install."""
    node_modules = ROOT / "node_modules"
    if not node_modules.exists():
        log("setup", "node_modules not found. Running 'pnpm install'...", "33")
        pnpm = shutil.which("pnpm")
        if not pnpm:
            log("error", "pnpm was not found on PATH. Please install pnpm (https://pnpm.io).", "31")
            sys.exit(1)
        res = subprocess.run([pnpm, "install"], cwd=ROOT)
        if res.returncode != 0:
            log("error", "pnpm install failed. Please check dependencies.", "31")
            sys.exit(res.returncode)


def check_data_artifacts(force_pipeline: bool = False, fast_mode: bool = True):
    """Ensure public/data/ contains required json files; run pipeline if missing or forced."""
    required = [
        ROOT / "public" / "data" / "aqi_frames.json",
        ROOT / "public" / "data" / "gas_grids.json",
        ROOT / "public" / "data" / "hotspots.json",
    ]
    missing = [p for p in required if not p.exists()]
    if missing or force_pipeline:
        if force_pipeline:
            log("pipeline", "Forced pipeline run requested. Running synthetic simulation...", "35")
        else:
            log("pipeline", f"Missing demo artifacts ({len(missing)} files). Generating data...", "35")

        cmd = [sys.executable, str(ROOT / "pipelines" / "run_demo.py")]
        if fast_mode:
            cmd.append("--fast")
        
        log("pipeline", f"Running: {' '.join(cmd)}", "35")
        res = subprocess.run(cmd, cwd=ROOT)
        if res.returncode != 0:
            log("error", "Synthetic simulation failed.", "31")
            sys.exit(res.returncode)

        export_cmd = [sys.executable, str(ROOT / "pipelines" / "export_web.py")]
        log("pipeline", f"Exporting layers: {' '.join(export_cmd)}", "35")
        res_exp = subprocess.run(export_cmd, cwd=ROOT)
        if res_exp.returncode != 0:
            log("error", "Export to web data failed.", "31")
            sys.exit(res_exp.returncode)

        log("pipeline", "Demo dataset successfully generated and exported!", "32")


def stream_output(pipe, prefix: str, color_code: str):
    """Read lines from process pipe and print with colored prefix."""
    try:
        for line in iter(pipe.readline, ""):
            if not line:
                break
            stripped = line.rstrip("\r\n")
            if stripped:
                log(prefix, stripped, color_code)
    except Exception:
        pass
    finally:
        try:
            pipe.close()
        except Exception:
            pass


def kill_proc_tree(proc: subprocess.Popen):
    """Cleanly terminate process and all child processes across platforms."""
    if proc.poll() is not None:
        return
    pid = proc.pid
    if IS_WINDOWS:
        try:
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except Exception:
            proc.terminate()
    else:
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
        except Exception:
            proc.terminate()


def main():
    parser = argparse.ArgumentParser(description="Run VayuDrishti unified demo servers.")
    parser.add_argument("--pipeline", action="store_true", help="Force running synthetic pipeline before starting")
    parser.add_argument("--full", action="store_true", help="Use full 60-day dataset instead of --fast when running pipeline")
    parser.add_argument("--no-web", action="store_true", help="Do not start Next.js web application")
    parser.add_argument("--no-dashboard", action="store_true", help="Do not start Streamlit dashboard")
    parser.add_argument("--port-web", type=int, default=3000, help="Next.js port (default 3000)")
    parser.add_argument("--port-dashboard", type=int, default=8501, help="Streamlit port (default 8501)")
    parser.add_argument("--open", action="store_true", help="Automatically open browser to demo")
    args = parser.parse_args()

    os.chdir(ROOT)

    # 1. Check data and dependencies
    if not args.no_web:
        check_node_modules()
    check_data_artifacts(force_pipeline=args.pipeline, fast_mode=not args.full)

    procs: list[tuple[str, subprocess.Popen]] = []

    def cleanup(signum=None, frame=None):
        print("\n", flush=True)
        log("demo", "Shutting down servers...", "33")
        for name, proc in procs:
            kill_proc_tree(proc)
        log("demo", "All servers stopped. Goodbye!", "32")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    pnpm = shutil.which("pnpm")

    # 2. Start Next.js frontend
    if not args.no_web:
        if not pnpm:
            log("error", "pnpm executable not found on PATH.", "31")
            sys.exit(1)

        web_cmd = [pnpm, "dev", "--port", str(args.port_web)]
        log("web", f"Starting Next.js map on port {args.port_web}...", "36")
        
        # On Windows, shell=True helps resolve .cmd cleanly; start_new_session on Unix allows killing process group
        web_proc = subprocess.Popen(
            web_cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            shell=IS_WINDOWS,
            start_new_session=not IS_WINDOWS,
        )
        procs.append(("web", web_proc))
        threading.Thread(
            target=stream_output,
            args=(web_proc.stdout, "web", "36"),
            daemon=True,
        ).start()

    # 3. Start Streamlit dashboard
    if not args.no_dashboard:
        dash_cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(ROOT / "dashboard" / "app.py"),
            "--server.port",
            str(args.port_dashboard),
            "--server.headless",
            "true",
        ]
        log("dashboard", f"Starting Streamlit dashboard on port {args.port_dashboard}...", "35")
        dash_proc = subprocess.Popen(
            dash_cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            shell=IS_WINDOWS,
            start_new_session=not IS_WINDOWS,
        )
        procs.append(("dashboard", dash_proc))
        threading.Thread(
            target=stream_output,
            args=(dash_proc.stdout, "dashboard", "35"),
            daemon=True,
        ).start()

    # 4. Banner display
    print("\n" + "=" * 68)
    print("  \033[1;32mVayuDrishti Demo Environment is Starting!\033[0m")
    print("=" * 68)
    if not args.no_web:
        print(f"  \033[1;36m>\033[0m Web Application (Map & Scrollytelling): \033[1;4mhttp://localhost:{args.port_web}\033[0m")
    if not args.no_dashboard:
        print(f"  \033[1;35m>\033[0m Research Dashboard (Streamlit):         \033[1;4mhttp://localhost:{args.port_dashboard}\033[0m")
    print("=" * 68)
    print("  Single-terminal mode: press \033[1;33mCtrl+C\033[0m anytime to stop all servers.")
    print("=" * 68 + "\n", flush=True)

    if args.open and not args.no_web:
        time.sleep(2)
        webbrowser.open(f"http://localhost:{args.port_web}")

    # 5. Monitor child processes
    try:
        while True:
            time.sleep(0.5)
            for name, proc in procs:
                if proc.poll() is not None:
                    log("demo", f"Server '{name}' exited with code {proc.returncode}.", "31")
                    cleanup()
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
