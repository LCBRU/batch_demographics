from batch_demographics.database import db


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


def create_user(faker):
    u = faker.user_details()
    db.session.add(u)
    db.session.commit()

    return u