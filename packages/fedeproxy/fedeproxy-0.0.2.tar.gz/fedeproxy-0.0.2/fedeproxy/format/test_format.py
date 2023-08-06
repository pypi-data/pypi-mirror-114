import pytest

from . import format


@pytest.fixture
def issue():
    return {
        "url": "http://example.com/issue",
        "title": "title",
        "description": "description",
        "repository": "http://example.com/repository",
        "user": "http://example.com/issue-user",
        "created_at": "2016-01-04T15:31:51.081Z",
        "closed_at": "2021-01-02 10:30:50",
        "state": "closed",
        "comments": [
            {
                "url": "http://example.com/comment1",
                "body": "body1",
                "user": "http://example.com/comment-user1",
                "created_at": "2021-01-01 10:30:50",
                "id": "comment1",
            },
            {
                "url": "http://example.com/comment2",
                "body": "body2",
                "user": "http://example.com/comment-user2",
                "created_at": "2021-01-01 10:30:50",
                "id": "comment2",
            },
        ],
        "id": "issue1234",
    }


def test_format_issue(issue, tmpdir):
    f = format.FormatIssue()
    assert f.schema.validate().valid
    p = f"{tmpdir}/issue.json"
    f.save(p, issue)
    assert f.load(p) == issue
    assert f.validate(issue)
