# 406 MHz Cospas-Sarsat Phase-Coherent Direction Finding (KrakenSDR)

This project implements a custom 5-channel, phase-coherent Radio Direction Finding (RDF) network in GNU Radio. It is specifically engineered to track 406 MHz Cospas-Sarsat distress beacons using a KrakenSDR. 

Unlike continuous-wave (CW) signals, Cospas-Sarsat beacons transmit an intermittent digital burst (a 5-Watt, 440-millisecond pulse once every 50 seconds). Standard continuous direction-finding flowgraphs fail on intermittent bursts. This architecture solves that challenge by using an Adaptive CFAR Squelch to cleanly gate the burst, feeding synchronized spatial arrays into the MUSIC algorithm, and using a custom Smart Vector Gate to hold the bearing on screen between bursts.

## Project Architecture

This project is divided into three main components: a master flowgraph and two custom hierarchical blocks.

### 1. The KrakenSDR Simulator (`cospas_sarsat_doa.grc`)
*Hierarchical Block* \
Because testing intermittent 5W bursts in the real world is difficult, this block mathematically simulates the hardware. 
* It generates a baseband 406 MHz Cospas-Sarsat BPSK payload.
* It splits the signal into 5 parallel paths and injects realistic AWGN (Additive White Gaussian Noise).
* It mathematically shifts the phase of each channel based on a Uniform Circular Array (UCA) geometry (r = 0.22 meters). 
* The user can dynamically change the simulated Angle of Arrival using a UI slider.

### 2. The Adaptive Burst Squelch (`squelcher.grc`)
*Hierarchical Block* \
Standard absolute-threshold squelches suffer from "self-gating" or chatter on massive 5W bursts. This block is a **Temporally Offset CFAR (Constant False Alarm Rate)** squelch.
* **Path A** takes the live RF. 
* **Path B** delays the signal by 2 seconds, runs it through an IIR filter, and multiplies it by a margin to calculate the past noise floor. 
* **Path C** divides the live signal by the delayed noise floor, outputting a highly stable binary gate (0.0 or 1.0) exactly when the burst hits.

### 3. The Master Flowgraph (`kraken_music_doa.grc`)
This is the main controller flowgraph that ties the system together.
* **Decimation:** Drops the 2.4 MHz sample rate down by a factor of 128 to 18.75 kHz using a brick-wall low-pass filter to prevent noise aliasing.
* **MUSIC DOA Algorithm:** Groups exactly 8,192 decimated samples (matching the 437ms burst length) and processes the spatial covariance matrix to output a 360-degree bearing spectrum.
* **Smart Vector Gate (Python Block):** A custom Embedded Python block that synchronizes the high-speed Squelch stream with the low-speed MUSIC vector frames. It drops mathematical `NaN` explosions, ignores flatlined DC-offset frames, and "holds" the last valid burst peak on the UI between the 50-second silences.

---

## How to Run Locally (Deployment Guide)

To migrate and run this project on a new Ubuntu/Linux system, you must compile the KrakenSDR modules and generate the Hierarchical blocks locally.

### Step 1: Install the KrakenSDR OOT Modules
The DOA MUSIC block and the KrakenSDR source block are not native to GNU Radio. You must install the `gr-krakensdr` Out-Of-Tree (OOT) module.

   ```bash
   git clone https://github.com/krakenrf/krakensdr_doa.git
   cd gr-krakensdr
   mkdir build && cd build
   cmake ..
   make
   sudo make install
   ```

### Step 2: Generate the Hierarchical Blocks
GNU Radio cannot run the master flowgraph until the simulator and squelcher blocks are compiled into Python.

1. Open `squelcher.grc` in GNU Radio Companion (GRC).
2. Click the **Generate** button (the flowchart icon next to Play). Do *not* click Play.
3. Open `cospas_sarsat_doa.grc` in GRC and click **Generate**.
4. Restart GNU Radio Companion.

**Troubleshooting Missing Blocks:**
If you restart GRC and the master flowgraph still complains that `squelcher` or `cospas_sarsat_doa` are missing, GRC failed to link the generated blocks. You must manually move them to your user's GRC directory:
```bash
# Create the hidden GRC folder if it doesn't exist
mkdir -p /home/$USER/.grc_gnuradio

# Assuming you are in the folder with your generated files:
cp squelcher.py /home/$USER/.grc_gnuradio/
cp squelcher.grc.yml /home/$USER/.grc_gnuradio/
cp cospas_sarsat_doa.py /home/$USER/.grc_gnuradio/
cp cospas_sarsat_doa.grc.yml /home/$USER/.grc_gnuradio/
```
*Restart GRC one more time, and the blocks will appear.*

### Step 3: Run the Master Flowgraph
1. Open `kraken_music_doa.grc`. 
2. Click **Play**.
3. Adjust the Angle of Incidence slider to verify the MUSIC algorithm correctly tracks the simulated burst.

## Using With Physical Hardware
This flowgraph currently contains a **Throttle block** to prevent your CPU from maxing out at 100% while running the mathematical simulator. Due to lack of availability of KrakenSDR hardware, the `cospas_sarsat_doa` simulator is used.

When you remove the `cospas_sarsat_doa` simulator block and plug in the physical **KrakenSDR Source** block, **you MUST delete or bypass the Throttle block.** Physical SDR hardware acts as its own metronome. Leaving a software throttle in the chain with real hardware will cause massive buffer underruns and destroy the phase-coherency of the array.

Additionally, ensure you run the Heimdall DAQ noise-source calibration before running the flowgraph to account for phase delays in your physical coaxial cables.
