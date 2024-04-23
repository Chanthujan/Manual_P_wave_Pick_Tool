# Manual Pick Tool for P-Wave Detection
## Overview
The Manual Pick Tool is specifically designed to support the evaluation of P-wave detection algorithms by enabling precise manual picking of P-wave arrival times, calculation of Peak Ground Acceleration (PGA), and padding of noise data for comprehensive processing. This tool is integral to our research efforts in improving the accuracy and reliability of Earthquake Early Warning Systems (EEWS).

## Features
  1. Picking P-Wave Arrival Time: This step ensures precise identification of P-wave arrival times from the earthquake data, allowing for accurate comparison with algorithm-detected times.
  2. Calculation of PGA for P-waves: This allows the reliable calculation of Peak Ground Acceleration (PGA) values from manually picked P-wave data.
  3. Padding Noise Data for Processing: Including noise data addresses gaps in continuous earthquake data. This is useful for increasing earthquake data length, making processing different P-wave detection algorithms easy.

## Detailed Description 
### Feature 1 - Picking P-Wave Arrival Time
#### a. Waveform Inspection:
&emsp; The tool displays acceleration recordings for each earthquake across three directional axes.

#### b. P-wave Marking:
&emsp; If the P-wave start is clear, the user can select the starting point by zooming in on the waveform's vertical acceleration recording or without zooming. 

#### c. Amplitude Calculation:
&emsp; Once the P-wave start is identified, the tool calculates the initial amplitude by averaging the vertical acceleration values over 1 second starting from the marked P-wave onset.

#### d. Data Logging:
&emsp;  The P-wave arrival time and calculated amplitude are automatically recorded in an Excel sheet

#### Visualisation of the tool's P-wave picking window
<img src="Figures/Figure_1.png" alt="Earthquakes" style="width: 38%;"> <img src="Graphs/Stations.png" alt="Stations" style="width: 42%;">  

### Feature 2 - Calculation of PGA for P-waves


### Feature 3 - Padding Noise Data for Processing
