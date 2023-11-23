# Milvus-Database-Local-Deploy
Sementic Search using Milvus local deployment using docker and hugging face embeddings 


## Prerequisite
1. Docker
2. Python

## Set-up
1. Clone repo
2. Create Environmet
    ```
    python -m venv venv
    ```
3. Activate environment (powershell)
    ```
    venv/scripts/activate
    ```
4. Download libraries
    ```
    pip install -r requirements.txt
    ```
5. Run milvus local server
    ```
    cd milvus
    docker compose up
    ```
6. Add context (context.docx) to data folder
7. Create collection and insert data
    ```
    cd ..
    py pre.py
    py setup.py
    ```


## How to use
1. Run flask server
    ```
    py app.py
    ```
2. Go to localhost:6969

## Further improvements
1. Dockerise flask server
2. Accept multiple context files