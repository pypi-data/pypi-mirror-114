import os

from .gitea import Gitea


def test_gitea_fork():
    (Forge, url) = (Gitea, f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8781")
    forge = Forge(url)
    forge.authenticate(username="root", password="Wrobyak4")
    password = "Wrobyak4"

    username1 = "testuser1"
    email1 = "testuser1@example.com"
    forge.user_create(username1, password, email1)
    forge.project_delete(username1, "testproject")

    username2 = "testuser2"
    email2 = "testuser2@example.com"
    forge.user_create(username2, password, email2)
    forge.project_delete(username2, "testproject")

    forge.authenticate(username=username1, password=password)
    p1 = forge.project_create(username1, "testproject")

    forge.authenticate(username=username2, password=password)
    p2 = forge.project_fork(username1, "testproject")
    assert p1.id != p2.id
    assert p2.project == "testproject"
    assert p1.project == p2.project

    p3 = forge.project_fork(username1, "testproject")
    assert p2.id == p3.id

    forge.authenticate(username="root", password="Wrobyak4")
    assert forge.project_delete(username2, "testproject") is True
    assert forge.user_delete(username2) is True
    assert forge.project_delete(username1, "testproject") is True
    assert forge.user_delete(username1) is True
