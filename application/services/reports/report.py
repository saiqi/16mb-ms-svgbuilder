import math
import svgwrite.container
import svgwrite.shapes
import svgwrite.text
import svgwrite.path


class Report(object):

    @staticmethod
    def _name_from_translations(identifier, translations):
        return [r['translation'] for r in translations if r['identifier'] == identifier][0]

    @staticmethod
    def _number_to_px(number):
        return str(int(math.floor(number))) + 'px'

    @staticmethod
    def _make_title(title, width, height, font, primary_color, secondary_color):
        group = svgwrite.container.Group(class_='title', transform='translate(5,5)', id='title')

        rect_height = Report._number_to_px(height)
        rect_width = Report._number_to_px(width)
        rect_el = svgwrite.shapes.Rect(size=(rect_width, rect_height), rx='3px', ry='3px', fill=primary_color,
                                       stroke=secondary_color, stroke_width='3px')
        group.add(rect_el)

        text_y = Report._number_to_px(.5 * height)
        text_x = '5px'
        text_length = Report._number_to_px(.9 * width)
        text_style = '''
        fill: {};
        font-size: {};
        font-family: {};
        '''.format(secondary_color, Report._number_to_px(.9 * height), font)
        text_el = svgwrite.text.Text(title, x=[text_x], y=[text_y], textLength=text_length, fill=secondary_color,
                                     dominant_baseline='central', style=text_style.replace(' ', '').replace('\t', ''))

        group.add(text_el)

        return group, (rect_width, rect_height)

    @staticmethod
    def _make_event_label(event_id, event_name, event_figure, width, height, figure_font, text_font,
                          primary_color, secondary_color):
        group = svgwrite.container.Group(class_='event', id=event_id)

        label_height = int(math.floor(height))
        label_width = int(math.floor(width))
        flat_h = int(math.floor(.5 * label_width))
        c_x = label_width - flat_h
        c_y = int(math.floor(label_height))

        commands = [
            'M 0 0',
            'h {}'.format(flat_h),
            'c {} 0 {} {} {} {}'.format(c_x, c_x, c_y, (label_width - flat_h), label_height),
            'h -{}'.format(label_width),
            'v -{}'.format(label_height)
        ]

        shape_path = svgwrite.path.Path(commands, fill=primary_color, stroke=secondary_color, stroke_width='2px')

        text_commands = [
            'M {} 0'.format(flat_h),
            'c {} 0 {} {} {} {}'.format(c_x, c_x, c_y, (label_width - flat_h), label_height),
            'h -{}'.format(label_width),
            'v -{}'.format(label_height)
        ]

        text_path = svgwrite.path.Path(text_commands, id='textCurve', fill=primary_color)

        figure_style = '''
        fill: {};
        font-size: {};
        font-family: {};
        '''.format(secondary_color, Report._number_to_px(.66 * label_height), figure_font)
        text_figure_x = Report._number_to_px(.4 * label_width)
        text_figure_y = Report._number_to_px(.5 * label_height)
        text_figure = svgwrite.text.Text(event_figure, textLength=Report._number_to_px(.66 * label_width),
                                         x=[text_figure_x], y=[text_figure_y], dominant_baseline='central',
                                         text_anchor='middle', style=figure_style.replace('\n', '').replace(' ', ''))

        name_style = '''
        fill: {};
        font-size: {};
        stroke: {};
        font-family: {};
        font-weight: bold;
        stroke-width: 1px;
        stroke-linecap: butt;
        stroke-linejoin: miter;
        letter-spacing: -2px;
        '''.format(primary_color, Report._number_to_px(.25 * label_height), secondary_color, text_font)
        text_group = svgwrite.text.Text('', style=name_style.replace('\n', '').replace(' ', ''))
        text_name = svgwrite.text.TextPath('#textCurve', event_name.upper())
        text_group.add(text_name)

        group.add(text_path)
        group.add(shape_path)
        group.add(text_figure)
        group.add(text_group)

        return group, (label_width, label_height)

    @staticmethod
    def _make_stat_label(stat_id, stat_name, stat_figure, stat_rank, width, height, figure_font, text_font,
                         primary_color, secondary_color):
        group = svgwrite.container.Group(id=stat_id, class_='stat')

        label_height = height
        label_width = width

        r = .5 * label_height
        x = math.floor(r)
        y = 0.

        circle_x = Report._number_to_px(x)
        circle_y = Report._number_to_px(y)
        circle_r = Report._number_to_px(r)
        stroke_w = Report._number_to_px(.1 * label_height)

        circle_el = svgwrite.shapes.Circle(center=(circle_x, circle_y), r=circle_r, stroke_width=stroke_w,
                                           stroke=secondary_color, fill=primary_color)

        figure_style = '''
        fill: {};
        font-size: {};
        font-family: {};
        '''.format(secondary_color, Report._number_to_px(.5 * label_height), figure_font)
        text_figure_el = svgwrite.text.Text(stat_figure, x=[circle_x], y=[circle_y],
                                            style=figure_style.replace(' ', '').replace('\n', ''),
                                            text_anchor='middle', dominant_baseline='central',
                                            textLength=Report._number_to_px(.66 * label_height))

        commands = [
            'M {} {}'.format(x, math.floor(r * math.sin(math.atan(1)))),
            'h {}'.format(math.floor(label_width - 2 * r)),
            'v {}'.format(-math.floor(r)),
            'L {} {}'.format(math.floor(label_width - 2 * r), math.floor(r * math.sin(-math.atan(1)))),
            'h {}'.format(-math.floor(label_width - 3 * r))
        ]

        shape_el = svgwrite.path.Path(commands, fill=secondary_color)

        shape_width = label_width - 2 * r
        name_x = Report._number_to_px(.5 * (label_width + r))
        name_y = Report._number_to_px(0)
        name_style = '''
        fill: {};
        font-size: {};
        font-family: {};
        '''.format(primary_color, Report._number_to_px(.33 * label_height), text_font)
        text_name_el = svgwrite.text.Text(stat_name, x=[name_x], y=[name_y],
                                          style=name_style.replace(' ', '').replace('\n', ''), text_anchor='middle',
                                          dominant_baseline='central',
                                          textLength=Report._number_to_px(.75 * shape_width))

        rect_height = Report._number_to_px(r)
        rect_width = Report._number_to_px(r)
        rect_x = Report._number_to_px(label_width - r)
        rect_y = Report._number_to_px(r * (math.sin(math.atan(1)) - 1))
        rect_el = svgwrite.shapes.Rect(size=(rect_width, rect_height), insert=(rect_x, rect_y), fill=primary_color)

        rank_style = '''
        fill: {};
        font-size: {};
        font-family: {};
        '''.format(secondary_color, Report._number_to_px(.5 * r), figure_font)
        rank_x = Report._number_to_px(label_width - .5 * r)
        rank_y = Report._number_to_px(r * (math.sin(math.atan(1)) - 1) + .5 * r)
        text_rank_el = svgwrite.text.Text(stat_rank, x=[rank_x], y=[rank_y],
                                          style=rank_style.replace(' ', '').replace('\n', ''), text_anchor='middle',
                                          dominant_baseline='central', textLength=Report._number_to_px(.75 * r))

        group.add(shape_el)
        group.add(circle_el)
        group.add(text_figure_el)
        group.add(text_name_el)
        group.add(rect_el)
        group.add(text_rank_el)

        return group, (width, height)

    @staticmethod
    def _make_summary_label(season_entity, summary, width, height, figure_font, text_font, primary_color,
                            secondary_color, translations):
        group = svgwrite.container.Group(id='summary', class_='summary')

        label_height = height
        label_width = width

        season_width = int(math.floor(.25 * label_width))
        season_height = int(math.floor(.2 * label_height))
        season_el = svgwrite.shapes.Rect(size=(season_width, season_height), fill=secondary_color)

        season_style = '''
        fill: {};
        font-size: {};
        font-family: {};
        '''.format(primary_color, Report._number_to_px(.75 * season_height), text_font)
        season_name = season_entity['informations']['name']
        season_name_x = Report._number_to_px(.5 * season_width)
        season_name_y = Report._number_to_px(.5 * season_height)
        season_name_el = svgwrite.text.Text(season_name, style=season_style.replace(' ', '').replace('\n', ''),
                                            x=[season_name_x], y=[season_name_y], text_anchor='middle',
                                            dominant_baseline='central')

        nb_games_width = int(math.floor(.2 * label_width))
        nb_games_height = int(math.floor(.4 * label_height))
        nb_games_x = 0
        nb_games_y = season_height
        nb_games_el = svgwrite.shapes.Rect(insert=(nb_games_x, nb_games_y), size=(nb_games_width, nb_games_height),
                                           fill=secondary_color)

        nb_games_name_width = int(math.floor(.8 * label_width))
        nb_games_name_height = int(math.floor(.4 * label_height))
        nb_games_name_x = nb_games_width
        nb_games_name_y = season_height
        nb_games_name_el = svgwrite.shapes.Rect(insert=(nb_games_name_x, nb_games_name_y),
                                                size=(nb_games_name_width, nb_games_name_height), fill=primary_color,
                                                stroke=secondary_color,
                                                stroke_width=Report._number_to_px(.1 * nb_games_name_height))

        nb_start_width = int(math.floor(.5 * label_width))
        nb_start_height = int(math.floor(.4 * label_height))
        nb_start_x = nb_start_width
        nb_start_y = season_height + nb_games_height
        nb_start_el = svgwrite.shapes.Rect(insert=(nb_start_x, nb_start_y), size=(nb_start_width, nb_start_height),
                                           fill=secondary_color)

        nb_sub_width = int(math.floor(.5 * label_width))
        nb_sub_height = int(math.floor(.4 * label_height))
        nb_sub_x = 0
        nb_sub_y = season_height + nb_games_height
        nb_sub_el = svgwrite.shapes.Rect(insert=(nb_sub_x, nb_sub_y), size=(nb_sub_width, nb_sub_height),
                                         fill=secondary_color)

        group.add(season_el)
        group.add(season_name_el)
        group.add(nb_games_el)
        group.add(nb_games_name_el)
        group.add(nb_start_el)
        group.add(nb_sub_el)

        for summary_key, summary_value in summary.items():
            current_name = Report._name_from_translations(summary_key, translations)
            if summary_key == 'nb_games_played':
                nb_games_fig_x = Report._number_to_px(nb_games_x + .5 * nb_games_width)
                nb_games_fig_y = Report._number_to_px(nb_games_y + .5 * nb_games_height)
                nb_games_style = '''
                fill: {};
                font-size: {};
                font-family: {};
                '''.format(primary_color, Report._number_to_px(.75 * nb_games_height), figure_font)
                nb_games_fig_el = svgwrite.text.Text(summary_value, x=[nb_games_fig_x], y=[nb_games_fig_y],
                                                     text_anchor='middle', dominant_baseline='central',
                                                     style=nb_games_style.replace(' ', '').replace('\n', ''))
                group.add(nb_games_fig_el)

                nb_games_name_txt_x = Report._number_to_px(nb_games_name_x + .5 * nb_games_name_width)
                nb_games_name_txt_y = Report._number_to_px(nb_games_name_y + .5 * nb_games_name_height)
                nb_games_text = '''
                fill: {};
                font-size: {};
                font-family: {};
                '''.format(secondary_color, Report._number_to_px(.75 * nb_games_height), text_font)
                nb_games_name_text_el = svgwrite.text.Text(current_name.upper(), x=[nb_games_name_txt_x],
                                                           y=[nb_games_name_txt_y], text_anchor='middle',
                                                           dominant_baseline='central',
                                                           style=nb_games_text.replace(' ', '').replace('\n', ''))
                group.add(nb_games_name_text_el)
            elif summary_key == 'nb_games_started':
                nb_games_fig_x = Report._number_to_px(nb_start_x + .5 * nb_start_width)
                nb_games_fig_y = Report._number_to_px(nb_start_y + .5 * nb_start_height)
                nb_games_style = '''
                fill: {};
                font-size: {};
                font-family: {};
                '''.format(primary_color, Report._number_to_px(.5 * nb_start_height), text_font)
                nb_games_fig_el = svgwrite.text.Text('{} {}'.format(str(summary_value), current_name.lower()),
                                                     x=[nb_games_fig_x], y=[nb_games_fig_y], text_anchor='middle',
                                                     dominant_baseline='central',
                                                     style=nb_games_style.replace(' ', '').replace('\n', ''))
                group.add(nb_games_fig_el)
            else:
                nb_games_fig_x = Report._number_to_px(nb_sub_x + .5 * nb_sub_width)
                nb_games_fig_y = Report._number_to_px(nb_sub_y + .5 * nb_sub_height)
                nb_games_style = '''
                fill: {};
                font-size: {};
                font-family: {};
                '''.format(primary_color, Report._number_to_px(.5 * nb_sub_height), text_font)
                nb_games_fig_el = svgwrite.text.Text('{} {}'.format(str(summary_value), current_name.lower()),
                                                     x=[nb_games_fig_x], y=[nb_games_fig_y], text_anchor='middle',
                                                     dominant_baseline='central',
                                                     style=nb_games_style.replace(' ', '').replace('\n', ''))
                group.add(nb_games_fig_el)

        return group, (width, height)

    def to_svg(self, width, height, main_font, figure_font, title_font, primary_color, secondary_color):
        raise NotImplementedError('Report class is an abstract class')
