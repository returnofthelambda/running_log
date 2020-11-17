# clean the XML files imported from a Garmin Forefunner
# first pull files via...
# then run garmin_dump xxx.gmn > xxx.xml

# to clean XML file:
# 1) remove all lines starting with <track>
# 2) remove line 2 <laps .. />
# 3) move </run> (should be line 2 now) to end of file
import xml.etree.ElementTree as ET


def clean(pth):
    tree = ET.parse(pth)
    root = tree.getroot()

    i = 0
    data = []
    points = []
    for child in root:
        if str(child.tag) == 'lap':
            i += 1
            subls = []
            for chiles in child:  # .getchildren():
                # print(chiles.tag)
                if (chiles.tag == 'begin_pos') or (chiles.tag == 'end_pos'):
                    subls.append(chiles.attrib)
                elif chiles.tag == 'unknown':
                    next  # skip
                else:
                    subls.append(chiles.text)

            data.append([str(child.tag) + str(i), child.attrib['start'],
                         child.attrib['duration'], child.attrib['distance'],
                         child.attrib['trigger'], subls])
        elif str(child.tag) == 'point':
            points.append(child.attrib)

    return data, points
