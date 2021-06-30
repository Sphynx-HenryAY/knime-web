def knime_xml_lookup(
	path_xml,
	name_file,
	*keys
):

	from xml.etree import ElementTree
	from pathlib import Path

	from dotenv import get_key
	path_workspace = get_key( ".env", "WORKSPACE_PATH" )

	tree = ElementTree.parse(
		Path( path_workspace, path_xml, name_file )
	)
	root = tree.getroot()

	keys = list(keys)

	while keys:
		key = keys.pop(0)
		for node in root:
			if node.attrib.get( "key" ) == key:
				root = node
				continue
	else:
		return root.attrib.get( "value" )

def node_lookup( path_xml, *keys ):
	return knime_xml_lookup( path_xml, "settings.xml", *keys )

def workflow_lookup( path_xml, *keys ):
	return knime_xml_lookup( path_xml, "workflow.knime", *keys )
