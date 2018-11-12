def assert_field_in_error_display(resp, field_name):
    e = resp.soup.find("div", class_="alert")
    assert field_name in e.text
