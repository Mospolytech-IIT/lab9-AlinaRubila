"""Modules"""
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker
from sqlalchemy import  Column, Integer, String

Base = declarative_base()

class User(Base):
    """Class for user table"""
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True)
    email = Column(String(20), unique=True)
    password = Column(String(15))
class Post(Base):
    """Class for post table"""
    __tablename__ = "Posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30))
    content = Column(String(500))
    user_id = Column(Integer, ForeignKey(User.id))
engine = create_engine("mysql+pymysql://root:niceMeow@localhost/backend")
Base.metadata.create_all(engine)
Session = sessionmaker(autoflush=False, bind=engine)

def add_new_user(i_username, i_email, i_password, db: Session):
    """Adding new user to db"""
    user = User(username=i_username, email=i_email, password=i_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
def find_user(i_name, i_password, db:Session):
    """Finding user in db while signing in"""
    user = db.query(User).filter(User.username==i_name).first()
    if user.password == i_password:
        return user
    else:
        return None
def add_new_post(i_title, i_content, i_user: User, db: Session):
    """Adding new post to db"""
    post = Post(title=i_title, content=i_content, user_id=i_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
def get_users(db: Session):
    """Getting all the users in db"""
    users = db.query(User).all()
    return users
def get_user(i_id, db: Session):
    """Getting one user by his id"""
    user = db.query(User).filter(User.id==i_id).first()
    return user
def get_posts(db: Session):
    """Getting posts from db"""
    posts = db.query(Post).all()
    result = []
    for p in posts:
        u = db.query(User).filter(User.id == p.user_id).first()
        item = [p, u.username]
        result.append(item)
    return result
class PostUser:
    """Class for formating posts"""
    id: int
    title: str
    content: str
    author: str
def get_posts1(db: Session):
    """Getting formated posts from db"""
    posts = db.query(Post).all()
    result = []
    for p in posts:
        u = db.query(User).filter(User.id == p.user_id).first()
        item = PostUser()
        item.id = p.id
        item.title = p.title
        item.content = p.content
        item.author = u.username
        result.append(item)
    return result
def get_posts_user(db: Session, user: User):
    """Getting posts of certain user"""
    posts = db.query(Post).filter(Post.user_id==user.id).all()
    return posts
def get_post(db: Session, i_id):
    """Getting one post from db by its id"""
    post = db.query(Post).filter(Post.id==i_id).first()
    return post

def update_user(db:Session, id1, name1, email1, password1):
    """Updating user information"""
    user1 = db.query(User).filter(User.id==id1).first()
    if user1 is None: return None
    user1.username = name1
    user1.email = email1
    user1.password = password1
    db.commit()
    db.refresh(user1)
    return user1
def update_post(db: Session, id1, title1, content1):
    """Updating post information"""
    post1 = db.query(Post).filter(Post.id==id1).first()
    if post1 is None: return None
    post1.title = title1
    post1.content = content1
    db.commit()
    db.refresh(post1)
    return post1

def update_email(db: Session, user1: User, new_email):
    """Updating user email"""
    user = db.query(User).filter(User.id==user1.id).first()
    user.email = new_email
    db.commit()
    db.refresh(user)
    return user
def update_content(db: Session, post1: Post, new_content):
    """Updating content of the post"""
    post = db.query(Post).filter(Post.id==post1.id).first()
    post.content = new_content
    db.commit()
    db.refresh(post)
    return post
def delete_post(db: Session, post1: Post):
    """Deleting post"""
    post = db.query(Post).filter(Post.id == post1.id).first()
    db.delete(post)
    db.commit()
def delete_user(db: Session, user1: User):
    """Deleting user and his posts"""
    user = db.query(User).filter(User.id==user1.id).first()
    posts = db.query(Post).filter(Post.user_id == user.id).all()
    db.delete(user)
    for p in posts:
        db.delete(p)
    db.commit()
