from pathlib import Path
import xml.etree.ElementTree as ET
import requests
from typing import List, Tuple


class Filter:
    """Class for filtering xmls based on passed params.
    """

    # remaining is to handle unioon of combinations when many process types or inputs are given
    def __init__(self, params: List[str]):
        self.params = params
        self.udf_tag = '{http://genologics.com/ri/userdefined}field'
        self.related_entity_tags = ['project', 'submitter', 'artifact', 'reagent-label']  # handlde these

    def _parse(self, root: ET.Element) -> List[Tuple[str, str]]:
        """Parsing xml to prepare for filtering.

        Work In Progress!!!!!!!!"""

        parsed_xml = []
        for child in root.iter():
            if child.tag == self.udf_tag:
                udf = child.attrib.get('name')
                parsed_xml.append((f"udf.{udf}", child.text))
            elif child.tag in self.related_entity_tags:
                continue
            elif child.tag == 'input':
                parsed_xml.append(('inputartifactlimsid', child.attrib.get('limsid')))
            elif child.tag == 'parent-process':
                uri = child.attrib.get('uri')
                r = requests.get(uri)
                if not r.content:
                    # warn about missing process file??
                    continue
                tree = ET.fromstring(r.content)
                parsed_xml.append(('process-type', tree.findall('type')[0].text))
            elif child.tag == 'sample':
                parsed_xml.append(('samplelimsid', child.attrib.get('limsid')))
            else:
                parsed_xml.append((child.tag, child.text))
        return parsed_xml

    def _filter(self, root: ET.Element) -> bool:
        """Checking if the filtering parameters are a subset of the parsed xml."""

        parsed_xml = self._parse(root)
        if set(self.params) <= set(parsed_xml):
            return True
        return False

    def make_entity_xml(self, entity_type: dict, base_uri: str, db: dict) -> str:
        """Formatting the entity xml response based existing entities in the database
        filtered by the filtering params.

        Example of entity xml for artifacts:

        <art:artifacts xmlns:art="http://genologics.com/ri/artifact">
        <artifact limsid="2-1000001" uri="http://127.0.0.1:8000/api/v2/artifacts/2-1000001"/>
        <artifact limsid="2-1000002" uri="http://127.0.0.1:8000/api/v2/artifacts/2-1000002"/>
        <artifact limsid="2-1000003" uri="http://127.0.0.1:8000/api/v2/artifacts/2-1000003"/>
        <artifact limsid="2-1000004" uri="http://127.0.0.1:8000/api/v2/artifacts/2-1000004"/>
        </art:artifacts>
        """

        entitiy_xml = [
            f'<smp:{entity_type["plur"]} xmlns:smp="http://genologics.com/ri/{entity_type["sing"]}">']

        for entity_id, xml_content in db[entity_type["plur"]].items():
            root = ET.fromstring(xml_content)
            if self._filter(root):
                path = f'<{entity_type["sing"]} uri="{base_uri}/api/v2/{entity_type["plur"]}/{entity_id}" limsid="{entity_id}"/>'
                entitiy_xml.append(path)

        entitiy_xml.append(f'</smp:{entity_type["plur"]}>')

        return '\n'.join(entitiy_xml)
