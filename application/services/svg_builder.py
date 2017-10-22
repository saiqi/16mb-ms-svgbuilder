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

            if len(spans) != 1:
                raise SvgBuilderError('Too many or no tspan tags related to text node')

            spans[0].text = str(values[0].value)

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

            width = float(n.get('width'))*ratio

            n.attrib['width'] = str(width)

    @rpc
    def replace_jsonpath(self, svg_string, results):
        root = etree.fromstring(svg_string.replace('\n', '').encode('utf-8'))

        text_nodes = root.xpath('//n:text[@content]', namespaces={'n': 'http://www.w3.org/2000/svg'})
        self._handle_text_tag(text_nodes, results)

        rect_nodes = root.xpath('//n:rect[@currentValue]', namespaces={'n': 'http://www.w3.org/2000/svg'})
        self._handle_rect(rect_nodes, results)

        return etree.tostring(root).decode('utf-8')
