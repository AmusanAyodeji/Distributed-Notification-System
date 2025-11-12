from fastapi import APIRouter, Depends
from schema.user import UserCreate, UserOut as User, UserPreference
from services.auth import get_password_hash, init_db_connection, get_current_user
from typing import Annotated

router = APIRouter()

@router.post("/api/v1/users/")
def create_user(user_data:UserCreate):
    conn,cur = init_db_connection()
    cur.execute("SELECT * FROM users WHERE email = %s",(user_data.email,))
    user = cur.fetchone()
    if user:
        return {"error": "User with this email already exists."}
    
    if user_data.preferences.email and user_data.preferences.push:
        response = {
        "success": False,
        "message": "Email and Push cannot both be true",
        "data": user_data.preferences,
        "meta": {}
        }
        return response
    
    elif not user_data.preferences.email and not user_data.preferences.push:
        response = {
        "success": False,
        "message": "Email and Push cannot both be false",
        "data": user_data.preferences,
        "meta": {}
        }
        return response


    hashed_password = get_password_hash(user_data.password)
    cur.execute("INSERT INTO users (name, email, push_token, pref_email, pref_push, password) VALUES (%s, %s, %s, %s, %s, %s)",(user_data.name, user_data.email, user_data.push_token, user_data.preferences.email, user_data.preferences.push, hashed_password))
    conn.commit()
    cur.close()
    conn.close()
    response = {
        "success": True,
        "message": "User created",
        "data": User(
            name=user_data.name,
            email=user_data.email,
            push_token=user_data.push_token,
            preferences=user_data.preferences
        ),
        "meta": {}
    }
    return response

#do not include push token in things for user to input, it will be automatically gotten from their devices and saved to db

@router.get("/api/v1/users/me")
def get_user_info(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.patch("/api/v1/users/update/{user_preference}")
def change_notification_preference(preference: UserPreference, current_user: Annotated[User, Depends(get_current_user)]):
    if preference.email and preference.push:
        response = {
        "success": False,
        "message": "Email and Push cannot both be true",
        "data": preference,
        "meta": {}
        }
        return response
    elif not preference.email and not preference.push:
        response = {
        "success": False,
        "message": "Email and Push cannot both be false",
        "data": preference,
        "meta": {}
        }
        return response

    conn, cur = init_db_connection()
    cur.execute("UPDATE users SET pref_email = %s AND pref_push = %s WHERE email = %s",(preference.email, preference.push, current_user.email))
    conn.commit()
    cur.close()
    conn.close()
    response = {
        "success": True,
        "message": "Preference Updated",
        "data": preference,
        "meta": {}
    }
    return response

