import responses
import requests

from wapitiCore.net.crawler import Page


@responses.activate
def test_absolute_root():
    with open("tests/data/absolute_root_links.html") as fd:
        url = "http://perdu.com/"
        responses.add(
            responses.GET,
            url,
            body=fd.read()
        )

        resp = requests.get(url)
        page = Page(resp, url)

        assert page.links == [url]


@responses.activate
def test_relative_root():
    with open("tests/data/relative_root_links.html") as fd:
        url = "http://perdu.com/"
        responses.add(
            responses.GET,
            url,
            body=fd.read()
        )

        resp = requests.get(url)
        page = Page(resp, url)

        # We will get invalid hostnames with dots. Browsers do that too.
        assert set(page.links) == {url, "http://./", "http://../"}


@responses.activate
def test_relative_links():
    with open("tests/data/relative_links.html") as fd:
        url = "http://perdu.com/"
        responses.add(
            responses.GET,
            url,
            body=fd.read()
        )

        resp = requests.get(url)
        page = Page(resp, url)

        assert set(page.links) == {
            url,
            "http://perdu.com/file.html",
            "http://perdu.com/resource",
            "http://perdu.com/folder/",
            "http://perdu.com/folder/file.html",
            "http://perdu.com/folder/file2.html",
            "http://perdu.com/file3.html",
            "http://perdu.com/?k=v",
            "http://perdu.com/file3.html?k=v",
            "http://perdu.com/folder/?k=v",
            "http://perdu.com/folder?k=v",
            "http://external.tld/",
            "http://external.tld/yolo?k=v",
        }


@responses.activate
def test_other_links():
    with open("tests/data/other_links.html") as fd:
        url = "http://perdu.com/"
        responses.add(
            responses.GET,
            url,
            body=fd.read(),
            adding_headers={
                "Location": "https://perdu.com/login"
            },
            status=301
        )

        resp = requests.get(url, allow_redirects=False)
        page = Page(resp, url)

        assert sorted(page.iter_frames()) == [
            "http://perdu.com/frame1.html",
            "http://perdu.com/frame2.html",
            "http://perdu.com/iframe.html"
        ]
        assert page.scripts == ["http://perdu.com/script.js"]
        assert page.redirection_url == "https://perdu.com/login"
        assert set(page.images_urls) == {
            "http://perdu.com/img/logo.png",
            "http://perdu.com/img/header.png",
            "http://perdu.com/img/ads.php?id=5878545"
        }
        assert page.js_redirections == ["http://perdu.com/maintenance.html"]
        assert page.favicon_url == "http://perdu.com/favicon.ico"
        assert page.html_redirections == ["http://perdu.com/adblock.html"]


@responses.activate
def test_extra_links():
    with open("tests/data/extra_links.html") as fd:
        url = "http://perdu.com/"
        responses.add(
            responses.GET,
            url,
            body=fd.read()
        )

        resp = requests.get(url, allow_redirects=False)
        page = Page(resp, url)

        assert set(page.extra_urls) == {
            "http://perdu.com/planets.gif",
            "http://perdu.com/sun.html",
            "http://perdu.com/mercur.html",
            "http://perdu.com/venus.html",
            "http://perdu.com/link.html",
            "http://perdu.com/audio.html",
            "http://perdu.com/embed.html",
            "http://perdu.com/horse.ogg",
            "http://perdu.com/horse.mp3",
            "http://perdu.com/video.html",
            "http://perdu.com/subtitles_en.vtt",
            "http://perdu.com/dopequote.html",
            "http://perdu.com/del.html",
            "http://perdu.com/ins.html",
            "http://perdu.com/q.html",
            "http://perdu.com/data.html",
            "http://perdu.com/high-def.jpg",
            "http://perdu.com/low-def.jpg",
            "http://perdu.com/img_orange_flowers.jpg"

        }


@responses.activate
def test_meta():
    with open("tests/data/meta.html") as fd:
        url = "http://perdu.com/"
        responses.add(
            responses.GET,
            url,
            body=fd.read()
        )

        resp = requests.get(url, allow_redirects=False)
        page = Page(resp, url)

        assert page.title == "  -  Title :) "
        assert page.description == "Meta page"
        assert page.keywords == ["this", "is", " dope"]
        assert page.generator == "YoloCMS 1.0"
        assert page.text_only == "This is dope"
        assert page.favicon_url == "http://perdu.com/custom.ico"
        assert page.md5 == "2778718d04cfa16ffd264bd76b0cf18b"


@responses.activate
def test_base_relative_links():
    with open("tests/data/base_relative_links.html") as fd:
        url = "http://perdu.com/"
        responses.add(
            responses.GET,
            url,
            body=fd.read()
        )

        resp = requests.get(url)
        page = Page(resp, url)

        assert set(page.links) == {
            url,
            "http://perdu.com/blog/file.html",
            "http://perdu.com/blog/resource",
            "http://perdu.com/blog/folder/",
            "http://perdu.com/blog/folder/file.html",
            "http://perdu.com/blog/folder/file2.html",
            "http://perdu.com/folder/file2.html",
            "http://perdu.com/",
            "http://perdu.com/blog/",
            "http://perdu.com/blog/file3.html",
            "http://perdu.com/blog/?k=v",
            "http://perdu.com/blog/?k=v2",
            "http://perdu.com/blog/file3.html?k=v",
            "http://perdu.com/blog/folder/?k=v",
            "http://perdu.com/blog/folder?k=v",
            "http://external.tld/",
            "http://external.tld/yolo?k=v",
        }
