from tests.model_tools import create_user

def login(client, faker):
    u = create_user(faker)

    resp = client.get("/login")

    crf_token = resp.soup.find(
        "input", {"name": "csrf_token"}, type="hidden", id="csrf_token"
    )

    data = dict(email=u.email, password=u.password)

    if crf_token:
        data["csrf_token"] = crf_token.get("value")

    client.post("/login", data=data, follow_redirects=True)

    return u


def assert_field_in_error_display(resp, field_name):
    e = resp.soup.find("div", class_="alert")
    assert field_name in e.text

