import math
import svgwrite.container
import svgwrite.shapes
import svgwrite.text
import svgwrite.image
import svgwrite.path

from application.services.reports.report import Report


class PlayerNewsReport(Report):
    def __init__(self, title, background, player_picture, season_picture, competition_picture, season_entity,
                 player_entity, summary, events, stats):
        self.title = title
        self.background = background
        self.player_picture = player_picture
        self.season_picture = season_picture
        self.competition_picture = competition_picture
        self.season_entity = season_entity
        self.player_entity = player_entity
        self.summary = summary
        self.events = events
        self.stats = stats

    def to_svg(self, width, height, main_font, figure_font, title_font, primary_color, secondary_color):
        dwg = svgwrite.Drawing(size=(str(width) + 'px', str(height) + 'px'))

        border_el = svgwrite.shapes.Rect(size=(width, height), fill='white', stroke='black')
        dwg.add(border_el)

        if self.background:
            bg_width = self._number_to_px(width)
            bg_height = self._number_to_px(height)

            bg_el = svgwrite.image.Image(href='data:image/png;base64,{}'.format(self.background),
                                         size=(bg_width, bg_height), insert=('0px', '0px'))
            bg_el.stretch()

            dwg.add(bg_el)

        title_el, title_size = self._make_title(self.title, .75*width, .05*height, title_font, primary_color,
                                                secondary_color)

        dwg.add(title_el)

        entity_trans_x = 0
        entity_trans_y = int(math.floor(height*.2))
        entity_group = svgwrite.container.Group(class_='entity', id='entity',
                                                transform='translate({},{})'.format(entity_trans_x, entity_trans_y))
        entity_text_size = self._number_to_px(height*.1)
        entity_text_style = '''
        font-family: {};
        font-size: {};
        fill: {};
        stroke: {};
        stroke-width: 2px;
        stroke-linecap: butt;
        stroke-linejoin: miter;
        text-align:center;
        '''.format(main_font, entity_text_size, primary_color, secondary_color).replace('\n', '').replace(' ', '')

        entity_x = self._number_to_px(.5*.66*width)

        if self.player_entity['informations']['nickname']:
            nickname = self.player_entity['informations']['nickname']
            entity_text_el = svgwrite.text.Text(nickname.upper(), x=[entity_x], y=['0px'], fill=secondary_color,
                                                dominant_baseline='central',
                                                textLength=self._number_to_px(.66*width), style=entity_text_style)
            entity_group.add(entity_text_el)
        else:
            first_name = self.player_entity['informations']['first_name']
            last_name = self.player_entity['informations']['last_name']

            first_name_text_el = svgwrite.text.Text(first_name, x=[entity_x], y=['0px'], fill=secondary_color,
                                                    dominant_baseline='central', text_anchor='middle',
                                                    style=entity_text_style)
            last_name_text_el = svgwrite.text.Text(last_name.upper(), x=[entity_x], y=[entity_text_size],
                                                   fill=secondary_color, dominant_baseline='central',
                                                   text_anchor='middle', style=entity_text_style)

            entity_group.add(first_name_text_el)
            entity_group.add(last_name_text_el)

        dwg.add(entity_group)

        for event in self.events:
            event_el, event_size = self._make_event_label(event['type'], event['name'], event['value'], .9*.1*height,
                                                          .1*height, figure_font, main_font, primary_color,
                                                          secondary_color)

            if event['type'] == 'nb_goals':
                event_dx = int(math.floor((.66 + 1./12.)*width - .5*event_size[0]))
                event_dy = int(math.floor(.175*height + .5*event_size[1]))
            else:
                event_dx = int(math.floor((.66 + 1./4.)*width) - .5*event_size[0])
                event_dy = int(math.floor(.175*height + .5*event_size[1]))
            event_el.translate(event_dx, event_dy)
            dwg.add(event_el)

        nb_stats = len(self.stats)
        stat_vpadding = 10
        stat_vshift = .5
        stat_height = .1*height if (1.-stat_vshift)*height / nb_stats > .1*height else (1.-stat_vshift)*height / nb_stats
        for i, stat in enumerate(self.stats):
            stat_el, stat_size = self._make_stat_label(stat['formula_id'], stat['name'].upper(),
                                                       math.floor(stat['value']), stat['rank'],
                                                       .33*width, stat_height, figure_font,
                                                       main_font, primary_color, secondary_color)
            stat_dx = int(math.floor(.66*width))
            stat_dy = int(math.floor(stat_vshift*height + i*(stat_height + stat_vpadding) - nb_stats*stat_vpadding))
            stat_el.translate(stat_dx, stat_dy)
            dwg.add(stat_el)

        summary_el, summary_size = self._make_summary_label(self.season_entity, self.summary, .33*width, .1*height,
                                                            figure_font, main_font, primary_color, secondary_color)
        summary_dx = int(math.floor(.66*width))
        summary_dy = int(math.floor(.075*height))
        summary_el.translate(summary_dx, summary_dy)
        dwg.add(summary_el)

        return dwg.tostring()
