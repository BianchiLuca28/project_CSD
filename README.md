# Detecting anomalies in Time Series

This project is a collaboration with Schnell S.p.A, we explored different Machine Learning tecniques to detect anomalities in time series data produced by different sensor mounted on a special machinery. 


## Authors

- [@Stanislav Teghipco](https://github.com/Staffilon)
- [@Fabio De Vitis Michele](https://github.com/FabioDevIsTyping)
- [@Francesco Finucci](https://github.com/Meguazy)
- [@Luca Bianchi](https://github.com/BianchiLuca28)

## Documentation
Here we can find the documentation for the project. We explain in details the various steps of the process, starting from a description of the starting dataset and ending with the creation and the validation of the model.
The docs can be found at this link: [Documentation](https://drive.google.com/file/d/1yRoNmiyTgJKQRJEjwGaD6Xc2AcvF08Yqview?usp=sharing).

## Presentation
Here we can find the slides for the presentation of the project: [Presentation](https://unicamit-my.sharepoint.com/:p:/g/personal/stanislav_teghipco_studenti_unicam_it/EeYaSQk9lTdNvvI-N101UtYB6rhWWFd0QLN8m8f8Imn9zw?e=aGzivB)

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

## FAQ

#### Question 1

Answer 1

#### Question 2

Answer 2


## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

