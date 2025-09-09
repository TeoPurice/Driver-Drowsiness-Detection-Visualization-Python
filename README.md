# Driver Drowsiness Detection Visualization

This Python program evaluates driver alertness using two computed indices:  

- **Eye Quality Index (EQI):** captures visual/biometric indicators of driver fatigue.  
- **Steering Quality Index (SQI):** measures vehicle control and steering consistency.  

A driver is flagged as **safe** if both EQI and SQI are ≤ 0.5; otherwise, a warning is issued.  
Each drive can include multiple data points, and results are visualized on a chart.

---

## Graphs 📊

- The chart displays **EQI (x-axis)** vs **SQI (y-axis)**.  
- The **green shaded box** represents the "safe zone" (≤ 0.5 for both indices).  
- Each data point is plotted:
  - **Green point** = safe  
  - **Red point** = warning  

Multiple drives can be recorded, and each drive generates its own chart.

---

## Algorithm 🔢

### Eye Quality Index (EQI)

The EQI is calculated as a weighted sum of normalized biometric measures:

$$
EQI = c_{1} \cdot (\text{normalized eye closure rate})
    + c_{2} \cdot (\text{normalized blink duration})
    + c_{3} \cdot (1 - \text{normalized saccadic velocity})
$$

Where:  
- $c_{1} = 0.5$ (primary emphasis on eye closure rate)  
- $c_{2} = 0.3$ (secondary emphasis on blink duration)  
- $c_{3} = 0.2$ (penalizes slower saccadic movements)  

### Steering Quality Index (SQI)

The SQI is similarly computed from driving behavior measures:

$$
SQI = d_{1} \cdot (\text{normalized steering variability})
    + d_{2} \cdot (\text{normalized lane deviation})
    + d_{3} \cdot (\text{normalized steering correction time})
$$

Where:  
- $d_{1} = 0.6$ (dominant contribution from steering variability)  
- $d_{2} = 0.3$ (lane deviation as a secondary factor)  
- $d_{3} = 0.1$ (occasional corrections contribute modestly)  

### Why Normalization?

Inputs are normalized to a scale of 0–1 to account for different units and ranges.  
For example:
- Eye closure rate (%) is capped at 50% (≥ 50% treated as 1.0)
- Blink duration (ms) is capped at 500 ms
- Lane deviation (s) is capped at 5 s

This ensures extreme or unrealistic values do not dominate the indices.

---

## Usage ⚙️

Run in editor or use terminal:
```bash
python drowsiness_detection.py
```

### Example Run

**Input:**
```
Start a new drive (y or n): y
Enter eye closure rate (as a percentage): 20
Enter blink duration (in milliseconds): 200
Enter saccadic velocity (degrees/second): 25
Enter steering angle variability (degrees): 5
Enter lane deviation (seconds): 1
Enter steering correction time (seconds): 1
Add another data point to this drive? (y or n): n
Start a new drive (y or n): n
```

**Console Output:**
```
Driver is proceeding safely and alertly. Please continue!
Drive 1 recorded with 1 data points.
All drives recorded:
Drive 1: 1 data points recorded.
```

A chart is displayed with one green point inside the safe zone. See [`demo_runs.txt`](demo_runs.txt) for full sample runs.

