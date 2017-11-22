import math
import re
import json

from nameko.rpc import rpc
from lxml import etree
from jsonpath_rw import parser


class SvgBuilderError(Exception):
    pass


class SvgBuilderService(object):

    name = 'svg_builder'

    @staticmethod
    def _handle_text_tag(nodes, results):
        for n in nodes:
            path = parser.parse(n.get('content'))

            values = path.find(results)

            if len(values) != 1:
                raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(n.get('content')))

            spans = n.xpath('./n:tspan', namespaces={'n': 'http://www.w3.org/2000/svg'})

            if len(spans) > 1:
                raise SvgBuilderError('Too many tspan tags related to text node')

            has_tpan = len(spans) > 0

            if 'percentage' in n.attrib:
                percentage_path = parser.parse(n.get('percentage'))
                is_percentage = percentage_path.find(results)

                if len(is_percentage) != 1:
                    raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(n.get('percentage')))

                if is_percentage[0].value is True:
                    text = str(round(100*values[0].value)) + '%'
                else:
                    text = str(round(values[0].value))
            else:
                text = str(values[0].value)

            if has_tpan is True:
                spans[0].text = text
            else:
                n.text = text

    @staticmethod
    def _handle_images(nodes, results):
        for n in nodes:
            path = parser.parse(n.get('content'))

            values = path.find(results)

            if len(values) != 1:
                raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(n.get('content')))

            n.attrib['{http://www.w3.org/1999/xlink}href'] = 'data:image/png;base64,' + values[0].value

    @staticmethod
    def _handle_rect(nodes, results):
        for n in nodes:
            value_path = parser.parse(n.get('currentValue'))
            ref_path = parser.parse(n.get('refValue'))

            values = value_path.find(results)

            if len(values) != 1:
                raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(n.get('currentValue')))

            ref_values = ref_path.find(results)

            if len(ref_values) != 1:
                raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(n.get('refValue')))

            value = values[0].value
            ref_value = ref_values[0].value

            ratio = 1
            if ref_value != 0:
                ratio = value/ref_value

            if value == 0:
                ratio = 0

            ref_width = float(n.get('width'))
            width = ref_width*ratio

            n.attrib['width'] = str(width)

            if n.get('origin'):
                origin = n.get('origin')
                if origin == 'end':
                    if n.get('x'):
                        ref_x = float(n.get('x'))
                        n.attrib['x'] = str(ref_x + (ref_width - width))

    @staticmethod
    def _handle_ellipse(nodes, results):
        for n in nodes:
            value_path = parser.parse(n.get('currentValue'))
            ref_path = parser.parse(n.get('refValue'))

            values = value_path.find(results)

            if len(values) != 1:
                raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(n.get('currentValue')))

            ref_values = ref_path.find(results)

            if len(ref_values) != 1:
                raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(n.get('refValue')))

            value = values[0].value
            ref_value = ref_values[0].value

            ratio = 1
            if ref_value != 0:
                ratio = value/ref_value

            angle = 2*math.pi*ratio
            is_large_arc = angle > math.pi

            d = n.get('d')
            try:
                arc_d = list(filter(lambda x: x!='', re.search(r'[A|a]([\d+.\-, ]+)', d).group(1).split(' ')))
                center_d = list(filter(lambda x: x!='', re.search(r'[M|m]([\d+.\-, ]+)', d).group(1).split(' ')))
            except:
                raise SvgBuilderError('Bad formated d attribute in path')

            start_x, start_y = map(float, center_d[0].split(','))
            radius_x, radius_y = map(float, arc_d[0].split(','))

            center_x = start_x
            center_y = start_y + radius_y

            x = center_x + radius_x*math.cos(angle - math.pi/2)
            y = center_y + radius_y*math.sin(angle - math.pi/2)

            dx = start_x - x
            dy = y - start_y

            if ratio == 1:
                n.tag = etree.QName('http://www.w3.org/2000/svg', 'circle')
                del n.attrib['d']
                n.attrib['cx'] = str(center_x)
                n.attrib['cy'] = str(center_y)
                n.attrib['r'] = str(radius_x)
            else:
                computed_d = list()
                computed_d.append('m')
                computed_d.append('{},{}'.format(start_x, start_y))
                computed_d.append('a')
                computed_d.append('{},{}'.format(radius_x, radius_y))
                computed_d.append('0')
                computed_d.append('1' if is_large_arc else '0')
                computed_d.append('0')
                computed_d.append('{},{}'.format(dx, dy))

                n.attrib['d'] = ' '.join(computed_d)

    @staticmethod
    def _handle_colors(nodes, results):
        for n in nodes:
            value_path = parser.parse(n.get('colorValue'))
            color_mapping = dict()
            for c in n.get('colorMapping').split(';'):
                k, v = c.split(':')
                color_mapping[k.strip()] = v.strip()

            values = value_path.find(results)

            if len(values) != 1:
                raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(n.get('colorValue')))

            value = values[0].value

            try:
                color = color_mapping[value]
            except KeyError:
                try:
                    color = color_mapping[str(value)]
                except KeyError:
                    color = color_mapping['default']

            if 'style' in n.attrib:
                styles = n.get('style').split(';')
                for s in styles:
                    prop = s.split(':')

                    if prop[0] == 'fill':
                        old_color = prop[1]
                        n.attrib['style'] = n.attrib['style'].replace(old_color, color)
            else:
                n.attrib['style'] = 'fill:{};'.format(color)

    @rpc
    def replace_jsonpath(self, svg_string, results):
        root = etree.fromstring(svg_string.replace('\n', '').encode('utf-8'))

        text_nodes = root.xpath('//n:text[@content]', namespaces={'n': 'http://www.w3.org/2000/svg'})
        self._handle_text_tag(text_nodes, results)

        rect_nodes = root.xpath('//n:rect[@currentValue]', namespaces={'n': 'http://www.w3.org/2000/svg'})
        self._handle_rect(rect_nodes, results)

        images_nodes = root.xpath('//n:image[@content]', namespaces={'n': 'http://www.w3.org/2000/svg'})
        self._handle_images(images_nodes, results)

        ellipse_nodes = root.xpath('//n:path[@currentValue and @class=\'ellipse\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
        self._handle_ellipse(ellipse_nodes, results)

        color_nodes = root.xpath('//*[@colorValue]')
        self._handle_colors(color_nodes, results)

        return etree.tostring(root).decode('utf-8')
