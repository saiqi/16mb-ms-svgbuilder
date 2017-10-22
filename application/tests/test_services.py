import datetime

from nameko.testing.services import worker_factory

from application.services.svg_builder import SvgBuilderService

TEMPLATE = '''
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   version="1.1"
   id="Calque_1"
   x="0px"
   y="0px"
   width="255.118px"
   height="308.976px"
   viewBox="0 0 255.118 308.976"
   enable-background="new 0 0 255.118 308.976"
   xml:space="preserve"
   inkscape:version="0.91 r13725"
   sodipodi:docname="template_SO.svg">

    <text
         xml:space="preserve"
         style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:12.5px;line-height:125%;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';text-align:start;letter-spacing:0px;word-spacing:0px;writing-mode:lr-tb;text-anchor:start;fill:#318ccb;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
         x="20.292917"
         y="194.41924"
         id="text7137"
         sodipodi:linespacing="125%"
         content="$.referential.man_of_game.common_name">
             <tspan
               sodipodi:role="line"
               id="tspan7139"
               x="20.292917"
               y="194.41924">Homme du match</tspan>
    </text>
    <rect
     style="fill:#c5ddec"
     x="87.707817"
     y="200.10043"
     width="106.117"
     height="6.8889999"
     id="rect5081" />
     <rect
     style="fill:#00508c"
     x="87.707817"
     y="200.10043"
     width="3.6570001"
     height="6.8889999"
     id="rect5083"
     currentValue="$.query.soccer_match_advanced_player_stats[0].value"
     refValue="$.query.soccer_match_advanced_player_stats[0].max_value" />
</svg>
'''


def test_replace_jsonpath():
    results = {
        'query': {
            'soccer_match_advanced_player_stats': [
                {'max_value': 2.0, 'rank_match': 1, 'type': 'Tirs de la tête', 'value': 1.0},
                {'max_value': 4.0, 'rank_match': 1, 'type': 'Tirs non cadrés', 'value': 4.0}
            ],
            'soccer_match_team_infos': [
                {'score': 1, 'side': 'Home', 'team_id': 'Amiens'},
                {'score': 0, 'side': 'Away', 'team_id': 'Bordeaux'}
            ],
            'soccer_match_teamstat': [
                {'away_value': 436.0, 'home_value': 275.0, 'type': 'Passes réussies'},
                {'away_value': 4.0, 'home_value': 4.0, 'type': 'Tirs cadrés'},
                {'away_value': 14.0, 'home_value': 13.0, 'type': 'Tirs'},
                {'away_value': 48.0, 'home_value': 56.0, 'type': 'Duels perdus'},
                {'away_value': 0.59, 'home_value': 0.41, 'type': 'Possession'},
                {'away_value': 3.0, 'home_value': 4.0, 'type': 'Corners joués'}
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
                'type': 'soccer player'
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

    print(converted)
