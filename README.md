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


## Libraries

## How-to-run
