import torch
from torchvision import transforms
from torch.autograd import Variable
import cv2 as cv

from bestOf.backend.classDefinitions import BlinkAndCropNet
import os
import sys
sitePackageList = sys.path
sitePackPath = ""

for i in sitePackageList:
    if not os.path.isdir(i):
        continue
    if "bestOf" in os.listdir(i):
        sitePackPath = os.path.join(
            i, './bestOf/backend/saved_models/blinkingFaces.pth')

sitePackPath = sitePackPath.replace("\\", "/")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BlinkAndCropNet()

# sitePackPath = './bestOf/backend/saved_models/blinkingFaces.pth'

model.load_state_dict(torch.load(sitePackPath, map_location=device))
model.eval()

transform = transforms.Compose(
    [transforms.ToTensor()])


def test(image):
    try:
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = cv.resize(image, (80, 80), interpolation=cv.INTER_AREA)

        image_tensor = transform(image)
        image_tensor = image_tensor.unsqueeze(0)

        input_var = Variable(image_tensor)
        input_var = input_var.to(device)
        output = model(input_var)
        output = torch.round(output)

        return output.data.cpu().numpy()[0][0]

    except Exception as e:
        # print(e)
        return 0


if __name__ == '__main__':
    import identifyPeople

    x = test(identifyPeople.read_img(
        './bestOf/resources/blinkset/nonblinkers/Adrian_McPherson_0001.jpg'))
    # print(x)

    subs, _ = identifyPeople.crop_subjects(
        identifyPeople.read_img('./bestOf/resources/examples/IMG_1351.jpg'))

    x = test(subs[0])
    # print(x)
