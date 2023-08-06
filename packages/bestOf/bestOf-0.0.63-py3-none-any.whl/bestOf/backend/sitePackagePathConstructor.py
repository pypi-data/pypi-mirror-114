import sys
import os


def get_site_package_path(filename):
    sitePackageList = sys.path
    sitePackPath = ""

    for i in sitePackageList:
        if not os.path.isdir(i):
            continue
        if "bestOf" in os.listdir(i):
            sitePackPath = os.path.join(
                i, filename)

    sitePackPath = sitePackPath.replace("\\", "/")
    return sitePackPath
