from xml.dom import minidom
from html import unescape


def prettyXML(filePath):
    xml = open(filePath, 'r', encoding='utf-8').read()
    xml = minidom.parseString(xml)
    xml = xml.toprettyxml()
    xml = unescape(xml)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.writelines(xml)
    return xml
