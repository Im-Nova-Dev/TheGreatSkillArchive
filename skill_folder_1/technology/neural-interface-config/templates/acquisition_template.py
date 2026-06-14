#!/usr/bin/env python3
"""
OpenBCI / BrainFlow Real-time Acquisition Template
For use with neural-interface-config skill.
Run: python templates/acquisition_template.py --board cyton --port /dev/ttyUSB0 --stream-name MyEEG
"""

import argparse
import signal
import sys
import time
from typing import Optional

import numpy as np

try:
    from brainflow import (
        BoardIds, BoardShim, BrainFlowInputParams, BrainFlowError, LogLevels
    )
    from pylsl import StreamInfo, StreamOutlet, local_clock
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install: pip install brainflow pylsl numpy")
    sys.exit(1)


# ─── Signal handling for clean shutdown ───
_shutdown = False


def _signal_handler(signum, frame):
    global _shutdown
    print("\n[+] Shutdown signal received")
    _shutdown = True


signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)


# ─── Board configuration map ───
BOARD_MAP = {
    "cyton": BoardIds.CYTON_BOARD,
    "cyton_daisy": BoardIds.CYTON_DAISY_BOARD,
    "ganglion": BoardIds.GANGLION_BOARD,
    "ganglion_wifi": BoardIds.GANGLION_WIFI_BOARD,
    "synthetic": BoardIds.SYNTHETIC_BOARD,  # for testing without hardware
}


# ─── LSL Stream Setup ───
def create_lsl_outlet(stream_name: str, board_id: BoardIds, srate: int, n_chans: int) -> StreamOutlet:
    info = StreamInfo(
        name=stream_name,
        type="EEG",
        channel_count=n_chans,
        nominal_srate=srate,
        channel_format="float32",
        source_id=f"brainflow_{board_id.name.lower()}_{int(time.time())}"
    )
    # Channel metadata (10-20 standard for common configs)
    if n_chans == 8:
        labels = ["Fp1", "Fp2", "C3", "C4", "P7", "P8", "O1", "O2"]
    elif n_chans == 16:
        labels = ["Fp1", "Fp2", "F7", "F8", "F3", "F4", "T3", "T4",
                  "C3", "C4", "P3", "P4", "O1", "O2", "Fz", "Cz"]
    else:
        labels = [f"CH{i+1}" for i in range(n_chans)]

    chans = info.desc().append_child("channels")
    for lbl in labels:
        ch = chans.append_child("channel")
        ch.append_child_value("label", lbl)
        ch.append_child_value("unit", "microvolts")
        ch.append_child_value("type", "EEG")

    # Marker channel for events
    markers = info.desc().append_child("channels")
    mk = markers.append_child("channel")
    mk.append_child_value("label", "Markers")
    mk.append_child_value("unit", "int")
    mk.append_child_value("type", "Marker")

    return StreamOutlet(info, chunk_size=32, max_buffered=3600)


# ─── Main Acquisition Loop ───
def run_acquisition(
    board_id: BoardIds,
    port: str,
    stream_name: str,
    log_level: LogLevels = LogLevels.LEVEL_INFO,
    daisy: bool = False,
) -> int:
    params = BrainFlowInputParams()
    params.serial_port = port
    params.timeout = 15  # seconds

    board = BoardShim(board_id, params)
    BoardShim.enable_dev_board_logger()
    BoardShim.set_log_level(log_level)

    try:
        board.prepare_session()
        print(f"[+] Board prepared: {BoardIds(board_id).name}")
    except BrainFlowError as e:
        print(f"[!] prepare_session failed: {e}")
        return 1

    # Get board specs
    srate = BoardShim.get_sampling_rate(board_id)
    n_chans = len(BoardShim.get_eeg_channels(board_id))
    print(f"[+] Sampling rate: {srate} Hz, EEG channels: {n_chans}")

    # Impedance check (only for boards that support it)
    if board_id in (BoardIds.CYTON_BOARD, BoardIds.CYTON_DAISY_BOARD, BoardIds.GANGLION_BOARD):
        try:
            imp = board.get_impedance_data()
            print(f"[+] Impedances (kΩ): {imp}")
            high = [i for i, z in enumerate(imp) if z > 50]
            if high:
                print(f"[!] High impedance on channels: {high}")
        except BrainFlowError:
            print("[-] Impedance check not available for this board")

    outlet = create_lsl_outlet(stream_name, board_id, srate, n_chans)
    print(f"[+] LSL outlet created: '{stream_name}' — connect with LabRecorder or pylsl")

    board.start_stream(45000)  # ring buffer size
    print("[+] Streaming... Press Ctrl+C to stop")

    eeg_channels = BoardShim.get_eeg_channels(board_id)
    marker_channel = BoardShim.get_marker_channel(board_id)

    sent_samples = 0
    last_report = time.time()

    try:
        while not _shutdown:
            data = board.get_board_data()  # non-blocking, clears buffer
            if data.size == 0:
                time.sleep(0.005)  # 5 ms
                continue

            # data shape: (n_channels, n_samples)
            # Only push EEG channels + marker
            eeg_data = data[eeg_channels, :].T  # (n_samples, n_chans)
            markers = data[marker_channel, :] if marker_channel < data.shape[0] else np.zeros(eeg_data.shape[0])

            for i in range(eeg_data.shape[0]):
                sample = eeg_data[i].astype(np.float32)
                # Append marker as last channel (or push separate marker stream)
                outlet.push_sample(np.append(sample, markers[i]).tolist(), timestamp=local_clock())
                sent_samples += 1

            now = time.time()
            if now - last_report > 5:
                rate = sent_samples / (now - last_report)
                print(f"  ... {sent_samples} samples sent ({rate:.0f} Hz)")
                sent_samples = 0
                last_report = now

    except KeyboardInterrupt:
        pass
    finally:
        board.stop_stream()
        board.release_session()
        print("[+] Session released cleanly")

    return 0


# ─── CLI ───
def main():
    parser = argparse.ArgumentParser(description="OpenBCI/BrainFlow → LSL acquisition")
    parser.add_argument("--board", choices=list(BOARD_MAP.keys()), default="cyton",
                        help="Board type (default: cyton)")
    parser.add_argument("--port", default="/dev/ttyUSB0",
                        help="Serial port (default: /dev/ttyUSB0)")
    parser.add_argument("--stream-name", default="OpenBCI_EEG",
                        help="LSL stream name (default: OpenBCI_EEG)")
    parser.add_argument("--daisy", action="store_true",
                        help="Use Cyton+Daisy (16-ch) mode")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug logging")
    args = parser.parse_args()

    board_id = BOARD_MAP[args.board]
    if args.daisy and board_id == BoardIds.CYTON_BOARD:
        board_id = BoardIds.CYTON_DAISY_BOARD

    log_level = LogLevels.LEVEL_DEBUG if args.debug else LogLevels.LEVEL_INFO
    return run_acquisition(board_id, args.port, args.stream_name, log_level, args.daisy)


if __name__ == "__main__":
    sys.exit(main())