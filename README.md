# Table of Contents

1. [Project Description and Motivation](#motivation)
2. [Installation](#installation)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Contributors](#Contributors)
6. [Licensing & Copyright](#licensing)
7. [Acknowledgements](#Acknowledgements)
---
## Project Description and Motivation<a name="motivation"></a>
In this project all data analysis steps are followed for IMDB movie data base. The main steps I followed to find answer for my "Research Questions" are:
- Data Wrangling (Data Gathering, Data Assessment and Data Cleaning)
- Exploratory Data Analysis (visualization using Matplotlib)
- Discuss about limitation and summarizing my conclusions from EDA phase.
-----

## Installation<a name="installation"></a>
Here is the list of main libraries that I have used for this project:
* Numpy
* Pandas
* Matplotlib

The code should run with no issues using Python versions "3.8.3".

---
## File Descriptions <a name="files"></a>
The data I used in this project is provided in **tmdb-movies.csv** which could be found in main directory of this repository.

This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue


---
## Results <a name="results"></a>

In this project I was interested to find answer to some questions. My questions and brief conclusion for each of them are summarized as follow:

**Which Genre has the highest vote_average**: I found The higher the number of genre is **NOT** associated with higher vote_average. In my analysis, I found Drama had highest number of main_genre among all movies while Thriller genre was the genre with the highest vote_average.

**Relationship between revenue_adj and release_year and also profit_adj and release_year**: No correlation between revenue_adj and profit_adj with release_year BUT strong correlation between max revenue and max profit.

**Relationship between profit_adj and runtime**: Eventually, I was interested to see if the profit (max profit for each year) is correlated with max runtime ? what I found was: Although there is positive correlation between these two variables, but the correlation was not so significant.

---
## Contributors <a name="Contributors"></a>
Mehdi Khajeh
* email: <mehd.khajeh@gmail.com>
* cellphone: 403-667-8048
---
## License & Copyright <a name="licensing"></a>

&copy; Mehdi Khajeh 2021
Licensed under [MIT License](License)

---
## Acknowledgements <a name="Acknowledgements"></a>
This project was the first project that I went through whole steps of Data Analysis. I acknowledge Udacity to define this great project in their Data Analytics Nano Degree (DAND) program.

---
