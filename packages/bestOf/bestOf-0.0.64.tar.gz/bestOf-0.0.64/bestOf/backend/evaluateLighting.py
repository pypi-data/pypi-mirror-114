import mediapipe as mp
import math
import cv2 as cv
import numpy as np
import identifyPeople
import evaluateCentering

FACE_MESH_CREATOR = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)


def create_mesh(sub):
    results = FACE_MESH_CREATOR.process(sub)
    return results.multi_face_landmarks


def gaussian_illumination_on_full_subject(image):
    mean, l_vals = pure_luminance_analysis(image)
    stdev = math.sqrt(sum((i - mean) ** 2 for i in l_vals) / len(l_vals))

    probabilities = []
    for x in l_vals:
        factor = 1 / (stdev * math.sqrt(2 * math.pi))
        exp = -1 * ((x - mean) ** 2) / (2 * (stdev ** 2))
        probabilities.append(factor * (math.e ** exp))

    return sum(probabilities) / len(probabilities)


def pure_luminance_analysis(image):
    l_vals = []
    image = cv.cvtColor(image, cv.COLOR_RGB2HLS)
    for row in image:
        for pixel in row:
            luminance = pixel[1]
            l_vals.append(luminance)
    mean = sum(l_vals) / len(l_vals)
    return mean, l_vals


def evaluate_lighting_in_region(pixels):
    pass


def split_face(face, num_regions=8):
    pass


def collect_regions(landmarks):
    for landmark in landmarks:
        coord1 = (landmark.x, landmark.y)
        # max dist is sqrt(2), so initialize to an arbitrary number larger than sqrt(2)
        min_dist = 2
        min_dist_2 = 2
        min_dist_landmark = None
        min_dist_landmark_2 = None
        for other in landmarks:
            if landmark != other:
                coord2 = (other.x, other.y)
                dist = evaluateCentering.euclidean(coord1, coord2)
                pass


def evaluate_lighting(image):
    return pure_luminance_analysis(image)[0]


if __name__ == '__main__':
    subs, _ = identifyPeople.crop_subjects(identifyPeople.read_img(
        './bestOf/resources/examples/dark.jpg'))

    x, _ = pure_luminance_analysis(subs[0])
    print(x)

    subs, _ = identifyPeople.crop_subjects(identifyPeople.read_img(
        './bestOf/resources/examples/bright.jpg'))

    x, _ = pure_luminance_analysis(subs[0])
    print(x)

    # print(create_mesh(subs[0]))
