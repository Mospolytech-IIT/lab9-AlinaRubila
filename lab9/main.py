"""Fast API and other modules"""
from fastapi import FastAPI
from fastapi import Body, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

import data_base
from data_base import Session, add_new_user, get_users, User, find_user, add_new_post, update_user, \
    update_post, PostUser

app = FastAPI()
db = Session()
user_now = User()

@app.get("/")
def welcome():
    """Main page"""
    html = "<h1>Welcome!</h1>"
    return HTMLResponse(content=html)

@app.get("/management/users")
def users():
    """Users management page"""
    return FileResponse("public/view_users.html")
@app.get("/management/posts")
def posts():
    """Posts management page"""
    return FileResponse("public/view_posts.html")

@app.get("/users")
def all_users():
    """Getting all users"""
    return get_users(db)

@app.get("/users/{i_id}")
def get_user(i_id):
    """Getting user by his id"""
    user = data_base.get_user(i_id, db)
    if user is None:
        return JSONResponse(status_code=404, content={"message": "User is not found"})
    return user

@app.post("/users")
def edit_user(data=Body()):
    """Updating user information"""
    id1 = int(data["id"])
    name1 = data["username"]
    email1 = data["email"]
    password1 = data["password"]
    user = update_user(db, id1, name1, email1, password1)
    if user is None: return JSONResponse(status_code=404, content={"message": "User is not found"})
    return user

@app.delete("/users/{id1}")
def delete_user(id1):
    """Deleting user"""
    user = data_base.get_user(id1, db)
    if user is None: return JSONResponse(status_code=404, content={"message": "User is not found"})
    data_base.delete_user(db, user)
    return user

@app.get("/posts")
def all_posts():
    """Getting all the posts"""
    return data_base.get_posts1(db)

@app.get("/posts/{i_id}")
def get_post(i_id):
    """Getting post by its id"""
    post = data_base.get_post(db, i_id)
    if post is None:
        return JSONResponse(status_code=404, content={"message": "Post is not found"})
    return post
@app.post("/posts")
def edit_post(data=Body()):
    """Editing post properties"""
    id1 = int(data["id"])
    title1 = data["title"]
    content1 = data["content"]
    post = update_post(db, id1, title1, content1)
    if post is None: return JSONResponse(status_code=404, content={"message": "Post is not found"})
    user = data_base.get_user(post.user_id, db)
    post1 = PostUser()
    post1.id = post.id
    post1.title = post.title
    post1.content = post.content
    post1.author = user.username
    return post1
@app.delete("/posts/{id1}")
def delete_post(id1):
    """Deleting post"""
    post = data_base.get_post(db, id1)
    if post is None: return JSONResponse(status_code=404, content={"message": "Post is not found"})
    data_base.delete_post(db, post)
    return post

@app.get("/register")
def reg_form():
    """Register page"""
    return FileResponse("public/register_form.html")

@app.put("/register")
def register(data=Body()):
    """Registration of new user"""
    name = data["username"]
    email = data["email"]
    password = data["password"]
    user = add_new_user(name, email, password, db)
    global user_now
    user_now = user
    return {"message": "registered successfully!"}

@app.post("/login")
def login(username: str = Form(), password: str =Form()):
    """Logging user in"""
    i = find_user(username, password, db)
    if i is None:
        return {"message": f"invalid login or password"}
    global user_now
    user_now = i
    return {"message": "signed in successfully!"}
@app.get("/login")
def send_file():
    """Login page"""
    return FileResponse("public/index.html")
@app.get("/createpost")
def post_form():
    """Post page"""
    return FileResponse("public/post_form.html")
@app.post("/posting")
def posting(data=Body()):
    """Creating new post"""
    title = data["title"]
    content = data["content"]
    add_new_post(title, content, user_now, db)
    return {"message": "Post has been created!"}


