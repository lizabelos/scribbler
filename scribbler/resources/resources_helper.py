import os
from os import listdir
from os.path import join, isfile
from random import randint

from PIL import Image
from lxml import etree

from scribbler.dataset import IAMHandwritingLineDataset

resource_paths = {}
resource_preloaded_image = {}
resource_preloaded_texts = {}


def list_resources(name):
    global resource_paths

    if not name in resource_paths:
        dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../resources/" + name)
        resource_paths[name] = [join(dir_name, f) for f in listdir(dir_name) if isfile(join(dir_name, f))]

    return resource_paths[name]


def preload_image_resources(name):
    global resource_preloaded_image

    if not name in resource_preloaded_image:
        resource = list_resources(name)
        resource_preloaded_image[name] = [Image.open(path).convert('RGB') for path in resource]

    return resource_preloaded_image[name]


def preload_text_ressources(name):
    global resource_preloaded_texts

    if not name in resource_preloaded_texts:
        resources = list_resources(name)
        resource_preloaded_texts[name] = []
        for resource in resources:
            tree = etree.parse(resource)
            root = tree.getroot()
            recursive_preload_text_ressources(name, root)

    return resource_preloaded_texts[name]


def recursive_preload_text_ressources(name, root):
    global resource_preloaded_texts

    title = root.tag.title()
    if title == "Text":
        resource_preloaded_texts[name].append(root.text)
    else:
        for children in root.getchildren():
            recursive_preload_text_ressources(name, children)


def count_resource(name):
    resource = list_resources(name)
    return len(resource)


def peak_resource(name, index):
    resource = list_resources(name)
    return resource[index]


def peak_random_resource(name):
    resource = list_resources(name)
    return resource[randint(0, len(resource) - 1)]


def peak_random_preloaded_image(name):
    resource = preload_image_resources(name)
    return resource[randint(0, len(resource) - 1)]


def peak_random_preloaded_text(name):
    resource = preload_text_ressources(name)
    return resource[randint(0, len(resource) - 1)]


def get_random_text(name, min_size=10, max_size=50):
    text = peak_random_preloaded_text(name)
    # text = "".join([c if self.labels.find(c) != -1 else "" for c in text])

    p = randint(0, len(text) // 2)
    return text[p:p+randint(min_size, max_size)]


def get_random_background(width, height):
    image = peak_random_preloaded_image("backgrounds")
    image_width, image_height = image.size
    x_crop = randint(0, max(1, image_width - width))
    y_crop = randint(0, max(1, image_height - height))
    return image.crop((x_crop, y_crop, x_crop + width, y_crop + height))


iam_handwriting_line_dataset_instance = None


def init_iam_handwriting_line_dataset(path):
    global iam_handwriting_line_dataset_instance
    iam_handwriting_line_dataset_instance = IAMHandwritingLineDataset(path)


def get_iam_handwriting_line_dataset_instance():
    global iam_handwriting_line_dataset_instance
    if iam_handwriting_line_dataset_instance is None:
        print("Please call init_iam_handwriting_line_dataset from scribbler.ressources.ressources_helper with the path of IAM dataset")
        assert iam_handwriting_line_dataset_instance is not None
    return iam_handwriting_line_dataset_instance
