# IPASS - Kaedin Schouten - 2021
## About the project (IPASS)
The Individual Propaedeutic Assessment (IPASS) is the direction-specific conclusion of the propaedeutic year in my studies: HBO-ICT; direction: Artificial Intelligence. It's my chance to show what I've learned this year. In addition, IPASS has been designated as an executioner: I have to obtain at least a pass mark for this project in order to be allowed to move on to the second year of this training.

## The problem
If a candidate has to go through a program (on the [Eelloo](https://eelloo.nl) platform) with multiple, predominantly long questionnaires (such as 'Drives' and 'Personality'), this costs the candidate a lot of time. In addition, this does not seem to be an inspiring activity for every candidate.

Is it possible to use an algorithm to predict the final profile/report that candidates will receive when they have completed all questionnaires and questionnaires, based on less information and intermediately calculated scale scores?

### Requirements
1. We work with an anonymized dataset
2. Predictions must be made after each amount of information added
3. The predictions are made for information that has not yet been filled in
4. The more information provided by the candidate, the more accurate the prediction of the missing information becomes
5. The intermediate accuracy is possibly indicated with a number (for example 1-100) (optional)
6. The algorithm must work on the platform as a 'thinking app'
7. The algorithm should provide a fun user experience. So fast calculation time.
8. The algorithm must be used for the benefit of the candidate. The candidate remains in control

## My solution
### Algorithm
The algorithm that I am developing can be seen as an 'engine'. Which means that it is 1 large algorithm that consists of several (small) algorithms that work together. These smaller algorithms coordinate which calculations are most efficient based on the data that the engine receives. This way you have an engine that is fast, smart and reusable. The disadvantage of this is that it requires a lot of thinking and programming work. Fortunately, with my knowledge and planning I can manage this well and this should not cause any unforeseen problems.

### Type
This algorithm is a prediction algorithm. Which - as the name says - is going to predict scores using the dataset. What is important with this kind of algorithm is that validating a result is quite difficult. This is doable in the test situation, because you already know in advance what a candidate has as a score. In the production environment this is not the case and it is therefore important that enough validation calculations and tests are made to measure reliability.

### Aim
This engine is used for the benefit of the candidate. It is therefore important that the predictions of scores are accurate and reliable, but also that the candidate remains in control at all times. Using the dataset, large numbers of tests can be made that can contribute a lot to calibrating the engine in order to provide the most reliable result. The purpose of this engine is therefore to accurately, reliably and efficiently predict scores from non-completed assessment scores. With this data we can easily guide the candidate through the platform as a collaborative app.

## Repository-contents
### [Data](data)
All the datasets used for the algorithm. These dataset(s) container thousands of rows which each row being a candidate and its scores for every trait. The candidates (and their scores) are used for computing predictions.

### [Tests](tests)
This directory houses all the files for the tests. We have 2 testfiles as we have 2 main classes. Each of the classes has their own sub-functions and helper-code to achieve its purposes. It is important to know that testing and validating functions are two very different things. Because the aim of the algorithm is to predict scores, we can test this by seeing if we get result. What result we get does not really matter as it is a prediction. It might not be a very accurate prediction but is to be determined by the validation.

### [Main](main.py)
A file with the main function tot test the code and fetch results. See below for intstructions on how to use.

### [Models](models.py)
This file container 2 classes. 1 controller class for the Dataset and the other for the engine. Each class has its own helper-functions and code to achieve their purposes. This file also houses a few object-models.

### [Plots](plots.py)
In this file there are functions that are able to plot certain candidate-score related computations. For exmaple: plot 100 candidates with half their scores predicted. The functions should be called from the [main file](main.py).

### [Utils](utils.py)
This utils file - as the same states - is file containing some utility-functions. Mainly to help functions in the [plots](plots.py) and [main](main.py) files. For example: getting all the empty traits from a user.

## Libraries used
### [Matplotlib](https://matplotlib.org/stable/gallery/index.html)
This is only used to plot test cases. This way you can see the growth in accuracy or other similar interesting measurements. The impact of this library is only fairly large for the test cases.

### Copy --> [Deep copy](https://docs.python.org/3/library/copy.html)
This standard Python library is used to make deep copies. This is done so that we can make a copy of, for example, a candidate and thus know the original state. The impact of this library is quite large since making a copy of an object is done in a number of (important) places.

### CSV --> [Reader](https://docs.python.org/3/library/csv.html)
A standard Python library used to load CSV files. So these are the datasets I received from Eelloo. The impact of this library is great because the dataset is loaded with it.

### Math --> [Sqrt](https://docs.python.org/3/library/math.html)
Python standard library that has useful tools such as a faster runtime for calculating the square root of a number. The impact of this library is very small. I could have coded such functions myself, but the runtime might have been longer. It's also nice that this comes standard in Python, so you don't have to install anything.

### Random --> [Choice](https://docs.python.org/3/library/random.html#functions-for-sequences), [Randint](https://docs.python.org/3/library/random.html#functions-for-integers), [Shuffle](https://docs.python.org/3/library/random.html#functions-for-sequences)
Also a basic Python library that has useful tools to do anything arbitrary. This is implemented in a function that returns a random candidate from a list, and a function that returns a random number as a backup within certain limits. The impact of this function is very small as I could also have made tools myself. This library is standard in Python and that is the reason that I chose the library. Also a faster runtime.

### Collections --> [Counters](https://docs.python.org/3/library/collections.html#counter-objects)
A standard Python library can easily count how many times an element occurs in a list. This one has a significantly faster runtime than you would with pure-python. So the impact of this is huge.

### Data classes --> [Data class](https://docs.python.org/3/library/dataclasses.html)
A very important Python library that can easily turn python classes into objects (dataclasses). This 'decorator[13]' is placed at the top of the class definition to show that it is a data class. The impact of this is very large.

## How-to-run
1. Clone this repo
2. Make sure you have a virtual environment setup with the library [Matplotlib](https://matplotlib.org/stable/gallery/index.html) installed
3. Run the main.py
4. Change the functions, values, calles etc if needed in the main.py
