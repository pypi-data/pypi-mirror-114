import bestOf.backend.evaluateSharpness as evaluateSharpness
import bestOf.backend.evaluateCentering as evaluateCentering
import bestOf.backend.evaluateLighting as evaluateLighting
import bestOf.backend.evaluateResolution as evaluateResolution


def create_sharpness_map(images, image_info, groups, progress_func, progress, max_progress):
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
            sharpness_map[index] = group_sharpness_scores[idx_in_group] + \
                (avg_subject_sharpness_scores[idx_in_group] / 2)

    return sharpness_map, progress


def create_centering_map(image_info, groups, progress_func, progress, max_progress):
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
            centering_map[index] = group_centering_scores[idx_in_group]

    return centering_map, progress


def create_lighting_map(image_info, groups, progress_func, progress, max_progress):
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
            lighting_map[index] = avg_subject_lighting_scores[idx_in_group]

    return lighting_map, progress
