import cv2 as cv
import mediapipe as mp
from matplotlib import pyplot as plt
import numpy as np


FACE_DETECTOR = mp.solutions.face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.7)


def array_is_subset(superarray, subarray):
    return set(np.unique(subarray)).issubset(set(np.unique(superarray)))


def read_img(filename):
    return plt.imread(filename)


def save_img(filename, img):
    cv.imwrite(filename, img)


def save_img_colored(filename, img):
    cv.imwrite(filename, cv.cvtColor(img, cv.COLOR_RGB2BGR))


def show_img(image):
    cv.imshow('Image', image)
    cv.waitKey(0)


def detect_faces(image):
    if image is None:
        raise Exception('No image found.')

    return FACE_DETECTOR.process(image).detections


def crop_subjects_from_segmented_image(image, n=8):
    im_height, im_width, _ = image.shape

    delta_h = int(im_height / n)
    delta_w = int(im_width / n)

    print(delta_h, delta_w)

    all_subjects = []
    all_bounds = []

    for i in range(n):
        for j in range(n):
            seg = image[int(i * delta_h):int((i + 1) * delta_h),
                        int(j * delta_w):int((j + 1) * delta_w)]
            subs, bounds_list = crop_subjects(np.copy(seg, order='K'))
            for bounds in bounds_list:
                bounds.xmin = (int(j * delta_w) +
                               (bounds.xmin * bounds.width)) / im_width
                bounds.ymin = (int(i * delta_h) +
                               (bounds.ymin * bounds.height)) / im_height

                seg_width = int((j + 1) * delta_w) - int(j * delta_w)
                seg_height = int((i + 1) * delta_h) - int(i * delta_h)

                bounds.width = bounds.width * seg_width / im_width
                bounds.height = bounds.height * seg_height / im_height

            all_subjects.extend(subs)
            all_bounds.extend(bounds_list)

    intermediate_range = [
        element + 0.5 for element in range(n) if element != n - 1]

    print(intermediate_range)

    for i in intermediate_range:
        for j in range(n):
            seg = image[int(i * delta_h):int((i + 1) * delta_h),
                        int(j * delta_w):int((j + 1) * delta_w)]
            subs, bounds_list = crop_subjects(np.copy(seg, order='K'))

            for idx, sub in enumerate(subs):
                for existing_sub in all_subjects:
                    if array_is_subset(existing_sub, sub[0:int(sub.shape[0] / 4), 0:int(sub.shape[1] / 4)]):
                        break
                else:
                    all_subjects.append(sub)
                    all_bounds.append(bounds_list[idx])

    for i in range(n):
        for j in intermediate_range:
            seg = image[int(i * delta_h):int((i + 1) * delta_h),
                        int(j * delta_w):int((j + 1) * delta_w)]
            subs, bounds_list = crop_subjects(np.copy(seg, order='K'))

            for idx, sub in enumerate(subs):
                for existing_sub in all_subjects:
                    if array_is_subset(existing_sub, sub[0:int(sub.shape[0] / 4), 0:int(sub.shape[1] / 4)]):
                        break
                else:
                    all_subjects.append(sub)
                    all_bounds.append(bounds_list[idx])

    if n == 1:
        return all_subjects, all_bounds
    else:
        larger_scale_subjects, larger_scale_bounds = crop_subjects_from_segmented_image(
            image, n=n - 1)
        if len(larger_scale_subjects) >= len(all_subjects):
            return larger_scale_subjects, larger_scale_bounds
        else:
            return all_subjects, all_bounds


def get_subject_bounds(face_info):
    return face_info.location_data.relative_bounding_box


# def correct_eye_bounds(top_left, bottom_right):
#     new_top_left = min(top_left[0], bottom_right[0]), min(
#         top_left[1], bottom_right[1])
#     new_bottom_right = max(top_left[0], bottom_right[0]), max(
#         top_left[1], bottom_right[1])
#     return new_top_left, new_bottom_right


def is_left_eye_higher(face_info):
    return face_info['keypoints']['left_eye'][1] < face_info['keypoints']['right_eye'][1]


def get_eye_bounds(face_info):
    # Average eye diameter is roughly 23 mm: Bekerman, Inessa & Gottlieb, Paul & Vaiman, Michael. (2014). Variations in Eyeball Diameters of the Healthy Adults. Journal of ophthalmology. 2014. 503645. 10.1155/2014/503645. \
    # Average face width is roughly 147.6 mm: DU LL, Wang LM, Zhuang Z. [Measurement and analysis of human head-face dimensions]. Zhonghua Lao Dong Wei Sheng Zhi Ye Bing Za Zhi. 2008 May;26(5):266-70. Chinese. PMID: 18727867.

    # Thus, the width of each eye should be roughly 16% of the face width
    # This function computes eye bounds by extending 16% of the face width upward and leftward from the left eye and the same downward and rightward from the right eye
    # The extension is used as 16% rather than 8% in either direction to allow cases where the innermost edge of the eye is detected as the eye
    extension = 0.16

    face_bounds = get_subject_bounds(face_info)
    _, _, face_width, _ = face_bounds

    left_higher = is_left_eye_higher(face_info)

    if left_higher:
        top_left = int(face_info['keypoints']['left_eye'][0] - (
            face_width * extension)), int(face_info['keypoints']['left_eye'][1] - (face_width * extension))
        bottom_right = int(face_info['keypoints']['right_eye'][0] + (
            face_width * extension)), int(face_info['keypoints']['right_eye'][1] + (face_width * extension))
    else:
        top_left = int(face_info['keypoints']['left_eye'][0] - (
            face_width * extension)), int(face_info['keypoints']['right_eye'][1] - (face_width * extension))
        bottom_right = int(face_info['keypoints']['right_eye'][0] + (
            face_width * extension)), int(face_info['keypoints']['left_eye'][1] + (face_width * extension))

    return (top_left, bottom_right)


def show_point(image, point):
    image = cv.circle(image, point, radius=10, color=(0, 0, 255), thickness=-1)
    show_img(image)


def show_rect(image, top_left, bottom_right):
    cv.rectangle(
        image, (top_left[0], top_left[1]), (bottom_right[0], bottom_right[1]), (0, 255, 0), 1)
    show_img(image)


def crop_subjects(image):
    faces_info = detect_faces(image)

    im_height, im_width, _ = image.shape

    subjects = []
    bounds_list = []

    if not faces_info:
        return [], []

    for face in faces_info:
        # print(face.score)
        bounds = get_subject_bounds(face)

        xmin = bounds.xmin if bounds.xmin > 0 else 0
        xmin = xmin if xmin < 1 else 1
        ymin = bounds.ymin if bounds.ymin > 0 else 0
        ymin = ymin if ymin < 1 else 1

        x, y, w, h = int(xmin * im_width), int(ymin * im_height), int(
            bounds.width * im_width), int(bounds.height * im_height)
        sub = image[y:y + h, x:x + w]

        if not len(sub):
            continue

        try:
            sub = cv.cvtColor(sub, cv.COLOR_BGR2RGB)
        except:
            print(xmin, ymin)
            print(x, y, w, h)
            print(sub)

        subjects.append(sub)
        bounds_list.append(bounds)
    return subjects, bounds_list


# def show_bounding_boxes(image, bounding_boxes):
#     for box in bounding_boxes:
#         x, y, w, h = box['box']
#         cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 5)
#     show_img(image)

def get_eye_frame_from_img(filename):
    img = read_img(filename)
    faces_info = detect_faces(img)
    for face in faces_info:
        yield get_eye_bounds(face)


def main():
    img = read_img('./bestOf/resources/examples/IMG_1663.jpg')
    show_img(img)
    subs = crop_subjects_from_segmented_image(img, n=10)

    for sub in subs:
        show_img(sub)

    # subs, _ = crop_subjects(img)
    # for sub in subs:
    #     show_img(sub)


if __name__ == '__main__':
    main()
