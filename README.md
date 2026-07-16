This repository contains the code to execute the replication from the paper "Unadmitted Technical Debt: Dataset and Detection Approaches" for the course "Reproductibility In Computer Science Research"

Paper Description: 
    - Authors: Dongjin Yu , Senior Member, IEEE, Yihang Xu , Xin Chen , Quanxin Yang , and Sixuan Wang
    - Published at: IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 51, NO. 12.
    - Published on DECEMBER 2025


Requirements:
    - To execute this replciation experiment, you need access to a LLM inference API.


Recommended: Create a python venv.
    -$ python -m venv venv
    -$ source venv/bin/activate
    -$ pip install -r requirements.txt


Repository description:
    root/experiment_pipeline: Contains the python scripts to execute the replication experiment. 
    root/generate_visualizations: Contains the python scripts to create the latex table presented in the paper. There is also a script to create a Confidence Interval chart.

How to configure the experiment:
    - Modify the file "root/experiment_pipeline/config.py" with your preferences and your experiment and API requirements.
    - Modify the file "root/generate_visualizations/config.py" with your preferences to generate the latex table.


How to execute the experiment:
    - Once configured, you can go to the folder root/experiment_pipeline and run the script main.py
        Commands:
            $cd experiment_pipeline
            $python main.py


How to generate the latex table:
    - Once configured (generate_visualizations/config.py). you can go to the folder root/generate_visualizations/ and run the script "generate_latex_table.py" or "generate_all_visualizations.py". The latex table will be generated in root/generate_visualizations/latex_results.txt

Notes:
    - To the inferences run asyncronously. On config.py you can set the max number of concurrent requests sent to your API.   


# Link: https://ieeexplore.ieee.org/document/11208161

