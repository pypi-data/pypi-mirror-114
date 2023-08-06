from setuptools import setup

setup(
    name="bestOf",
    version="0.0.67",
    description="A module that uses machine learning to chose the best image in groups",
    packages=["bestOf", "bestOf.backend",
              "bestOf.backend.saved_models", "bestOf.frontend", ],
    url="https://github.com/apangasa/bestof",
    install_requires=["torch",
                      "torchvision",
                      "mediapipe",
                      "PyQt5",
                      "Pillow",
                      "matplotlib",
                      "opencv-python-headless"],
    include_package_data=True,

    entry_points={
        'console_scripts': ['bestOf = bestOf.frontend.app:main'],
    }

)
