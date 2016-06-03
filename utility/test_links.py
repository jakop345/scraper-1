from links_validator import check_links


def test_link_checker():
    urls = [("github", ("https://github.com/asfjlln", "https://github.com",))]
    codes = check_links(urls)
    assert codes[0][2] == 404
    assert codes[1][2] == 200
