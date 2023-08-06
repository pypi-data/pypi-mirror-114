def evaluate_resolution(image):
    return image.shape[0] * image.shape[1]


def normalize_resolution_scores(group_scores):
    max_val = max(group_scores)

    if not max_val:
        return [1.0] * len(group_scores)

    normalized_scores = [float(score) / float(max_val)
                         for score in group_scores]
    return normalized_scores
