import os
import argparse
from xml.etree import ElementTree

def convert_to_yolo(xml_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith('.xml'):
            tree = ElementTree.parse(os.path.join(xml_folder, xml_file))
            root = tree.getroot()

            size = root.find('size')
            image_width = int(size.find('width').text)
            image_height = int(size.find('height').text)

            yolo_annotations = []
            for obj in root.findall('object'):
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)

                x_center = (xmin + xmax) / 2
                y_center = (ymin + ymax) / 2
                width = xmax - xmin
                height = ymax - ymin

                x_center_normalized = x_center / image_width
                y_center_normalized = y_center / image_height
                width_normalized = width / image_width
                height_normalized = height / image_height

                yolo_annotations.append(f"0 {x_center_normalized} {y_center_normalized} {width_normalized} {height_normalized}")

            with open(os.path.join(output_folder, os.path.splitext(xml_file)[0] + '.txt'), 'w') as f:
                f.write("\n".join(yolo_annotations))

    print("Successfully converted!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert XML annotations to YOLO format')
    parser.add_argument('--xml_folder', type=str, required=True, help='Path to the folder containing XML files')
    parser.add_argument('--output_folder', type=str, required=True, help='Path to the folder to save YOLO format annotations')

    args = parser.parse_args()
    
    convert_to_yolo(args.xml_folder, args.output_folder)
