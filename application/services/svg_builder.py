from nameko.rpc import rpc

from application.services.schemas import PlayerNewsReportSchema


class SvgBuilderError(Exception):
    pass


class SvgBuilderService(object):

    name = 'svg_builder'

    @rpc
    def player_report(self, parameters, width, height, main_font, figure_font, title_font, primary_color,
                      secondary_color):
        model = PlayerNewsReportSchema().load(parameters)

        if model.errors:
            raise SvgBuilderError('Wrong formatted parameters {}'.format(str(model.errors)))

        report = model.data

        return report.to_svg(width, height, main_font, figure_font, title_font, primary_color, secondary_color)
