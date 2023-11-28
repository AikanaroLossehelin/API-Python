# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:18:13 2023

@author: aikan

uvicorn TD4_serv:app --reload
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import uvicorn
import bcrypt
from TD4_data import *
from typing import Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


app = FastAPI()

#Limiteur restreignant le nombre de requêtes appelables par certains utilisateurs
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Fonction de vérification du token de l'utilisateur
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except jwt.PyJWTError:
        raise credentials_exception

#Fonction de limitation selon l'authentification
def rate_limit_key(request: Request) -> str:
    # Obtenez le token de l'utilisateur à partir du header d'autorisation
    authorization: str = request.headers.get("Authorization")
    token = authorization.split()[1] if authorization else None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            user = next((u for u in users if u['email'] == email), None)
            if user:
                return f"licence:{user['licence']}"  # Clé basée sur la licence de l'utilisateur
        except jwt.PyJWTError:
            pass

    return "unauthenticated"  # Clé pour les utilisateurs non authentifiés

#Permet d'identifier l'utilisateur actuel à l'aide de son token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_token(token, credentials_exception)
    user = next((u for u in users if u['email'] == email), None)
    if user is None:
        raise credentials_exception
    return UserInDB(**user)

#Méthode de hashage du mot de passe utilisateur pour la mémorisation sécurisée
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

for user in users:
    user['hashed_password'] = hash_password(user["password"])
    
    
@app.post("/token")
@limiter.limit("10/minute", key_func=rate_limit_key, error_message="Limite de requêtes atteinte")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in users if u['pseudo'] == form_data.username), None)
    if user and verify_password(form_data.password, user['hashed_password']) and not user['disabled']:
        access_token = create_access_token(data={"sub": user["email"]})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Informations d'identification incorrectes ou compte désactivé")


@app.post("/signup")
@limiter.limit("10/minute", key_func=rate_limit_key, error_message="Limite de requêtes atteinte")
#Création de compte et ajout à la base de données
async def signup(user: User):
    # Vérifie si l'utilisateur existe déjà
    existing_user = next((u for u in users if u['email'] == user.email), None)
    if existing_user:
        raise HTTPException(status_code=400, detail="L'utilisateur existe déjà")

    # Hashe le mot de passe
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    # Crée un nouvel utilisateur
    new_user = {
        "nom": user.nom,
        "prenom": user.prenom,
        "pseudo": user.pseudo,
        "email": user.email,
        "hashed_password": hashed_password,
        "disabled": user.disabled,
        "licence": user.licence
    }

    # Ajoutez le nouvel utilisateur à la liste des utilisateurs
    users.append(new_user)

    return {"message": "Utilisateur créé avec succès"}


@app.put("/user/licence")
#Modification de la licence de l'utilisateur
async def update_licence(request: Request, licence_update: LicenceUpdate, current_user: UserInDB = Depends(get_current_user)):
    user = next((u for u in users if u['email'] == current_user.email), None)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    
    user['licence'] = licence_update.licence
    return {"message": "Licence mise à jour avec succès"}


@app.get("/user/licence")
@limiter.limit("10/minute", key_func=rate_limit_key, error_message="Limite de requêtes atteinte")
#Récupération et lecture de la licence de l'utilisateur
async def get_user_licence(request: Request, current_user: UserInDB = Depends(get_current_user)):
    return {"licence": current_user.licence}


@app.get("/indicators/rsi")
@limiter.limit("10/minute", key_func=rate_limit_key, error_message="Limite de requêtes atteinte")
#Récupération et lecture des données RSI par l'utilisateur
async def read_rsi(request: Request, current_user: User = Depends(get_current_user), data = indicators):
    user = next((u for u in users if u['email'] == current_user.email), None)
    if user and user['licence'] != "étudiant":
        return {f"data : {data['RSI']}"}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit pour les utilisateurs avec une licence étudiante")
    
    
@app.get("/indicators/macd")
@limiter.limit("10/minute", key_func=rate_limit_key, error_message="Limite de requêtes atteinte")
#Récupération et lecture des données MACD par l'utilisateur
async def read_macd(request: Request, current_user: User = Depends(get_current_user), data = indicators):
    user = next((u for u in users if u['email'] == current_user.email), None)
    if user and user['licence'] != "étudiant":
        return {f"data : {data['MACD']}"}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit pour les utilisateurs avec une licence étudiante")


@app.get("/coins/coin")
@limiter.limit("10/minute", key_func=rate_limit_key, error_message="Limite de requêtes atteinte")
#Récupération et lecture des données des monnaies par l'utilisateur (peut stipuler une monnaie précise)
async def read_coin(request: Request, name: Optional[str] = None, data = coins):
    if name:
        filtered_coins = [coin for coin in coins['coin'] if coin['name'] == name]
        return {f"{filtered_coins}"}
    else :
        return {f"{data['coin']}"}