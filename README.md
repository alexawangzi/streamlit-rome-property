## Project summary 

A data app that helps aspiring Rome investors to discover and analyse the value of their properties for short rentals.

## Team and project overview

<details open="open">
<summary><h3 style="display: inline-block">Team presentation</h2></summary>

Jianing Chen / Guoyang Cui / Yuqi Shen / Zi Wang / Qiang Zhu

1. First brainstorming:  All members 
    1. Discuss user requirement to build story line
    2. Confirm type of data visualisation 
    3. Establish code collaboration form - Gitlab & git
2. Data preprocessing and filter: Zi Wang 
    1. Clean data and deal with missing value 
3. Main task: All members 
    1. Follow the visualisation logic, generate graphs separately, each person was responsible for one graph
4. Results Collation ：Yuqi Shen
5. Documentation ：All members 

</details>

<details open="open">
<summary><h3 style="display: inline-block">General strategy</h2></summary>

1. Shows the distribution, occupancy rate and revenues for landlords of short rentals in Rome 
2. Can be filtered according to year, time and number of bedrooms
3. Help potential landlords to better choose their housing investments
</details>

## Approach

<details open="open">
<summary><h3 style="display: inline-block">Approach description</h2></summary>

Thinking from the perspective of landlord, we follow the story line that help the potential landlord decide where and how to invest in order to get larger profitability 
1. Overall Description
    1. Give general idea of the distribution and density of available housings through time - Scatter Plot
    2. Add tourist attractions point to get a better idea of the needs around - Icon graph
2. Occupancy rate - Screengrid
    1. Compared to others, occupancy rate is one of the most important indicators that directly influences final revenue
    2. Should vary a lot in different months and different type of properties
3. Revenue
    1. Total monthly revenue in general - Screengrid
    2. ADR (= total revenue / total rent days) - Heatmap 
    3. Average Daily Revenue (= total revenue / total available days), As compared to ADR, profitability can better capture the actual revenues of landlords. - 3D barchart 

</details>

<details open="open">
<summary><h3 style="display: inline-block">Future improvements</h2></summary>

1. Better layout for widgets and more reasonable choice of widgets. For example, for the selection of number of bedrooms, we can use "multiselect" instead of "selectbox".  

2. Change the size of icons. Since the tourist attraction icons can not be retrieved from local, the large size of the icons actually affects the performance(running time and fluency).  

3. Add download option for filtered data table for users to investigate.  

4. Add icons of major transportation stations such as train stations, airports, etc. for better discovery of the relationships between property revenues and their corresponding locations.   

5. Add filtering options for Property_Type and Listing_Type.  

6. Add labels to each data point. When clicking on a data point, its corresponding statistics and metrics will display.
</details>

## Project usage

### Requirements:

1. You have installed the Python 3.8.11.

2. Following python modules requirements have been fulfilled
	streamlit==0.79.0

	pydeck==0.7.0	

	pandas==1.1.3

	scikit-learn==0.23.2

	urllib3==1.25.11

### How to run the code

1. cd group_submission/

2. streamlit run submission.py ( add '--logger.level=debug' for debug mode)

3. open the app in brower with the indicated url


### Structure of code base

1. dataset folder containes icons and url links that are used for icon plot

2. clean_cleaning.ipynb contains the proicedure to clean the dataset

3. submission.py contain the code to genertae the website.

