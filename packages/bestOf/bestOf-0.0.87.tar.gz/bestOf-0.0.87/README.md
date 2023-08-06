# bestof

## Installation and Running

### For Windows

Simply run the following the commands:

```
pip install bestOf==0.0.87
bestOf
```

### For WSL

Install the package by running the folllowing in WSL:

```
pip install bestOf==0.0.86
```

Install Qt and related packages by running the following in WSL:

```
sudo apt install qt5-default
sudo apt-get install --reinstall libxcb-xinerama0

```

Install VcXsrv. One way to do so is by running the following commands in Powershell:

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

choco install vcxsrv
```

Start XLaunch with the following settings:

- Multiple windows
- Display number: -1
- Start no client
- Clipboard
- Primary Selection
- Native opengl
- Disable access control

To run the application, run the following in WSL:

```
export DISPLAY=:0
bestOf
```

## Summary

BestOf is an application designed to curate and cleanse large image libraries from events where several similar photos are often taken. Users simply upload all the relevant images, and BestOf returns an intuitive menu displaying their images organized into a grid layout. Each row of the grid represents a group, indicating that all images in a particular row are very similar in nature. The first image in each row is the recommended and default selected image, and at the end of the process, the user can download all selected images (having the option to select of the non-recommended ones if they so choose).

## How it Works

The process by which BestOf analyzes images has 3 major steps. First, it performs image similarity analysis by converting each image into a feature vector using a deep neural network. These feature vectors are used to compute cosine similarities and intelligently group images into sets. Second, it scores each image on default parameters. These parameters are attributes of the subjects in the image - namely whether they are blinking or cropped. An image is deemed better if a greater percentage of subjects are both not blinking and fully visible in the image. These attributes are identified via CNNs trained for these two tasks. The third step of the process is analyzing user-selected criteria. The user has the option to enable analysis of lighting, subject centering, sharpness, and resolution. They are also able to rank this criteria according to their preferences. BestOf creates a score that takes into account all enabled features, weighting them by the user defined rankings. This is combined with the default parameter score to give each image an official BestOf score that is then used to select the recommended image in each group.

## GitHub Repository

https://github.com/apangasa/bestof
