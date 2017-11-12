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

            ref_width = float(n.get('width'))
            width = ref_width*ratio

            n.attrib['width'] = str(width)

            if n.get('origin'):
                origin = n.get('origin')
                if origin == 'end':
                    if n.get('x'):
                        ref_x = float(n.get('x'))
                        n.attrib['x'] = ref_x + (ref_width - width)

    @rpc
    def replace_jsonpath(self, svg_string, results):
        root = etree.fromstring(svg_string.replace('\n', '').encode('utf-8'))

        text_nodes = root.xpath('//n:text[@content]', namespaces={'n': 'http://www.w3.org/2000/svg'})
        self._handle_text_tag(text_nodes, results)

        rect_nodes = root.xpath('//n:rect[@currentValue]', namespaces={'n': 'http://www.w3.org/2000/svg'})
        self._handle_rect(rect_nodes, results)

        images_nodes = root.xpath('//n:image[@content]', namespaces={'n': 'http://www.w3.org/2000/svg'})
        self._handle_images(images_nodes, results)

        return etree.tostring(root).decode('utf-8')
