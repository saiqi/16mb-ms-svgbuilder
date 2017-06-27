from nameko.testing.services import worker_factory

from application.services.svg_builder import SvgBuilderService


def test_player_news_report():
    service = worker_factory(SvgBuilderService)

    parameters = {
        'title': 'My wonderful and amazing title',
        'background': None,
        'player_picture': None,
        'season_picture': None,
        'competition_picture': None,
        'season_entity': {
            'id': '2016',
            'type': 'season',
            'provider': 'internet',
            'common_name': '2015/2016',
            'informations': {
                'id': '2016',
                'name': '2015/2016'
            }
        },
        'player_entity': {
            'id': 'p9808',
            'common_name': 'Harold Dudleynotovic',
            'type': 'player',
            'provider': 'internet',
            'informations': {
                'first_name': 'Harold',
                'last_name': 'Dudleynotovic',
                'nickname': None
            }
        },
        'summary': [
            {
                'type': 'nb_games_played',
                'name': 'Match Joués',
                'value': 25
            },
            {
                'type': 'nb_games_started',
                'name': 'Titulaire',
                'value': 23
            },
            {
                'type': 'nb_games_not_started',
                'name': 'Remplaçant',
                'value': 2
            }
        ],
        'events': [
            {
                'type': 'nb_goals',
                'name': 'Buts',
                'value': 7
            },
            {
                'type': 'nb_assists',
                'name': 'Passes D',
                'value': 10
            }
        ],
        'stats': [
            {
                'denominator': None,
                'formula_id': 'passes_left',
                'name': 'Left Passes',
                'from_date': '2015-08-30',
                'interval': 2552.0,
                'is_negative': False,
                'is_success_rate': False,
                'numerator': 155.0,
                'player_id': 'p9808',
                'to_date': '2016-05-14',
                'value': 155.0,
                'rank': 144
            },
            {
                'denominator': None,
                'formula_id': 'total_cross',
                'name': 'Centres',
                'from_date': '2015-08-30',
                'interval': 2552.0,
                'is_negative': False,
                'is_success_rate': False,
                'numerator': 73.0,
                'player_id': 'p9808',
                'to_date': '2016-05-14',
                'value': 73.0,
                'rank': 5
            },
            {
                'denominator': None,
                'formula_id': 'total_scoring_att',
                'name': 'Tirs',
                'from_date': '2015-08-30',
                'interval': 2552.0,
                'is_negative': False,
                'is_success_rate': False,
                'numerator': 0.0,
                'player_id': 'p9808',
                'to_date': '2016-05-14',
                'value': 0.0,
                'rank': 1500
            },
            {
                'denominator': None,
                'formula_id': 'total_contest',
                'name': 'Dribbles',
                'from_date': '2015-08-30',
                'interval': 2552.0,
                'is_negative': False,
                'is_success_rate': False,
                'numerator': 2.0,
                'player_id': 'p9808',
                'to_date': '2016-05-14',
                'value': 2.0,
                'rank': 152
            },
            {
                'denominator': None,
                'formula_id': 'interception',
                'name': 'Interceptions',
                'from_date': '2015-08-30',
                'interval': 2552.0,
                'is_negative': False,
                'is_success_rate': False,
                'numerator': 18.0,
                'player_id': 'p9808',
                'to_date': '2016-05-14',
                'value': 18.0,
                'rank': 85
            },
            {
                'denominator': None,
                'formula_id': 'red_card',
                'name': 'Cartons rouges',
                'from_date': '2015-08-30',
                'interval': 2552.0,
                'is_negative': False,
                'is_success_rate': False,
                'numerator': 3.0,
                'player_id': 'p9808',
                'to_date': '2016-05-14',
                'value': 3.0,
                'rank': 1
            }
        ]
    }

    svg = service.player_report(parameters, 500, 300, 'Impact', 'Impact', 'Impact', 'lightblue', 'darkblue')

    print(svg)

    assert svg
