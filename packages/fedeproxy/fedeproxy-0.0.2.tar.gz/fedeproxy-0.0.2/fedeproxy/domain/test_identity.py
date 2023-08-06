import os

import pytest

from fedeproxy.architecture.forge.gitea import Gitea

from . import fedeproxy, identity


@pytest.fixture
def forge(tmpdir):
    f = fedeproxy.Fedeproxy(Gitea, f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8781")
    f.base_directory = f"{tmpdir}/fedeproxy"
    f.init()
    own = f.own
    own.authenticate(username="root", password="Wrobyak4")
    own.project_delete()
    email = "testuser2@example.com"
    password = "Wrobyak4"
    own.user_delete(own.owner)
    own.user_create(own.owner, password, email)
    own.authenticate(username=own.owner, password=password)
    own.init()
    yield own
    own.authenticate(username="root", password="Wrobyak4")
    own.project_delete()
    own.user_delete(own.owner)


@pytest.fixture
def identity_sample():
    emails = ["one@example.com", "two@example.com"]
    url = "url"
    owned = True
    token = "TOKEN"
    return {
        "emails": emails,
        "url": url,
        "owned": owned,
        "token": token,
    }


def test_identity_private(identity_sample):
    i = identity.IdentityPrivate()
    assert i.serialize() == {
        "emails": [],
        "url": None,
        "owned": False,
        "token": None,
    }
    assert i.is_owned() is False
    assert i.is_staged() is True
    i.unserialize(identity_sample)
    assert i.serialize() == identity_sample
    assert i.is_owned() is True
    assert i.is_staged() is False


def test_identity_public(identity_sample):
    i_private = identity.IdentityPrivate()
    i_private.unserialize(identity_sample)
    i_public = identity.IdentityPublic()
    i_public.from_private(i_private)
    expected = {
        "emails": [
            "d25354f658256d3988a0a1f07ae2dbfa64c0141b3eaa5650fd268b3fdd903b7d",
            "1f6c1f35fba8e0f461ef40adaec3cbda883f6a5bcfa5fddef2df80af49fc0832",
        ],
        "owned": True,
        "url": "url",
    }
    assert i_public.serialize() == expected
    i_public.unserialize(expected)
    assert i_public.serialize() == expected


def test_identities(forge, identity_sample):
    identities = identity.IdentitiesPrivate(forge)
    identities.init()
    assert identities.load() is False
    assert identities.identities == []
    i = identity.IdentityPrivate()
    i.unserialize(identity_sample)
    identities.identities.append(i)
    identities.save()

    identities = identity.IdentitiesPrivate(forge)
    identities.init()
    assert identities.load() is True
    identity_loaded = identities.identities[0]
    assert identity_loaded.serialize() == identity_sample
