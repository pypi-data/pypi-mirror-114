import bestOf.backend.evaluateSharpness as evaluateSharpness
import bestOf.backend.evaluateCentering as evaluateCentering
import bestOf.backend.evaluateLighting as evaluateLighting
import bestOf.backend.evaluateResolution as evaluateResolution

import collections


def create_sharpness_map(images, image_info, groups, weight, progress_func, progress, max_progress):
    sharpness_scores = []

    for idx, image in enumerate(images):
        sharpness_scores.append(evaluateSharpness.evaluate_sharpness(
            image))
        progress += 1
        progress_func("sharpness", image_info[idx][1], int(
            progress / max_progress * 100))
    # index to normalized sharpness score + half of normalized subject sharpness score
    sharpness_map = {}
    for group in groups:
        group_sharpness_scores = []
        for index in group:
            for pos, item in enumerate(image_info):
                if item[0] == index:
                    group_sharpness_scores.append(
                        sharpness_scores[pos])
                    break
            progress += 1
            progress_func("sharpness", image_info[pos][1], int(
                progress / max_progress * 100))
        group_sharpness_scores = evaluateSharpness.normalize_sharpness_scores(
            group_sharpness_scores)

        avg_subject_sharpness_scores = []
        for index in group:
            for pos, item in enumerate(image_info):
                if item[0] == index:
                    subject_sharpness_scores = item[3]
                    if not len(subject_sharpness_scores):
                        avg_subject_sharpness_scores.append(0)
                        continue

                    avg_subject_sharpness_scores.append(
                        sum(subject_sharpness_scores) / len(subject_sharpness_scores))
            progress += 1
            progress_func("sharpness", image_info[pos][1], int(
                progress / max_progress * 100))
        avg_subject_sharpness_scores = evaluateSharpness.normalize_sharpness_scores(
            avg_subject_sharpness_scores)

        for idx_in_group, index in enumerate(group):
            sharpness_map[index] = weight * (group_sharpness_scores[idx_in_group] + (
                avg_subject_sharpness_scores[idx_in_group] / 2))

    return sharpness_map, progress


def create_centering_map(image_info, groups, weight, progress_func, progress, max_progress):
    centering_map = {}

    for group in groups:
        group_centering_scores = []
        for index in group:
            for pos, item in enumerate(image_info):
                if item[0] == index:
                    group_centering_scores.append(image_info[pos][4])
                    break
            progress += 1
            progress_func("centering", image_info[pos][1], int(
                progress / max_progress * 100))
        print(group_centering_scores)
        group_centering_scores = evaluateCentering.normalize_centering_scores(
            group_centering_scores)

        for idx_in_group, index in enumerate(group):
            centering_map[index] = weight * \
                group_centering_scores[idx_in_group]

    return centering_map, progress


def create_lighting_map(image_info, groups, weight, progress_func, progress, max_progress):
    lighting_map = {}
    for group in groups:
        avg_subject_lighting_scores = []
        for index in group:
            for pos, item in enumerate(image_info):
                if item[0] == index:
                    subject_lighting_scores = item[5]
                    if not len(subject_lighting_scores):
                        avg_subject_lighting_scores.append(0)
                        continue

                    avg_subject_lighting_scores.append(
                        sum(subject_lighting_scores) / len(subject_lighting_scores))
            progress += 1
            progress_func("lighting", image_info[pos][1], int(
                progress / max_progress * 100))
        avg_subject_lighting_scores = evaluateLighting.normalize_lighting_scores(
            avg_subject_lighting_scores)

        for idx_in_group, index in enumerate(group):
            lighting_map[index] = weight * \
                avg_subject_lighting_scores[idx_in_group]

    return lighting_map, progress


def create_resolution_map(images, image_info, groups, weight, progress_func, progress, max_progress):
    resolution_scores = []
    resolution_map = {}

    for idx, image in enumerate(images):
        resolution_scores.append(evaluateResolution.evaluate_resolution(
            image))
        progress += 1
        progress_func("resolution", image_info[idx][1], int(
            progress / max_progress * 100))

    for group in groups:
        group_resolution_scores = []
        for index in group:
            for pos, item in enumerate(image_info):
                if item[0] == index:
                    group_resolution_scores.append(
                        resolution_scores[pos])
                    break
            progress += 1
            progress_func("resolution", image_info[pos][1], int(
                progress / max_progress * 100))
        group_resolution_scores = evaluateResolution.normalize_resolution_scores(
            group_resolution_scores)

        for idx_in_group, index in enumerate(group):
            resolution_map[index] = weight * \
                group_resolution_scores[idx_in_group]
    return resolution_map, progress


def create_total_score_map(image_info, sharpness_map, centering_map, lighting_map, resolution_map):
    overall_score_map = collections.Counter(sharpness_map) + collections.Counter(
        centering_map) + collections.Counter(lighting_map) + collections.Counter(resolution_map)

    overall_score_map = dict(overall_score_map)

    if not len(overall_score_map.keys()):
        for item in image_info:
            overall_score_map[item[0]] = item[2]
        return overall_score_map

    for item in image_info:
        overall_score_map[item[0]] += item[2]

    return overall_score_map
