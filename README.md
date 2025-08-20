🏎️ Formula 1 Qualifying & Race Predictor

This project is a Formula 1 Data Analysis and Prediction System that predicts qualifying results using machine learning and generates visual comparison graphs for qualifying and race performance.
It combines the official F1 dataset (ERGAST + extended 2025 data) with a Random Forest Regressor model to predict qualifying outcomes, while also providing several analysis scripts to visualize race/season progression.

⚙️ Technologies Used:

Python 3.10+
Pandas → Data cleaning & manipulation
Matplotlib → Visualization (qualifying graphs, race progression, season comparisons)
Scikit-learn → 
    RandomForestRegressor (predict qualifying positions)
    LabelEncoder for drivers, constructors, circuits
Joblib → Save/load trained models
Datasets → ERGAST + manually updated 2025 results

📖 Workflow & Files:

  1️⃣ Dataset Preparation (data/):

      races.csv → Metadata of each race (year, round, circuitId).

      results.csv → Final race results (positions, points, status).

      qualifying.csv → Session times (Q1, Q2, Q3).

      drivers.csv → Driver details.

      constructors.csv → Constructor details.

      circuits.csv → Circuit details.

    ✅ Extended to include 2025 results up to Spa, plus new drivers (Antonelli, Bortoleto, Hadjar).

  2️⃣ Machine Learning Model (model/):

    Model Used:
        RandomForestRegressor → chosen for its robustness in handling categorical encodings and capturing non-linear relationships.
        Target: Predicted qualifying position.
        Features:
            Encoded Driver
            Encoded Constructor
            Encoded Circuit
            Year

    Encoders
        driver_encoder.pkl → Maps driver names → numerical values.
        constructor_encoder.pkl → Maps constructors → numerical values.
        circuit_encoder.pkl → Maps circuit IDs → numerical values.
    Outputs:
        qualifying_model.pkl → trained regressor.
        valid_pairs.csv → all valid driver/constructor pairs for predictions.

  3️⃣ Prediction Script:
      predict_qualifying.py

      Loads trained model & encoders.
      Takes circuit ID + year as input.
      Predicts positions for all drivers in the grid (valid_pairs.csv).
      Allows user to select output size:
        -> Top 5
        -> Top 10
        -> All drivers

NOTE: Example usages should be run in terminal!
Example Usage of predict_qualifying.py:

  Terminal: 
    python predict_qualifying.py   
    Enter circuit ID (e.g., 14 for Spa): 21
    Enter season year (e.g., 2025): 2025
    How many to show? (5 / 10 / all): 10

  Output:
    📍 Predicted Qualifying for Circuit ID 21  — Year 2025
    1. Verstappen (Red Bull) — Position: 1.67
    2. Norris (McLaren) — Position: 2.79
    3. Piastri (McLaren) — Position: 3.12
    AND SO ON ---
    
4️⃣ Graphing Scripts:

  1) GraphCompare.py
      Input: Circuit + Year + Drivers
      Plots Q1 → Q2 → Q3 progression graph
      Annotates each lap time + final Q3 position

  2) RaceGraph.py
      Input: Circuit + Year + Drivers
      Compares grid start → finish positions

  3) manyracesgraph.py
      Input: Circuit + Multiple Years + Drivers
      Compares same circuit over multiple seasons

  4) QualiCompare.py
      Input: Circuit + Multiple Years + Drivers
      Compares final qualifying times across years

  5) SeasonCompare.py
      Input: Year + Drivers
      Shows race result progression across full season
      Annotates DNF, DNS, DSQ where applicable
      Adds secondary legend for total points

  6) SeasonPointsCompare.py
      Input: Year + Drivers
      Plots points progression per race across the season

🚀 How to Run:

    Clone the repo:
    
        git clone https://github.com/ApurrvSemwal16/F1-Qualifying-Predictor-and-Stat-Graphs.git
        cd F1-Qualifying-Predictor-and-Stat-Graphs

    Install dependencies:
    
        pip install -r requirements.txt
        
    Run a script of your choice.

📊 Example Insights:

  1) Which drivers improve across Q1 → Q2 → Q3.
  2) Historical performance at circuits across different years.
  3) Season-long battle between drivers, including DNFs & DNS.
  4) Points progression to visualize title fights.

✨ Credits:
  Dataset: Ergast F1 Dataset
  (Can/Should be extended to 2025 manually by user, currently dataset is up-to-date till 2024 ABU DHABI GP)
  ML Model:
    RandomForestRegressor (Scikit-learn)
    Visualization: Matplotlib
    ChatGPT (comments on files & error management)

NOTE: If any error is found or any bug is found in the codes, kindly update them to my email given below, any help in fixing and making this better will be highly appreciated and credited.

Thank You
Apurrv Semwal
2024365054.apurrv@ug.sharda.ac.in
Sharda University (CS-A)


