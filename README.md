![image](https://github.com/CharlesQuinn1/project_4_fantasy_football/assets/128498023/a1dca74e-0e36-4dbc-bf4c-58e99b97f8bc)



### Project Overview:
---
<b>Project Team Members:</b><br>
*	Charles Quinn inlikequinn1@gmail.com 
*	Alice Liu alice.liu053@gmail.com 
*	Brandon Loredo  bloredo1987@gmail.com  
*	Bryan Miller Bryanmiller512@Gmail.com

<b>Project Scope and Objectives:</b><br>
<p>The objective of this project is to develop a predictive machine learning algorithm leveraging NFL Combine results data spanning from 2000 to 2015. This algorithm is designed to assess an athlete's likelihood of transitioning into a professional NFL career based on their performance metrics during the Combine. By thoroughly analyzing this historical dataset, we intend to uncover crucial patterns and trends that significantly influence a player's potential NFL success. The primary aim is to provide valuable insights for both players and scouts, aiding in decision-making processes and potentially revolutionizing talent evaluation within the NFL.</p>

<b>Key Objectives:</b><br>
*	Assess NFL Combine data from 2000 to 2015
*	Identify key performance metrics crucial for NFL success
*	Develop a machine learning model for player evaluation
*	Evaluate the model's predictive accuracy and reliability
*	Provide actionable insights for players and scouts
*	Enhance talent evaluation processes within the NFL
*	Enable data-driven decision-making in player selection

<b>Link to dataset:</b><br>
*	https://www.kaggle.com/datasets/mitchellweg1/nfl-combine-results-dataset-2000-2022 
*	https://www.kaggle.com/datasets/ulrikthygepedersen/nfl-draft-1985-2015/data

### Rationale for the Project:
---
<b>Project Advantages:</b><br>
*	Informed Player Choices: Equips players with data-backed insights to make strategic decisions about their NFL aspirations.
*	Proactive Talent Development: Supports players in identifying areas for improvement, thereby increasing their chances of success in the NFL.
*	Optimized Team Selection: Enables NFL teams to make more informed choices during player drafts, leading to more competitive and successful rosters.

<b>Performance Metrics:</b><br>
To assess the impact and effectiveness of the project, the following key performance indicators will be employed:
*	<b>Performance Metrics:</b> Success will be evaluated based on the project's ability to establish significant correlations between player metrics, combine results, and eventual NFL performance. This analysis will drive targeted recommendations for players seeking to maximize their potential.
*	<b>Draft Success Rate:</b> The project's effectiveness will be measured by tracking the success rate of players recommended by the model in actual NFL drafts. A higher rate of drafted players achieving successful careers will indicate the model's accuracy.
*	<b>Long-Term Success Stories:</b> Tracking the careers of players who received recommendations and eventually made it into the NFL will serve as a testament to the project's effectiveness in identifying true potential.

### Project Outline:
---
*	Data cleaning <b>(Python)</b>
    -	load data to SQLite database
    -	document data
    -	Data exploration <b>(Tableau)</b><br>
            -	data trends<br>
            -	data distribution by combine position and event<br>
            -	identify outliers<br>
            -	correlation matrix

![image](https://github.com/CharlesQuinn1/project_4_fantasy_football/blob/main/Images/exploration_img1.png?raw=true)

![image](https://github.com/CharlesQuinn1/project_4_fantasy_football/blob/main/Images/exploration_img2.png?raw=true)

![image](https://github.com/CharlesQuinn1/project_4_fantasy_football/blob/main/Images/exploration_img3.png?raw=true)

* 	Models to Use <b>(Python)</b>:
    -	Decision Tree
    -	Naive Bayes
    -	KNN
    -	Random Forest
*	Analysis
    -	Compare each model using accuracy_score

![image](https://github.com/CharlesQuinn1/project_4_fantasy_football/blob/main/Images/models_img1.png?raw=true)

![image](https://github.com/CharlesQuinn1/project_4_fantasy_football/blob/main/Images/models_img2.png?raw=true)

![image](https://github.com/CharlesQuinn1/project_4_fantasy_football/blob/main/Images/models_img3.png?raw=true)
