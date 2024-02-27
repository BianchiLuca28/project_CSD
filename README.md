# Detecting anomalies in Time Series

This project is a collaboration with Schnell S.p.A, we explored different Machine Learning tecniques to detect anomalities in time series data produced by different sensor mounted on a special machinery. 


## Authors

- [@Stanislav Teghipco](https://github.com/Staffilon)
- [@Fabio De Vitis Michele](https://github.com/FabioDevIsTyping)
- [@Francesco Finucci](https://github.com/Meguazy)
- [@Luca Bianchi](https://github.com/BianchiLuca28)

## Documentation
Here we can find the documentation for the project. We explain in details the various steps of the process, starting from a description of the starting dataset and ending with the creation and the validation of the model.
The docs can be found at this link: [Documentation](https://drive.google.com/file/d/1yRoNmiyTgJKQRJEjwGaD6Xc2AcvF08Yq/view?usp=sharing).

## Presentation
Here we can find the slides for the presentation of the project: [Presentation](https://unicamit-my.sharepoint.com/:p:/g/personal/stanislav_teghipco_studenti_unicam_it/EeYaSQk9lTdNvvI-N101UtYB6rhWWFd0QLN8m8f8Imn9zw?e=aGzivB)

## Pre-requisites
You need to have docker, docker-compose and python installed on your computer.

## Run Locally

Clone the project

```bash
  git clone https://github.com/Meguazy/project_CSD
```

From the root directory, execute the following to build the image

```bash
  docker docker build -t streamlit .
```

Finally, start the image

```bash
  docker run -p 8501:8501 --name project_CSD streamlit
```

From here, connect to the following link on your browser to use the app 

```bash
  locahost:8501
```

## Access via the web link

Another way to access the app is via this link

```bash
  https://projectcsd.streamlit.app/
```

## Tool usage description
In order to correctly use the tool you need to have the repository cloned locally. 
Once you either click the web link or build the image locally with Docker, you will be welcomed by this home screen:

![Home Page](https://github.com/Meguazy/project_CSD/blob/main/Tool/streamlitProject/images/home_page?raw=true)

To analyze a time serie you have click on browse files and then you have to choose one of the samples located in the repository under 

```bash
  /Tool/streamlitProject/samples/
```

This is what you will see after you've uploaded a sample

![Sample uploaded](https://github.com/Meguazy/project_CSD/blob/main/Tool/streamlitProject/images/uploaded_series?raw=true)

From here you can either classify the time series, browse the app to get some statistical and analytical informations or you can click on the "PCA visualization" tab to get more info about the classified points for said acquisition. There also is an "About Us" page in which we you can find some informations about us creators of the project.

## About the Data directory
This data is deprecated data that we no longer use. We let it live on the repository only because if we didn't the older versions of the notebooks would not be runnable.

## About the python scripts directory
Here you can find scripts for the preprocessing of the files, such as cleaning, merging and organization of the various datasets.

## FAQ

#### Which preprocessing did we apply?
We've used L2 normalization in order to reduce the number of this series for accelerometer to 1 and StandardScaling to be able to analyze data on the same scale.

#### How did we classify the faulty acquisition?
We've used the CART algorithm and applied a Decision Tree on the data. Since we had labeled data we were able to apply a supervised learning algorithm

#### How did we find anomaly points on faulty acquisitions?
We've used statistical method such analyzing the points outside of the standard deviation range.


## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

