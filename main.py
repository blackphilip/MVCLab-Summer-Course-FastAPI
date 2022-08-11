from distutils.command.upload import upload
import os
import json
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse
from typing import  Union
from pydantic import BaseModel
from uuid import uuid4

class Weapon(BaseModel):
    name: str
    description: Union[str, None] = None
    ATK: int
    CD: float

class WeaponNotFound(Exception):
    def __init__(self, name: str):
        self.name = name

class FileUploadFail(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

weapons = []
weapon_file = 'weapons.json'
upload_file_names = []


if os.path.exists(weapon_file):
    with open(weapon_file, "r") as f:
        weapons = json.load(f)

@app.get('/')
def root():
    return {"Message": "Hello Welcome to Weapon Shop ! What can I help you?"}

@app.get('/list-my-weapon')
def list_my_weapon():
    return {'My weapons': weapons}

@app.get('/get-weapon-dps')
def get_weapon_dps(weapon_name: str=None):
    if not weapon_name:
        raise HTTPException(406, "Seems like you're not intrested in getting your weapon info.")
    else:
        for d in weapons:
            if d['name'] == weapon_name:
                return {f"Message": f"Weapon {weapon_name}'s DPS is {d['DPS']}."}

        raise WeaponNotFound(name=weapon_name)

@app.get('/best-damage-calculate/{int}')
def damage_calculate(time: int=10):
    if weapons:
        weapon_max_dps = 0
        for w in weapons:
            if float(w['DPS']) >= weapon_max_dps:
                weapon_max_dps = float(w['DPS'])

        max_damage = format(weapon_max_dps * time, '.2f')

        return {'Message': f"Your best damage in time {time} secs is {max_damage}."}
    else:
        raise HTTPException(410, "No weapon exist.")


@app.exception_handler(WeaponNotFound)
def not_exist(request: Request, exc: WeaponNotFound):
    return JSONResponse (
        status_code= 404,
        content= {
            'Message' : f'Uh oh ! Seems like {exc.name} is not in your weapon list, please add it to your weapon list then try again!'
        },
    )
    

@app.post('/add-weapon', response_model=Weapon)
def create_weapon(weapon: Weapon):
    weapon_dict = weapon.dict()
    
    if weapon.ATK and weapon.CD:
        dps = weapon.ATK / weapon.CD 
        weapon_dict.update({'DPS':format(dps, '.2f')})

    weapon_id = uuid4().hex
    weapon_dict.update({"id":weapon_id})
    weapons.append(weapon_dict)

    with open(weapon_file, "w") as f:
        json.dump(weapons, f, indent=4)
    return weapon_dict

@app.post('/get-best-weapon')
def get_best_weapon():
    if weapons:
        weapon_info = (None, 0)
        for w in weapons:
            if float(w['DPS']) >= weapon_info[1]:
                weapon_info = (w['name'], w['DPS'])

        return {'Message': f"Best weapon is {weapon_info[0]}, its DPS is {weapon_info[1]}."}
    else:
        raise HTTPException(410, "No weapon exist.")

@app.post('/upload-file')
def upload_file(file: Union[UploadFile, None] = None):
    if not file: 
        return {"Message" : "No file upload."}
    try:
        file_location = './' + file.filename
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
            file.close()
        upload_file_names.append(file.filename)
        return {"Result" : f"Upload File {file.filename} Success!"}
    except:
        raise FileUploadFail(name=f'{file.filename}')

@app.exception_handler(FileUploadFail)
def upload_fail(request: Request, exc: FileUploadFail):
    return JSONResponse (
        status_code= 420,
        content= {
            'Message' : f"I think {exc.name} isnt' really been uploaded, please try again!"
        },
    )
    