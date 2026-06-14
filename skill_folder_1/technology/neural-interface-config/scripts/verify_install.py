#!/usr/bin/env python3
"""
Verification probe for neural-interface-config skill.
Run: python scripts/verify_install.py
Checks: BrainFlow, pylsl, numpy imports + synthetic board streaming test.
"""

import sys
import subprocess
import importlib.util


def check_import(module: str, package: str = None) -> bool:
    """Check if a Python module can be imported."""
    pkg = package or module
    try:
        spec = importlib.util.find_spec(module)
        if spec is None:
            print(f"  ✗ {pkg}: NOT INSTALLED")
            return False
        __import__(module)
        print(f"  ✓ {pkg}: OK")
        return True
    except ImportError as e:
        print(f"  ✗ {pkg}: IMPORT ERROR — {e}")
        return False


def check_cli(tool: str, version_flag: str = "--version") -> bool:
    """Check if a CLI tool is available."""
    try:
        result = subprocess.run([tool, version_flag], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            ver = result.stdout.strip().split('\n')[0]
            print(f"  ✓ {tool}: {ver}")
            return True
        else:
            print(f"  ✗ {tool}: NOT FOUND (exit {result.returncode})")
            return False
    except FileNotFoundError:
        print(f"  ✗ {tool}: NOT INSTALLED")
        return False
    except subprocess.TimeoutExpired:
        print(f"  ✗ {tool}: TIMEOUT")
        return False


def test_synthetic_board_stream() -> bool:
    """Test streaming with BrainFlow synthetic board (no hardware needed)."""
    try:
        from brainflow import BoardIds, BoardShim, BrainFlowInputParams
        from pylsl import StreamInfo, StreamOutlet, resolve_stream, StreamInlet, local_clock
        import numpy as np
        import time

        print("\n[+] Testing synthetic board → LSL round-trip...")

        # Setup synthetic board
        params = BrainFlowInputParams()
        board = BoardShim(BoardIds.SYNTHETIC_BOARD, params)
        board.prepare_session()
        board.start_stream(45000)

        srate = BoardShim.get_sampling_rate(BoardIds.SYNTHETIC_BOARD)
        eeg_chans = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD)
        n_chans = len(eeg_chans)

        # Create LSL outlet
        info = StreamInfo("TestEEG", "EEG", n_chans, srate, "float32", "verify_test")
        outlet = StreamOutlet(info, chunk_size=32, max_buffered=360)

        # Create LSL inlet
        streams = resolve_stream("type", "EEG", timeout=2.0)
        if not streams:
            print("  ✗ No LSL EEG stream found")
            board.stop_stream()
            board.release_session()
            return False
        inlet = StreamInlet(streams[0], max_buflen=360)

        # Push and pull a few samples
        sent = 0
        received = 0
        t_start = time.time()
        while time.time() - t_start < 2.0:
            data = board.get_board_data()
            if data.size > 0:
                eeg_data = data[eeg_chans, :].T
                for sample in eeg_data:
                    outlet.push_sample(sample.astype(np.float32).tolist())
                    sent += 1

            chunk, _ = inlet.pull_chunk(timeout=0.1, max_samples=128)
            if chunk:
                received += len(chunk)

            time.sleep(0.01)

        board.stop_stream()
        board.release_session()

        if sent > 0 and received > 0:
            print(f"  ✓ Round-trip OK: sent {sent}, received {received} samples")
            return True
        else:
            print(f"  ✗ Round-trip FAILED: sent {sent}, received {received}")
            return False

    except Exception as e:
        print(f"  ✗ Synthetic test ERROR: {e}")
        return False


def main():
    print("=== neural-interface-config Verification ===\n")

    checks = []

    print("Python packages:")
    checks.append(check_import("brainflow", "brainflow"))
    checks.append(check_import("pylsl", "pylsl"))
    checks.append(check_import("numpy", "numpy"))
    checks.append(check_import("scipy", "scipy"))
    checks.append(check_import("mne", "mne (optional)"))
    checks.append(check_import("pyriemann", "pyriemann (optional)"))

    print("\nSystem tools:")
    checks.append(check_cli("lsusb"))  # for USB device enumeration

    print("\nSynthetic board round-trip test:")
    checks.append(test_synthetic_board_stream())

    print("\n=== Summary ===")
    passed = sum(checks)
    total = len(checks)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✓ ALL CHECKS PASSED — skill environment ready")
        return 0
    else:
        print("✗ SOME CHECKS FAILED — install missing dependencies")
        print("  pip install brainflow pylsl numpy scipy mne pyriemann")
        return 1


if __name__ == "__main__":
    sys.exit(main())