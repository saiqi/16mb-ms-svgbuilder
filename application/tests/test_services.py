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
  <text content="$.query.soccer_match_advanced_player_stats[0].value" percentage="$.query.soccer_match_advanced_player_stats[0].is_success_rate" id="text6090" sodipodi:linespacing="125%" style="font-style:normal;font-weight:normal;font-size:40px;line-height:125%;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" x="195.07384" xml:space="preserve" y="205.22029">
    <tspan id="tspan6092" sodipodi:role="line" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:7.5px;line-height:125%;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';text-align:start;writing-mode:lr-tb;text-anchor:start" x="195.07384" y="205.22029">placeholder</tspan>
  </text>
  <image id="pic1" content="$.referential.man_of_game.picture" isVectorial="false" xlink:href="foo"/>
  <image id="logo1" content="$.referential.man_of_game.logo" isVectorial="true" xlink:href="bar"/>
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
                {'score': 1, 'side': 'Home', 'team_id': 'Amiens'},
                {'score': 0, 'side': 'Away', 'team_id': 'Bordeaux'}
            ],
            'soccer_match_teamstat': [
                {'total': 436 + 275, 'away_value': 436.0, 'home_value': 275.0, 'type': 'Passes réussies'},
                {'total': 8, 'away_value': 4.0, 'home_value': 4.0, 'type': 'Tirs cadrés'},
                {'total': 27, 'away_value': 14.0, 'home_value': 13.0, 'type': 'Tirs'},
                {'total': 48 + 56, 'away_value': 48.0, 'home_value': 56.0, 'type': 'Duels perdus'},
                {'total': 1., 'away_value': 0.59, 'home_value': 0.41, 'type': 'Possession'},
                {'total': 7, 'away_value': 3.0, 'home_value': 4.0, 'type': 'Corners joués'}
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
                'picture': 'base64',
                'logo': '<svg></svg>'
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
            }
        }
    }
    service = worker_factory(SvgBuilderService)
    converted = service.replace_jsonpath(TEMPLATE, results)
    root = etree.fromstring(converted)

    logo = root.xpath('//n:image[@id = \'logo1\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert len(logo) == 1

    ellipse = root.xpath('//n:path[@id = \'path4865\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert len(ellipse) == 1
    assert ellipse[0].attrib['d'] != 'm 100,50 a 50,50 0 1 0 40.450849718747364,79.38926261462365'

    ellipse = root.xpath('//n:path[@id = \'path4866\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert len(ellipse) == 1
    assert '#3BA7B0' in ellipse[0].attrib['style']

    ellipse = root.xpath('//n:path[@id = \'path4867\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
    assert len(ellipse) == 1
    assert 'display: none' in ellipse[0].attrib['style']
