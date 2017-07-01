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
        'summary': {
            'nb_games_played': 25,
            'nb_games_started': 23,
            'nb_games_not_started': 2
        },
        'events': {
            'nb_goals': 7,
            'nb_assists': 10
        },
        'stats': [
            {
                'denominator': None,
                'id': 'passes_left',
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
                'id': 'total_cross',
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
                'id': 'total_scoring_att',
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
            # {
            #     'denominator': None,
            #     'id': 'total_contest',
            #     'from_date': '2015-08-30',
            #     'interval': 2552.0,
            #     'is_negative': False,
            #     'is_success_rate': False,
            #     'numerator': 2.0,
            #     'player_id': 'p9808',
            #     'to_date': '2016-05-14',
            #     'value': 2.0,
            #     'rank': 152
            # },
            # {
            #     'denominator': None,
            #     'id': 'interception',
            #     'from_date': '2015-08-30',
            #     'interval': 2552.0,
            #     'is_negative': False,
            #     'is_success_rate': False,
            #     'numerator': 18.0,
            #     'player_id': 'p9808',
            #     'to_date': '2016-05-14',
            #     'value': 18.0,
            #     'rank': 85
            # },
            # {
            #     'denominator': None,
            #     'id': 'red_card',
            #     'from_date': '2015-08-30',
            #     'interval': 2552.0,
            #     'is_negative': False,
            #     'is_success_rate': False,
            #     'numerator': 3.0,
            #     'player_id': 'p9808',
            #     'to_date': '2016-05-14',
            #     'value': 3.0,
            #     'rank': 1
            # }
        ],
        'translations': [
            {'identifier': 'nb_games_played', 'language': 'fr', 'translation': 'Matchs Joués'},
            {'identifier': 'nb_games_started', 'language': 'fr', 'translation': 'Titulaire'},
            {'identifier': 'nb_games_not_started', 'language': 'fr', 'translation': 'Remplaçant'},
            {'identifier': 'nb_goals', 'language': 'fr', 'translation': 'Buts'},
            {'identifier': 'nb_assists', 'language': 'fr', 'translation': 'Passes D'},
            {'identifier': 'red_card', 'language': 'fr', 'translation': 'Cartons rouges'},
            {'identifier': 'interception', 'language': 'fr', 'translation': 'Interceptions'},
            {'identifier': 'total_contest', 'language': 'fr', 'translation': 'Dribbles'},
            {'identifier': 'total_scoring_att', 'language': 'fr', 'translation': 'Tirs'},
            {'identifier': 'total_cross', 'language': 'fr', 'translation': 'Centres'},
            {'identifier': 'passes_left', 'language': 'fr', 'translation': 'Passes côté gauche'},
        ]
    }

    svg = service.player_report(parameters, 800, 400, 'Impact', 'Impact', 'Impact', 'lightblue', 'darkblue')

    print(svg)

    assert svg
