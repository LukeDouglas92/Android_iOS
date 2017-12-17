import xml.etree.ElementTree as ET
tree = ET.parse('desktop/english.xml')
root = tree.getroot()
with open('desktop/NewEnglish.txt', 'w') as f:
    f.write('key = text')
for name in root.findall('name'):
    resources = resources.find('resources').find('name').text
    for mesh_heading in resources.find('name').findall('MeshHeading'):
        MeSH = mesh_heading.find('DescriptorName').text
        IsMajor = mesh_heading.find('DescriptorName').get('MajorTopicYN')
        line_to_write = ArticleID + '|' + CreatedDate + '|' + MeSH + '|' + IsMajor + '\n'
        with open('my_text_file.txt', 'a') as f:
            f.write(line_to_write)

