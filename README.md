# Taylor-Swift-Quiz

## Overview
With the popularity of music increasing, everybody is invested in building their personal taste now more than ever. This Taylor Swift Personality-Based Song Recommender brings you just that.

To the Swifties and the curious listeners—whether you're a dedicated, active member of *The Tortured Poets Department* or a *Midnights* enthusiast—this tool will help you discover which song among Taylor's discography suits you the best! 



## Project Goals
The main aim of this project is to bring users an interactive quiz with personality- and music-based questions. The frontend collects the responses from users and sends them to a FastAPI backend, which processes the inputs and uses a machine learning model to determine the best-matching song. The result is then dynamically displayed on the webpage.



## Data Source
The dataset was retrieved from an open-source website, Kaggle.com. It contains data on Taylor Swift's songs from the year 2008 to the latest remastered releases of 2024. The dataset consists of 31 attributes and 284,808 rows.

**Dataset:** [Kaggle](https://www.kaggle.com/datasets/jarredpriester/taylor-swift-spotify-dataset)



## Tech Stack
**Frontend:** HTML, CSS, JavaScript  
**Backend:** Python, FastAPI  
**ML Model:** K-Nearest Neighbors (KNN)  
**Hosting:** Localhost



## How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/yashvi-raghuvanshi/Taylor-Swift-Quiz
cd Taylor-Swift-Quiz
```
### 2. Set Up Environment
  - Create a virtual enviroment:
    For macOS/Linux:
    ``` bash
    python3 -m venv venv
    source venv/bin/activate
    ```
  - For Windows:
    ``` powershell
    python -m venv venv
    venv\Scripts\activate
    ```
 ### 3. Install Required Packages
 ``` bash
 pip install -r requirements.txt
 ```

 ### 4. Start the Backend Server
 ``` bash
 uvicorn main:app --reload
 ```

