import datetime

from lxml import etree
from nameko.testing.services import worker_factory

from application.services.svg_builder import SvgBuilderService

TEMPLATE = '''
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg enable-background="new 0 0 255.118 308.976" height="308.976px" id="Calque_1" inkscape:version="0.91 r13725" sodipodi:docname="template_SO.svg" version="1.1" viewBox="0 0 255.118 308.976" width="255.118px" x="0px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:cc="http://creativecommons.org/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:svg="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" y="0px">
  <text id="text5638" sodipodi:linespacing="125%" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:12.5px;line-height:125%;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';text-align:start;letter-spacing:0px;word-spacing:0px;writing-mode:lr;text-anchor:start;fill:#ffffff;fill-opacity:0.94117647;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;" x="12.437594" xml:space="preserve" y="178.70859">
    <tspan id="tspan5640" sodipodi:role="line" style="fill-opacity:0.94117647;fill:#ffffff;stroke:none;stroke-opacity:1;" x="12.437594" y="178.70859">Un girondin dans le match</tspan>
  </text>
  <text content="$.referential.man_of_game.common_name" id="text7137" sodipodi:linespacing="125%" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:12.5px;line-height:125%;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';text-align:start;letter-spacing:0px;word-spacing:0px;writing-mode:lr;text-anchor:start;fill:#318ccb;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;" x="20.292917" xml:space="preserve" y="194.41924">
    <tspan id="tspan7139" sodipodi:role="line" x="20.292917" y="194.41924">Homme du match</tspan>
  </text>
  <rect origin="end" height="6.8889999" id="rect5081" style="fill:#c5ddec" width="106.117" x="87.707817" y="200.10043"/>
  <rect currentValue="$.query.soccer_match_advanced_player_stats[0].value" height="6.8889999" id="rect5083" refValue="$.query.soccer_match_advanced_player_stats[0].max_value" style="fill:#00508c" width="106.117" x="87.707817" y="200.10043"/>
  <text content="$.query.soccer_match_advanced_player_stats[0].type" id="text6086" sodipodi:linespacing="125%" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:7.5px;line-height:125%;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';text-align:start;letter-spacing:0px;word-spacing:0px;writing-mode:lr-tb;text-anchor:start;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" x="41.895054" xml:space="preserve" y="205.22029">
    placeholder
  </text>
  <text content="$.query.soccer_match_advanced_player_stats[0].type" maxLength="5" id="text6086b" sodipodi:linespacing="125%" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:7.5px;line-height:125%;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';text-align:start;letter-spacing:0px;word-spacing:0px;writing-mode:lr-tb;text-anchor:start;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" x="41.895054" xml:space="preserve" y="205.22029">
    placeholder very long
  </text>
  <text content="$.query.soccer_match_advanced_player_stats[0].value" percentage="$.query.soccer_match_advanced_player_stats[0].is_success_rate" id="text6090" sodipodi:linespacing="125%" style="font-style:normal;font-weight:normal;font-size:40px;line-height:125%;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" x="195.07384" xml:space="preserve" y="205.22029">
    <tspan id="tspan6092" sodipodi:role="line" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:7.5px;line-height:125%;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';text-align:start;writing-mode:lr-tb;text-anchor:start" x="195.07384" y="205.22029">placeholder</tspan>
  </text>
  <image id="pic1" content="$.referential.p1.picture" isVectorial="false" xlink:href="foo"/>
  <image id="logo1" content="$.referential.man_of_game.picture" isVectorial="true" xlink:href="bar"/>
  <text id="colorBlue" content="$.query.soccer_match_team_infos[0].team_id" colorValue="$.query.soccer_match_team_infos[0].color"/>
  <text id="colorRed" content="$.query.soccer_match_team_infos[0].team_id" colorValue="$.query.soccer_match_team_infos[0].color"/>
  <text id="colorGreen" content="$.query.soccer_match_team_infos[0].team_id" colorValue="$.query.soccer_match_team_infos[0].color" textColor="light: #FFFFFF;dark: #000000"/>
  <path
       id="path4865"
       class="ellipse"
       refValue="$.query.soccer_match_advanced_player_stats[0].max_value"
       currentValue="$.query.soccer_match_advanced_player_stats[0].value"
       d="m 100,50 a 50,50 0 1 0 40.450849718747364,79.38926261462365"
       style="fill:none;stroke:#875274;stroke-width:10"
       inkscape:connector-curvature="0" />
  <path
       id="path4286"
       refValue="$.query.soccer_match_teamstat[1].total"
       currentValue="$.query.soccer_match_teamstat[1].away_value"
       origin="end"
       class="ellipse"
       d="m 375.0,-62.5 a 62.5,62.5 0 0 1 0.0,125.0"
       style="stroke:#000BFF;stroke-width:20.625;fill:none" />
  <path
       id="path4866"
       refValue="$.query.soccer_match_advanced_player_stats[2].max_value"
       currentValue="$.query.soccer_match_advanced_player_stats[2].value"
       colorValue="$.query.soccer_match_advanced_player_stats[2].rank_match"
       colorMapping="default: #FFFFFF; 1: #3BA7B0; 2: #2DBA66; 3: #9F3535"
       d="m 100,50 a 50,50 0 1 0 40.450849718747364,79.38926261462365"
       style="fill:none;stroke:#875274;stroke-width:10"
       inkscape:connector-curvature="0" />
  <path
     id="path4867"
     refValue="$.query.soccer_match_advanced_player_stats[0].max_value"
     currentValue="$.query.soccer_match_advanced_player_stats[0].value"
     colorValue="$.query.soccer_match_advanced_player_stats[0].rank_match"
     colorMapping="default: #FFFFFF; 1: #3BA7B0; 2: #2DBA66; 3: #9F3535"
     disappearDefault="true"
     d="m 100,50 a 50,50 0 1 0 40.450849718747364,79.38926261462365"
     style="fill:none;stroke:#875274;stroke-width:10"
     inkscape:connector-curvature="0" />
  <g
     id="g1021"
     yPosition="$.query.soccer_match_player_lineup[{{k0}}].y"
     xPosition="$.query.soccer_match_player_lineup[{{k0}}].x"
     xReference="500"
     yReference="250"
     nRepeat="2"
     class="repeat">
    <g
       id="g1019"
       transform="translate(0,0)"
       class="template">
      <text
         x="67.895271"
         y="110.03716"
         content="$.referential.p{{k1}}.common_name"
         id="text999">label</text>
    </g>
  </g>
  <g
     id="g1022"
     yPosition="$.query.soccer_match_player_lineup[{{k0}}].y"
     xPosition="$.query.soccer_match_player_lineup[{{k0}}].x"
     xReference="500"
     yReference="250"
     nRepeat="$.query.soccer_match_player_lineup"
     class="repeat">
    <g
       id="g10123"
       transform="translate(0,0)"
       class="template">
      <text
         x="67.895271"
         y="110.03716"
         content="$.referential.p{{k1}}.common_name"
         id="text999">label</text>
    </g>
  </g>
  <g class="resizeable" id="myresizeable" adjustSize="$.query.soccer_match_advanced_player_stats[1].value">
      <rect height="6.8889999" id="rect155081" style="fill:#c5ddec" width="106.117" x="87.707817" y="200.10043"/>
  </g>
</svg>
'''


def test_replace_jsonpath():
    long_label = 'very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long label'
    results = {
        'query': {
            'soccer_match_advanced_player_stats': [
                {'max_value': 4.0, 'rank_match': 5, 'type': long_label, 'value': 0.85923323, 'is_success_rate': True},
                {'max_value': 2.0, 'rank_match': 1, 'type': 'Tirs de la tête', 'value': 1.0, 'is_success_rate': False},
                {'max_value': 4.0, 'rank_match': 1, 'type': 'Tirs non cadrés', 'value': 4.0, 'is_success_rate': False},
            ],
            'soccer_match_team_infos': [
                {'score': 1, 'side': 'Home', 'team_id': 'Amiens', 'color': '#000000'},
                {'score': 0, 'side': 'Away', 'team_id': 'Bordeaux', 'color': '#FFFFFF'}
            ],
            'soccer_match_teamstat': [
                {'total': 436 + 275, 'away_value': 436.0, 'home_value': 275.0, 'type': 'Passes réussies'},
                {'total': 8, 'away_value': 4.0, 'home_value': 4.0, 'type': 'Tirs cadrés'},
                {'total': 27, 'away_value': 14.0, 'home_value': 13.0, 'type': 'Tirs'},
                {'total': 48 + 56, 'away_value': 48.0, 'home_value': 56.0, 'type': 'Duels perdus'},
                {'total': 1., 'away_value': 0.59, 'home_value': 0.41, 'type': 'Possession'},
                {'total': 7, 'away_value': 3.0, 'home_value': 4.0, 'type': 'Corners joués'}
            ],
            "soccer_match_player_lineup": [
                {
                    "player_id": "p44413",
                    "side": "Away",
                    "nb_goals": 0,
                    "nb_yellow": 0,
                    "rank_match": 1,
                    "nb_assists": 0,
                    "type": "Buts encaissés",
                    "value": 1,
                    "nb_red": 0,
                    "team_id": "t144",
                    "x": 5,
                    "is_success_rate": False,
                    "rank_season": 138,
                    "nb_subon": 0,
                    "y": 25,
                    "formation_place": "P1"
                },
                {
                    "player_id": "p109404",
                    "side": "Away",
                    "nb_goals": 0,
                    "nb_yellow": 0,
                    "rank_match": 4,
                    "nb_assists": 0,
                    "type": "Dégagements",
                    "value": 3,
                    "nb_red": 0,
                    "team_id": "t144",
                    "x": 20,
                    "is_success_rate": False,
                    "rank_season": 858,
                    "nb_subon": 1,
                    "y": 45,
                    "formation_place": "P2"
                }
            ]
        },
        'referential': {
            'man_of_game': {
                'common_name': "Guy N'Gosso",
                'id': 'p92554',
                'informations': {
                    'first_name': 'Guy',
                    'id': 'p92554',
                    'known': "Guy N'Gosso",
                    'last_name': "N'Gosso Massouma",
                    'type': 'player'
                },
                'provider': 'opta_f9',
                'type': 'soccer player',
                'picture': '<svg id=\"myid\"></svg>'
            },
            'match': {
                'common_name': 'Amiens - Bordeaux',
                'content': {
                    'competition': 'French Ligue 1',
                    'country': 'France',
                    'name': 'Amiens - Bordeaux',
                    'season': ' 2017/2018',
                    'venue': 'Stade Océane'
                },
                'date': datetime.datetime(2017, 10, 21, 18, 0),
                'id': 'f920618',
                'provider': 'opta_f9',
                'type': 'game'
            },
            "p1": {
                'common_name': "Guy N'Gosso",
                'id': 'p92554',
                'informations': {
                    'first_name': 'Guy',
                    'id': 'p92554',
                    'known': "Guy N'Gosso",
                    'last_name': "N'Gosso Massouma",
                    'type': 'player'
                },
                'provider': 'opta_f9',
                'type': 'soccer player',
                'picture': 'base64'
            },
            "p2": {
                'common_name': "Guy N'Gosso",
                'id': 'p92554',
                'informations': {
                    'first_name': 'Guy',
                    'id': 'p92554',
                    'known': "Guy N'Gosso",
                    'last_name': "N'Gosso Massouma",
                    'type': 'player'
                },
                'provider': 'opta_f9',
                'type': 'soccer player',
                'picture': 'base64'
            }
        }
    }
    service = worker_factory(SvgBuilderService)
    converted = service.replace_jsonpath(TEMPLATE, results)
    root = etree.fromstring(converted)

    assert 'width' not in root.attrib and 'height' not in root.attrib

    lineup = root.xpath('//n:g[@class=\'repeat\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert len(lineup) == 2
    assert not lineup[0].xpath('//n:g[@class=\'template\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert len(lineup[0].getchildren()) > 0
    for c in lineup[0].getchildren():
        assert c.attrib['transform'] != 'translate(0,0)'
        texts = c.getchildren()
        assert texts[0].text == "Guy N'Gosso"

    logo = root.xpath('//n:use[@id = \'logo1\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert root.xpath('./n:defs/n:svg[@id = \'myid\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert len(logo) == 1
    assert logo[0].attrib['{http://www.w3.org/1999/xlink}href'] == '#myid'

    ellipse = root.xpath('//n:path[@id = \'path4865\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert len(ellipse) == 1
    assert ellipse[0].attrib['d'] != 'm 100,50 a 50,50 0 1 0 40.450849718747364,79.38926261462365'

    ellipse = root.xpath('//n:path[@id = \'path4866\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert len(ellipse) == 1
    assert '#3BA7B0' in ellipse[0].attrib['style']

    ellipse = root.xpath('//n:path[@id = \'path4867\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert len(ellipse) == 1
    assert 'display: none' in ellipse[0].attrib['style']

    resizeable = root.xpath('//n:g[@class=\'resizeable\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert len(resizeable) == 1
    assert 'transform' in resizeable[0].attrib
    assert resizeable[0].attrib['transform'] == 'scale(1.0,1.0)'

    blue = root.xpath('//n:text[@id = \'colorBlue\']', namespaces={'n': 'http://www.w3.org/2000/svg'})[0]
    assert 'fill:#000000' in blue.get('style')

    blue = root.xpath('//n:text[@id = \'colorGreen\']', namespaces={'n': 'http://www.w3.org/2000/svg'})[0]
    assert 'fill:#FFFFFF' in blue.get('style')


def test_clean_for_export():
    svg_string = '''
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
        <defs>
            <svg id="myid" width="10" height="20" viewBox="0 0 10 20"></svg>
        </defs>
    </svg>
    '''

    service = worker_factory(SvgBuilderService)
    res = service.clean_for_export(svg_string)

    root = etree.fromstring(res.encode('utf-8'))
    embeded = root.xpath('./n:defs/n:svg', namespaces={'n': 'http://www.w3.org/2000/svg'})[0]
    assert embeded.attrib['id'] == 'myid'
    assert 'width' not in embeded
    assert 'height' not in embeded


def test_staging_failure():
    import json
    query_result = json.load(open('./application/tests/result.json', 'r', encoding='utf-8'))
    template = open('./application/tests/template.svg', encoding='utf-8').read()

    service = worker_factory(SvgBuilderService)
    result = service.replace_jsonpath(template, query_result)
