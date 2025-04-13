from typing import List, Dict, Any
from fastapi import HTTPException, Depends, APIRouter, Request, status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session

try:
    from app.database import get_db
    from app.models import User
    from app.schemas import CreateUser, LoginUser
    from app.utils import verify_password, hash_password, create_access_token
except ImportError:
    from database import get_db
    from models import User
    from schemas import CreateUser, LoginUser
    from utils import verify_password, hash_password, create_access_token

from authlib.integrations.starlette_client import OAuth

# FastAPI Router
router = APIRouter(
    prefix='/user',
    tags=['User']
)

# Google OAuth Setup
oauth = OAuth()
oauth.register(
    name='google',
    client_id='286378699697-fu271gubg7b9mi8s9uaclafjkorb9eqt.apps.googleusercontent.com',
    client_secret='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',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
    authorize_params={"access_type": "offline", "prompt": "consent"},
)


@router.get('/', response_model=List[CreateUser])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()

    if existing_user:
        response = RedirectResponse(
            url="http://localhost:5173/login", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="message", value="User already exists. Please login.", httponly=False)
        return response

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email,
                    password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "redirect_url": "http://localhost:5173/"}


@router.post('/login', status_code=status.HTTP_200_OK)
@router.post('/login', status_code=status.HTTP_200_OK)
def login(user: LoginUser, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        (User.username == user.username_or_email) | (User.email == user.username_or_email)
    ).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": db_user.username,
        "email": db_user.email
    }



@router.get('/google/login')
async def google_login(request: Request):
    try:
        redirect_uri = request.url_for('google_auth')
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        print(f"Error during Google Login: {e}")
        raise HTTPException(status_code=500, detail=f"Google Login Error: {e}")


@router.get('/google/auth')
async def google_auth(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(
                status_code=400, detail="Google authentication failed")

        db_user = db.query(User).filter(
            User.email == user_info['email']).first()
        if not db_user:
            db_user = User(
                username=user_info['name'], email=user_info['email'], password="google_oauth"
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        access_token = create_access_token({"sub": db_user.email})
        redirect_url = f"http://localhost:5173/google-login?token={access_token}&username={db_user.username}"
        print(f"Redirecting to: {redirect_url}")
        return RedirectResponse(url=redirect_url)

    except Exception as e:
        print(f"Error during Google authentication: {e}")
        raise HTTPException(status_code=500, detail=f"Google Auth Error: {e}")


@router.delete('/delete-user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID {id} not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.patch('/update-user/{id}', response_model=CreateUser)
def update_user(id: int, update_data: Dict[str, Any], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID {id} not found")

    for key, value in update_data.items():
        if hasattr(user, key):
            if key == 'password':
                value = hash_password(value)
            setattr(user, key, value)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid field: {key}")

    db.commit()
    db.refresh(user)
    return user
