import pytest
from flask import Flask
from flask import url_for
from flask import request
from flask import g
from flask import session


@pytest.fixture
def app(app):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "42"

    @app.route("/g")
    def g_endpoint():
        if "foo" not in g:
            g.foo = request.args["foo"]
        return g.get("foo")

    @app.route("/session")
    def session_endpoint():
        if "foo" not in session:
            session["foo"] = request.args["foo"]
        return session.get("foo")

    return app


def test_shortcut_url_for(client, url_for):
    assert url_for("g_endpoint") == "/g"
    assert url_for("session_endpoint") == "/session"


def test_shortcut_g(client, g):
    assert "foo" not in g
    client.get("/g?foo=bar")
    assert g.foo == "bar"


def test_shortcut_session(client, session):
    assert "foo" not in session
    client.get("/session?foo=bar")
    assert session["foo"] == "bar"


def test_context_is_different_for_each_request(client, g):
    res = client.get("/g?foo=bar")
    assert res.text == "bar"
    assert g.foo == "bar"

    res = client.get("/g?foo=baz")
    assert res.text == "baz"
    assert g.foo == "baz"
