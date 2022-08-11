# HW - FastAPI

## How to run
* **Step 1: Install Python Packages**
    * > pip install -r requirements.txt
* **Step 2: Run by uvicorn (Localhost)**
    * > uvicorn main:app --reload
    * Default host = 127.0.0.1, port = 8000
* **Step 3: Test API using Swagger UI**
    * http://127.0.0.1:8000/docs

## GET methods
* >/list-my-weapon
    * List out all weapon's info.
* >/get-weapon-dps
    * Get specific weapon's DPS.
* >/best-damage-caculate/{int}
    * Calcualte the best damage you can cause.

## POST methods
* >/add-weapon
    * Add a weapon to your weapon list.
    * Request body:
    ```
    {
        "name": string,
        "description": string,
        "ATK": int,
        "CD": float
    }
    ```
* >/get-best-weapon
    * Find out your best weapon.
* >/upload-file
    * Upload file


