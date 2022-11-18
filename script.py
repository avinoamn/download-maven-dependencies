import sys
import os
import subprocess
import shutil
import uuid

def main(argv):
	"""Download Maven dependencies tree.

    Keyword arguments:
    argv[0] -- the pom.xml path
    argv[1] -- the output dir path of the downloaded dependencies
    """
	pom_xml_path = argv[0]
	output_dir_path = argv[1]

	temp_dir_path = create_uuid_dir('temp')
	output_tree_dir_path = create_uuid_dir('tree', output_dir_path)

	settings_xml_path = create_maven_settings_xml(temp_dir_path, output_tree_dir_path)

	download_dependencies(settings_xml_path, pom_xml_path, temp_dir_path)

	cleanup(temp_dir_path)

def download_dependencies(settings_xml_path, pom_xml_path, temp_dir_path):
	print('downloading dependencies')
	subprocess.call(r'mvn dependency:go-offline -s {} -f {}'.format(settings_xml_path, pom_xml_path), cwd=temp_dir_path, shell=True)
	print('finished downloading dependencies')

def create_uuid_dir(name, path=None):
	if path is None:
		path = os.path.dirname(os.path.realpath(__file__))

	dir_path = os.path.join(path, '{}-{}'.format(name, str(uuid.uuid4())[:4]))

	if not os.path.exists(dir_path):
			os.makedirs(dir_path)

	return dir_path

def create_maven_settings_xml(temp_dir_path, output_tree_dir_path):
	with open('settings.xml', 'r') as settings_file:
		settings_xml_data = settings_file.read().format(output_tree_dir_path)
		settings_xml_path = os.path.join(temp_dir_path, 'settings.xml')
		
		with open(settings_xml_path, 'w') as settings_xml:
			settings_xml.write(settings_xml_data)
		
		return settings_xml_path

def cleanup(temp_dir_path):
	shutil.rmtree(temp_dir_path)

if __name__ == '__main__':
	main(sys.argv[1:])
	