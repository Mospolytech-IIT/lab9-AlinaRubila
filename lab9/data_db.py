"""Imports from other module for testing"""
from data_base import Session, User, Post, add_new_user, add_new_post, get_users, get_posts, get_posts_user, \
    update_email, update_content, delete_post, delete_user

db = Session()

alina = add_new_user("Alina", "ali@mail.ru", "pelic12", db)
agatha = add_new_user("Agatha Edith", "roses@gmail.com", "reddreamfox", db)
pelican = add_new_user("Pelican", "aaf412@mail.ru", "aline2003", db)
no_name = add_new_user("No Name", "null@post.com", "424242", db)
post1 = add_new_post("Tradegy!", "You won't believe - they rejected my internship application! I'm so saaad(", alina, db)
post2 = add_new_post("I'm bored", "Someone - let's play minecraft together!", alina, db)
post3 = add_new_post("I published new chapter!", "Go to Ficbook: new chapter of Borderline is on now!", pelican, db)
post4 = add_new_post("Did you know...", "...that your music taste is amazing? Now you know it!", agatha, db)
post5 = add_new_post("I know an answer", "it's 42, lol", no_name, db)
post6 = add_new_post("Someday I'll be gone", "but you won't forget me, no-no", no_name, db)

us = get_users(db)
for u in us:
    print(f"{u.id} {u.username} {u.email}")
pt = get_posts(db)
for p in pt:
    print(f"{p[0].id} {p[0].title} {p[0].content} {p[1]}")
pt = get_posts_user(db, alina)
for p in pt:
    print(f"{p.id} {p.title} {p.content}")
agatha = update_email(db, agatha, "black@post.com")
print(f"{agatha.email}")
post6 = update_content(db, post6, "nah, I'm just kidding")
print(f"{post6.content}")
delete_post(db, post2)
pt = get_posts_user(db, alina)
for p in pt:
    print(f"{p.id} {p.title} {p.content}")
delete_user(db, no_name)
pt = get_posts(db)
for p in pt:
    print(f"{p[0].id} {p[0].title} {p[0].content} {p[1]}")

