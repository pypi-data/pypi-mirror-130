import re

import slimit
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

# suppress useless ply warnings
slimit.lexer.ply.lex.PlyLogger = slimit.parser.ply.yacc.PlyLogger = type(
    "_NullLogger",
    (slimit.lexer.ply.lex.NullLogger,),
    dict(__init__=lambda s, *_, **__: (None, s.super().__init__())[0]),
)
parser = Parser()


def get_title(html):
    parsed = BeautifulSoup(html, features="html.parser")
    player = parsed.body.find("div", attrs={"class": "fake-table-cell"})
    artists = player.h2.span.text.strip().split(", ")
    player.h2.span.replace_with("")
    name = player.h2.text.strip()

    return {"artists": artists, "title": name}


def parse_song(html, searched=None) -> dict:
    parsed = BeautifulSoup(html, features="html.parser")
    marso = parsed.body.find("script", attrs={"id": "linkfire-widget-data"})
    tree = parser.parse(marso.text)
    fields = {
        getattr(node.left, "value", ""): getattr(node.right, "value", "")
        for node in nodevisitor.visit(tree)
        if isinstance(node, ast.Assign)
    }

    artwork = fields["artwork"].strip('" ').replace("\\", "").strip()
    pagetitle = parsed.head.title.text.strip()
    comp = re.compile("(\((ft|Ft|feat|Feat)(|\.) .*\))")

    fts = comp.findall(pagetitle)
    feats = set()
    artists = set()
    for ft in fts:
        if isinstance(ft, tuple):
            ft = ft[0]

        ft = ft.strip("( )").replace("ft. ", "", 1).strip().split(" & ")

        for ft in ft:
            feats.add(ft)

    datas = pagetitle.split(" - ")
    artists_ = datas[0].strip("( )").replace("ft. ", "", 1).strip().split(" & ")
    for artist in artists_:
        artist = artist.strip()
        if ", " in artist:
            for a in artist.split(", "):
                artists.add(a)
        else:
            artists.add(artist)

    feats = list(feats)
    artists = list(artists) + feats
    for ft in fts:
        if isinstance(ft, tuple):
            ft = ft[0]

        datas[1] = datas[1].strip().replace(ft, "").strip()

    if len(datas) == 1:
        title = datas[0]
        artists = []
    else:
        title = datas[1]

    ret = {"title": title.strip(), "artists": artists, "artwork": artwork.strip()}
    if not searched:
        return ret

    ars_ = list(set(searched["artists"] + ret["artists"]))
    lows = []
    ars = []
    for ar in ars_:
        ar = ar.strip()
        if not ar.lower() in lows:
            lows.append(ar.lower())
            ars.append(ar)

    searched.update(ret)
    searched["artists"] = ars
    return searched


def parse_search_results(html, wanted_artists=[]) -> dict:
    data = {"items": []}
    parsed = BeautifulSoup(html, features="html.parser")
    tbody = parsed.body.find("table", attrs={"class": "tablesorter"})
    if tbody == None:
        data["pages"] = 0
        return data

    tbody = tbody.tbody
    results = tbody.find_all("tr")
    for res in results:

        datas = res.find_all("td")[3]
        id = datas.a["href"].strip("/")
        title = datas.a.p.text.strip()
        artists = datas.span.text.strip().split(", ")
        artists_ = datas.span.text.lower().strip().split(", ")
        versions = res.find_all("td")[6].text.lower().split(", ")
        date = res.find_all("td")[5].text.strip()
        if not all(item.lower() in artists_ for item in wanted_artists):
            continue

        data["items"].append(
            {
                "id": id.strip(),
                "title": title.strip(),
                "artists": artists,
                "versions": versions,
                "release_date": date,
            }
        )

    pages = (parsed.body.find("ul", attrs={"class": "pagination"})) or 1
    if pages != 1:
        pages = pages.find_all("li", attrs={"class": "page-item"})[-2].text

    data["pages"] = pages
    return data
