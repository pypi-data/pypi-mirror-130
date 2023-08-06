from eqlog.log import Logger
from eqlog.common import get_xml_path

xml_path = get_xml_path()

eqlog = Logger(config=xml_path)
