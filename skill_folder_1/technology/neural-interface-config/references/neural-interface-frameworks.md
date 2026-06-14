# Neural Interface Frameworks & Protocols Reference

*Condensed knowledge bank for in-brain compute interface configuration and troubleshooting.*

---

## Major BCI Platforms & SDKs

| Platform | Type | Language | Key APIs | Status |
|----------|------|----------|----------|--------|
| **Neuralink** | Invasive (N1 implant) | Proprietary | Custom telemetry, spike sorting, stimulation | Human trials (PRIME study) |
| **Blackrock Neurotech** | Invasive (Utah Array) | C++, Python | NeuroPort, Cerebus, NEURAL SDK | Commercial/clinical |
| **Synchron** | Endovascular (Stentrode) | Proprietary | Motor intent decoding, click/typing | Human trials (COMMAND) |
| **Paradromics** | Invasive (Connexus) | Proprietary | High-channel count (>1600), speech decoding | Pre-clinical |
| **OpenBCI** | Non-invasive (EEG) | Python, C++, JS | OpenBCI GUI, BrainFlow, LSL | Open source, research |
| **g.tec** | Non-invasive/Invasive | C++, Python, MATLAB | g.HIsys, g.MOBIlab, Simulink blocks | Commercial BCI systems |
| **NeuroPace** | Responsive neurostimulation | Proprietary | RNS System, ECoG sensing + stimulation | FDA approved (epilepsy) |

---

## Communication Protocols

### Lab Streaming Layer (LSL)
- **Purpose**: Real-time streaming of neural/time-series data
- **Transport**: TCP multicast/unicast, local network
- **Python**: `pylsl` — `resolve_stream()`, `StreamInlet`, `StreamOutlet`
- **Key config**: `LSL_LOCAL_ONLY=1` for single-machine, firewall rules for multi-host
- **Marker streams**: Integer/string event codes for trial alignment

### BrainFlow
- **Purpose**: Unified API across 20+ EEG/EMG/ECG boards
- **Boards**: Cyton, Ganglion, Muse, ganglion, OpenBCI, g.tec, etc.
- **Python**: `BoardShim(board_id, params)`, `get_board_data()`
- **Filters**: Built-in bandpass, notch, wavelet denoising
- **ML-ready**: `get_board_data(preset=ML_PRESET)` for feature vectors

### g.Nautilus / g.Nautilus Research
- **BLE 5.0** wireless EEG, 16-32 channels
- **SDK**: C++ DLL + Python bindings (`gtec.nautilus`)
- **Config**: Sampling rate (250/500 Hz), channel map, impedance check
- **Battery**: ~8h continuous, charge via USB-C

---

## Signal Processing Pipeline (Typical)

```
Raw ADC → Impedance Check → Referencing (CAR/bipolar) →
Bandpass (0.5-100 Hz) → Notch (50/60 Hz) →
Artifact Rejection (ICA/ASR) → Feature Extraction →
Decoder/Classifier → Control Signal → Device/Stimulation
```

### Key Libraries
| Task | Python | C++ | Notes |
|------|--------|-----|-------|
| Filtering | `scipy.signal`, `mne.filter` | DSPFilters, KissFFT | Zero-phase (filtfilt) for offline |
| ICA/ASR | `mne.preprocessing.ICA`, `asrpy` | — | ASR better for real-time |
| CSP/Riemannian | `pyriemann`, `mne.decoding.CSP` | — | Motor imagery decoding |
| Deep Learning | `braindecode`, `torch`, `tf` | ONNX Runtime | Export to ONNX for embedded |

---

## Configuration Patterns

### 1. Impedance Verification (Pre-session)
```python
# BrainFlow example
from brainflow import BoardShim, BrainFlowInputParams, BoardIds

params = BrainFlowInputParams()
params.serial_port = "/dev/ttyUSB0"  # Cyton
board = BoardShim(BoardIds.CYTON_BOARD, params)
board.prepare_session()
impedances = board.get_impedance_data()  # per-channel kΩ
board.release_session()

# Target: < 10 kΩ (gel), < 50 kΩ (dry)
assert all(z < 10 for z in impedances), "High impedance channels: " + str([i for i,z in enumerate(impedances) if z >= 10])
```

### 2. LSL Outlet for Real-time Streaming
```python
from pylsl import StreamInfo, StreamOutlet
import numpy as np

info = StreamInfo(
    name="NeuralData", type="EEG",
    channel_count=16, nominal_srate=250,
    channel_format='float32', source_id="openbci_001"
)
# Add channel labels
chans = info.desc().append_child("channels")
for label in ["Fp1","Fp2","F3","F4","C3","C4","P3","P4","O1","O2","F7","F8","T3","T4","T5","T6"]:
    chans.append_child("channel").append_child_value("label", label)

outlet = StreamOutlet(info, chunk_size=16, max_buffered=360)

# In acquisition loop:
outlet.push_sample(sample_array)  # or push_chunk for batches
```

### 3. Stimulation Safety Limits (Clinical)
| Parameter | Conservative Limit | Regulatory Note |
|-----------|-------------------|-----------------|
| Charge density | ≤ 30 µC/cm²/phase | FDA guidance for cortical |
| Charge per phase | ≤ 4 nC (microelectrodes) | Shannon limit |
| Pulse width | 50-450 µs | Symmetric biphasic |
| Frequency | ≤ 200 Hz continuous | Avoid tissue damage |
| Interphase gap | ≥ 100 µs | Charge balancing |

**Always verify** with hardware-specific datasheet — limits vary by electrode material (PtIr, TiN, PEDOT:PSS).

---

## Troubleshooting Checklist

| Symptom | Likely Cause | Verification |
|---------|--------------|--------------|
| No data / flatline | Board not powered, wrong serial port, driver | `dmesg | grep tty`, `ls /dev/tty*`, board LED |
| High 60 Hz noise | Ground loop, unshielded cables, impedance | Check impedance, add notch filter, use battery laptop |
| Packet loss (LSL) | WiFi, buffer overflow, CPU starvation | Wired Ethernet, increase `max_buffered`, `nice -n -10` |
| Stimulation not felt | Amplitude too low, electrode disconnected | Impedance check, verify waveform on scope |
| Decoder drift | Non-stationary signals, electrode migration | Recalibrate daily, adaptive decoder (RLS/Kalman) |
| BLE disconnections | Distance > 10m, interference, low battery | RSSI monitor, keep dongle close, charge headset |

---

## Regulatory / Safety References

- **FDA**: "Guidance for Industry: Implanted Brain-Computer Interface Devices" (2021)
- **IEC 60601-1**: Medical electrical equipment safety
- **ISO 14708-3**: Implants for surgery — neurostimulators
- **IEEE 2731**: Standard for Brain-Computer Interface Data Formats
- **Neurodata Without Borders (NWB:N)**: Neurophysiology data standard

---

## Quick-Start Hardware Matrix

| Use Case | Recommended Hardware | SDK | Approx Cost |
|----------|---------------------|-----|-------------|
| Research EEG (64-ch) | g.Nautilus Research + g.HIsys | Python/C++ | $15-25k |
| Consumer BCI dev | OpenBCI Cyton + Daisy (16-ch) | BrainFlow | $1.5k |
| Motor imagery BCI | OpenBCI + EEG cap + BrainFlow | BrainFlow + pyriemann | $2k |
| ECoG research | Blackrock Cerebus + Utah Array | NEURAL SDK | $100k+ |
| Speech decoding | Paradromics Connexus (pre-clinical) | Proprietary | N/A |
| Closed-loop stimulation | NeuroPace RNS / custom FPGA | Proprietary / Verilog | $50k+ |

---

*Last updated: 2026-06-06. Expand with provider-specific quirks as encountered.*