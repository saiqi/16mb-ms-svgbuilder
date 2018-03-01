import math
import re
import json
import html
import textwrap

from nameko.rpc import rpc
from lxml import etree
from jsonpath_rw import parser


class SvgBuilderError(Exception):
    pass


class SvgBuilderService(object):

    name = 'svg_builder'

    @staticmethod
    def _handle_text_length(node, text):
        if len(text) < 35:
            node.text = text
        else:
            node.text = None
            break_text = textwrap.fill(text, width=35)

            x = node.attrib['x']
            y = node.attrib['y']

            cpt = 0
            for t in break_text.split('\n'):
                tspan_node = etree.Element('tspan', nsmap = {'svg': 'http://www.w3.org/2000/svg'})
                tspan_node.attrib['x'] = x
                if cpt > 0:
                    tspan_node.attrib['dy'] = "1em"
                else:
                    tspan_node.attrib['dy'] = "0"
                tspan_node.text = t
                cpt += 1

                node.append(tspan_node)

    @staticmethod
    def _format_float(value):
        if type(value) != float:
            return value

        split = math.modf(value)

        if split[1] < 10 and split[0] > 0:
            return round(value, 2)

        return round(value)

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

            current_value = SvgBuilderService._format_float(values[0].value)

            if 'percentage' in n.attrib:
                percentage_path = parser.parse(n.get('percentage'))
                is_percentage = percentage_path.find(results)

                if len(is_percentage) != 1:
                    raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(n.get('percentage')))

                if is_percentage[0].value is True:
                    text = str(100*current_value) + '%'
                else:
                    text = str(current_value)
            else:
                text = str(current_value)

            if has_tpan is True:
                spans[0].text = text
            else:
                SvgBuilderService._handle_text_length(n, text)

    @staticmethod
    def _handle_images(nodes, results):
        for n in nodes:
            path = parser.parse(n.get('content'))

            values = path.find(results)

            if 'isVectorial' not in n.attrib:
                raise SvgBuilderError('Picture node without any isVectorial attribute')

            is_svg = n.get('isVectorial') == 'true'

            if len(values) != 1:
                raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(n.get('content')))

            if is_svg is True:
                n.attrib['{http://www.w3.org/1999/xlink}href'] = 'data:image/svg+xml;utf8,' + html.escape(values[0].value)
            else:
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

            is_inverted = False
            if 'origin' in n.attrib:
                if n.get('origin') == 'end':
                    is_inverted = True

            value = values[0].value
            ref_value = ref_values[0].value

            ratio = 1
            if ref_value != 0:
                ratio = value/ref_value

            if is_inverted is False:
                angle = 2*math.pi*ratio
            else:
                angle = -2*math.pi*ratio
            is_large_arc = abs(angle) > math.pi

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
                computed_d.append('1' if is_inverted else '0')
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

            is_default = False

            try:
                color = color_mapping[value]
            except KeyError:
                try:
                    color = color_mapping[str(value)]
                except KeyError:
                    is_default = True
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

            if is_default is True and 'disappearDefault' in n.attrib and n.attrib['disappearDefault'] == 'true':
                n.attrib['style'] = '{};{}'.format(n.attrib['style'], 'display: none')

    @staticmethod
    def _handle_repeat(nodes, results):
        for n in nodes:
            if 'nRepeat' not in n.attrib:
                raise SvgBuilderError('No nRepeat attribute in repeat node')

            if 'xPosition' not in n.attrib or 'yPosition' not in n.attrib:
                raise SvgBuilderError('No xPosition or yPosition in repeat node')

            if 'xReference' not in n.attrib or 'yReference' not in n.attrib:
                raise SvgBuilderError('No xReference or yReference in repeat node')

            size = int(n.attrib['nRepeat'])
            xPosTemplate = n.attrib['xPosition']
            yPosTemplate = n.attrib['yPosition']
            xReference = int(n.attrib['xReference'])
            yReference = int(n.attrib['yReference'])

            try:
                template = n.xpath('//n:g[@class=\'template\']', namespaces={'n': 'http://www.w3.org/2000/svg'})[0]
            except:
                raise SvgBuilderError('No template element in repeat node')

            for i in range(size):
                new_node = etree.Element('{http://www.w3.org/2000/svg}g')
                current_x_path = parser.parse(xPosTemplate.replace('{{k0}}', str(i)).replace('{{k1}}', str(i+1)))
                current_y_path = parser.parse(yPosTemplate.replace('{{k0}}', str(i)).replace('{{k1}}', str(i+1)))

                try:
                    current_x_ratio = current_x_path.find(results)[0].value
                except:
                    raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(current_x_path))

                try:
                    current_y_ratio = current_y_path.find(results)[0].value
                except:
                    raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(current_y_path))

                current_x = current_x_ratio * xReference
                current_y = current_y_ratio * yReference

                new_node.set('transform', 'translate({},{})'.format(current_x, current_y))
                for c in template.getchildren():
                    el_str = etree.tostring(c).decode('utf-8').replace('{{k0}}', str(i)).replace('{{k1}}', str(i+1))
                    new_node.append(etree.fromstring(el_str.encode('utf-8')))
                n.append(new_node)

            n.remove(template)

    @staticmethod
    def _handle_resizeable(nodes, results):
        for n in nodes:
            if 'adjustSize' not in n.attrib:
                raise SvgBuilderError('No adjustSize attribute in resizeable node')

            current_coef_path = parser.parse(n.attrib['adjustSize'])

            try:
                current_coef = current_coef_path.find(results)[0].value
            except:
                raise SvgBuilderError('Too many or no values related to JSON Path {}'.format(current_coef_path))

            n.set('transform', 'scale({c},{c})'.format(c=current_coef))

    @rpc
    def replace_jsonpath(self, svg_string, results):
        root = etree.fromstring(svg_string.replace('\n', '').encode('utf-8'))

        repeat_nodes = root.xpath('//n:g[@class=\'repeat\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
        self._handle_repeat(repeat_nodes, results)

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

        resizeable_nodes = root.xpath('//n:g[@class=\'resizeable\']', namespaces={'n': 'http://www.w3.org/2000/svg'})
        self._handle_resizeable(resizeable_nodes, results)

        return etree.tostring(root).decode('utf-8')
