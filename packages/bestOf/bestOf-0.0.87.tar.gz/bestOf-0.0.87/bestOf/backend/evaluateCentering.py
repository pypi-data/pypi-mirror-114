import math


def euclidean(coord1, coord2, y_modifier=3):
    return math.sqrt(((coord1[0] - coord2[0]) ** 2) + (((coord1[1] - coord2[1]) / y_modifier) ** 2))


def evaluate_centering(bounds_list, image):
    im_height, im_width, _ = image.shape
    center = (im_width / 2, im_height / 2)
    total_dist = 0

    # print(bounds_list)

    for bounds in bounds_list:
        x, y, w, h = int(bounds.xmin * im_width), int(bounds.ymin * im_height), int(
            bounds.width * im_width), int(bounds.height * im_height)
        coord = (x + w, y + h)
        dist = euclidean(coord, center)
        total_dist += dist

    # print('Total', total_dist)

    max_dist = math.sqrt((center[0] ** 2) + (center[1] ** 2))
    # print('Max', max_dist)

    return (max_dist - (total_dist / len(bounds_list))) / max_dist if len(bounds_list) and max_dist else None


def normalize_centering_scores(group_scores):
    max_val = max(group_scores)

    if not max_val:
        return [1.0] * len(group_scores)

    normalized_scores = [float(score) / float(max_val)
                         for score in group_scores]
    return normalized_scores
