# RAPD_Autoscorer
Semi-automatic RAPD gel analysis software featuring image preprocessing, DNA fragment size estimation, binary band scoring, and export for genetic diversity studies.
# RAPD Auto Scorer

A semi-automatic RAPD gel analysis software developed in Python.

## Features

✔ Image preprocessing
✔ Manual lane assignment
✔ Ladder calibration
✔ Automatic BP estimation
✔ Binary matrix generation
✔ Excel export
✔ CSV export

## Image Preprocessing (Under Developped) 

- Crop
- Rotate (0.1° precision)
- Grayscale
- 8-bit conversion
- Invert
- Brightness
- Contrast
- Histogram Equalization
- CLAHE
- Background subtraction
- Gaussian Blur
- Median Filter
- Bilateral Filter
- Sharpen
- Undo / Redo

## Analysis Workflow

Image

↓

Preprocessing

↓

Lane Detection

↓

Ladder Detection

↓

BP Estimation

↓

Binary Matrix

↓

Export

## Platform

Ubuntu 24.04 LTS

Python 3.12

Matplotlib

Scipy

Pillow

OpenCV

NumPy

Pandas

OpenPyXL

##Installation (Debian Based Linux OS ,ex. Ubuntu )
### 1. Clone the repository 
```bash
git clone https://github.com/r2croy/RAPD_Autoscorer

```
### 2. Enter the project

```bash
cd RAPD_Autoscorer
```
### 3. (Optional but recomendend) Create a virtual Environment 

```bash
python3 -m venv venv
```
Acitvate it : 

```bash
source venve/bin/activate
```

### 4. Install required pakeges 

```bash
 pip3 install -r requirements.txt
```
### 5. Run the program

```bash
python3 main.py
```

## Author

Ridoy Roy

Department of Genetic Engineering and Biotechnology

Shahjalal University of Science and Technology,Sylhet

Bangladesh
