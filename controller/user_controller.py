from app import app
from model.user_model import user_model

obj = user_model()
@app.route('/')
def user_sign_controller():
    return obj.user_sign()