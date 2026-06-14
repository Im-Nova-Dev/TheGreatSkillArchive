---
name: neural-interface-config
description: "Configure and troubleshoot in-brain compute interfaces for humans and agents."
version: 0.2.0
category: technology
---

# Neural Interface Config

## Overview

Configure and troubleshoot in-brain compute interfaces (BCI) for humans and agents — from non-invasive EEG (OpenBCI, g.tec) to invasive microelectrode arrays (Blackrock, Neuralink) and endovascular systems (Synchron). Covers hardware setup, real-time streaming (LSL, BrainFlow), signal processing pipelines, stimulation safety limits, and regulatory references.

## When To Use

- Setting up a new BCI acquisition rig (EEG, ECoG, Utah Array, Stentrode)
- Configuring real-time neural data streaming via Lab Streaming Layer (LSL)
- Implementing signal processing: filtering, artifact rejection, feature extraction, decoding
- Defining stimulation parameters within clinical safety limits
- Troubleshooting common BCI issues: noise, packet loss, impedance, decoder drift
- Validating software environment for neural interface development

## Prerequisites

- Python 3.9+ with `brainflow`, `pylsl`, `numpy`, `scipy`
- For EEG: OpenBCI Cyton/Ganglion, g.Nautilus, or compatible hardware
- For invasive: Blackrock Cerebus/NeuroPort, Neuralink SDK (requires NDA), Synchron API
- LSL-compatible recording software (LabRecorder, OpenViBE, custom)
- Wired Ethernet recommended for multi-machine LSL streaming
- Regulatory clearance (IRB/IDE) for human subjects research

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Impedance** | Electrode-skin/electrode-tissue resistance (kΩ). Target: <10 kΩ (gel EEG), <50 kΩ (dry), <5 kΩ (ECoG). |
| **Referencing** | Common Average Reference (CAR), bipolar, or linked ears. Affects spatial filtering and noise rejection. |
| **LSL** | Lab Streaming Layer — de-facto standard for real-time neural/time-series streaming over TCP. |
| **BrainFlow** | Unified Python/C++ API across 20+ biosignal boards. Handles board comms, filtering, ML features. |
| **Charge-balanced stimulation** | Biphasic pulses with interphase gap; net zero charge to prevent tissue damage/electrode corrosion. |
| **Decoder drift** | Non-stationarity in neural signals causing classifier degradation. Mitigated by adaptive decoders (RLS, Kalman). |

## Workflow

### 1. Hardware Bring-up
```bash
# Identify serial port (Linux)
ls /dev/ttyUSB* /dev/ttyACM*
dmesg -T | grep -i usb

# Verify board communication (BrainFlow)
python -c "
from brainflow import BoardShim, BrainFlowInputParams, BoardIds
params = BrainFlowInputParams(); params.serial_port = '/dev/ttyUSB0'
b = BoardShim(BoardIds.CYTON_BOARD, params)
b.prepare_session()
print('Impedances:', b.get_impedance_data())
b.release_session()
"
```

### 2. Real-time Streaming (LSL)
Use `templates/acquisition_template.py`:
```bash
python templates/acquisition_template.py --board cyton --port /dev/ttyUSB0 --stream-name MyEEG
```
- Connect with LabRecorder or `pylsl.StreamInlet(resolve_stream('type','EEG')[0])`
- For multi-machine: ensure firewalls allow TCP 22345 (LSL default), set `LSL_LOCAL_ONLY=0`

### 3. Signal Processing Pipeline
Reference: `references/neural-interface-frameworks.md` (libraries table)
```python
# Typical offline pipeline (MNE-Python)
import mne
raw = mne.io.read_raw_fif('session.fif', preload=True)
raw.filter(1, 100, fir_design='firwin').notch_filter([50, 100])
raw.set_eeg_reference('average')  # CAR
ica = mne.preprocessing.ICA(n_components=16, random_state=42)
ica.fit(raw)
ica.exclude = [0, 1]  # manually identified artifact components
raw_clean = ica.apply(raw.copy())
```

### 4. Stimulation Safety Configuration
```python
# Verify parameters against limits in references/neural-interface-frameworks.md
charge_density = amplitude_uA * pulse_width_us / electrode_area_cm2  # µC/cm²
assert charge_density <= 30, "Exceeds FDA cortical limit"
assert pulse_width_us <= 450, "Exceeds safe pulse width"
assert frequency_hz <= 200, "Exceeds continuous stimulation limit"
```

### 5. Verification
Run the install/environment probe:
```bash
python scripts/verify_install.py
```
Expected: All imports OK, synthetic board round-trip passes.

## Example Usage

```bash
# 1. Quick hardware check (Cyton)
python templates/acquisition_template.py --board cyton --port /dev/ttyUSB0 --stream-name TestCyton

# 2. Record with LabRecorder (GUI) or headless:
python -c "
from pylsl import resolve_stream, StreamInlet
import numpy as np
inlet = StreamInlet(resolve_stream('type','EEG')[0])
data = []
for _ in range(2500):  # 10 seconds @ 250 Hz
    chunk, _ = inlet.pull_chunk(timeout=1.0, max_samples=256)
    if chunk: data.extend(chunk)
np.save('eeg_10s.npy', np.array(data))
print(f'Recorded {len(data)} samples')
"

# 3. Run verification
python scripts/verify_install.py
```

## Support Files

| File | Purpose |
|------|---------|
| `references/neural-interface-frameworks.md` | Hardware platforms, protocols, signal processing libraries, safety limits, troubleshooting table, hardware matrix |
| `templates/acquisition_template.py` | Production-ready OpenBCI/BrainFlow → LSL acquisition script with CLI, impedance check, clean shutdown |
| `scripts/verify_install.py` | Environment verification probe: imports + synthetic board LSL round-trip test |

## Pitfalls & Edge Cases

| Issue | Symptom | Resolution |
|-------|---------|------------|
| **LSL multicast not crossing subnets** | Inlet can't resolve outlet stream | Use unicast: `LSL_LOCAL_ONLY=0` + explicit IP in `StreamInfo`, or run LSL relay |
| **Cyton Daisy channel ordering** | Channels 9-16 appear before 1-8 | BrainFlow returns Daisy-interleaved; use `BoardShim.get_eeg_channels()` for correct indices |
| **g.Nautilus BLE drops** | Intermittent data loss >2m | Keep USB dongle on same side of body; use USB extension; monitor RSSI |
| **Blackrock NEURAL SDK license** | `ImportError: libneural.so` | Source `setup_env.sh` from SDK install; `LD_LIBRARY_PATH` must include SDK lib |
| **Decoder drift overnight** | Classification accuracy drops >15% | Retrain daily; use adaptive CSP (RA-CSP) or Riemannian classifier with exponential forgetting |
| **Stimulation artifact saturation** | Amplifier rails during pulse | Enable blanking (hardware) or sample-and-hold (software); increase interphase gap |

## Verification Steps

1. **Environment**: `python scripts/verify_install.py` → all green
2. **Hardware**: Impedance check → all channels < target kΩ
3. **Streaming**: `templates/acquisition_template.py` runs 30s without buffer overrun
4. **Recording**: LabRecorder saves `.xdf` with matching sample count
5. **Round-trip**: Synthetic test in verify script receives >90% of sent samples

## Related Skills

- `technology/bci-decoder-training` — motor imagery / P300 / SSVEP decoder training
- `technology/neurofeedback-loop` — closed-loop neuromodulation
- `technology/eeg-artifact-rejection` — ICA, ASR, wavelet denoising deep dive
- `technology/implant-telemetry` — wireless power/data for implanted systems
- `technology/agent-tool-auditor` — audit tool usage in BCI software stacks

## Reference Notes

- Expanded from auto-generated stub on 2026-06-06
- References based on FDA guidance (2021), IEEE 2731, NWB:N standards
- Hardware matrix reflects 2024-2025 market; update as new systems launch
- All code templates tested with BrainFlow 5.15+, pylsl 1.16+, Python 3.11