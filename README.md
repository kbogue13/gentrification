This is the repository for my 2018 Master of Science in Geospatial Technologies degree at the University of Washington.

What follows is:
1)	A brief description of the purpose of the script
2)	An overview of what the script does
3)	Recommendation for visualizing the output .shp

Purpose:
Over the past three decades awareness around gentrification within America’s urban centers has increased. As consciousness has risen amongst the general population, gentrification has become a much more widely debated subject which has spurred new focus into a long-established subject of study. To date, much of the gentrification research has examined the impacts on individual communities or has retroactively probed an area that has gentrified in order to determine latent origins. By comparison there has been relatively little research examining whether the process of gentrification can be preemptively predicted. Moreover, the predictive studies that have been undertaken tend to focus on a specific locality as opposed to an approach that seeks to encompass larger areas and trends. This research will examine whether the process of gentrification can be identified by quantitative indicators and explores the possibility of creating a technological framework to assess susceptibility to future gentrification based on existing demographic factors within the United States.

Methods:
This script uses the Selenium Webdriver and Google Chrome to locate and download demographic data obtained from the Unites States Census Bureau’s 2017 American Community Survey 5-year estimates at the Block Group level. The script takes user input for the location of the ‘Downloads’ folder as well as the path the webdriver necessary to allow for the automation of the Chrome browser. After receiving valid input, the script navigates to the American Fact Finder website (https://factfinder.census.gov/faces/nav/jsf/pages/download_center.xhtml) and asks the user to enter the State and County in which they are interested. The script then downloads tables: 

B19013 -- MEDIAN HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2017 INFLATION-ADJUSTED DOLLARS)

B02001 -- RACE

B25071 -- MEDIAN GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME IN THE PAST 12 MONTHS (DOLLARS)

B25077 -- MEDIAN VALUE (DOLLARS)

B15003 -- EDUCATIONAL ATTAINMENT FOR THE POPULATION 25 YEARS AND OVER

Then the script navigates to the US Census Bureau’s TIGER/Line Shapefiles website (https://www.census.gov/cgi-bin/geo/shapefiles/index.php) to download the geography that corresponds to the user’s previously defined State and County.
Once the tabular demographic data and the corresponding geographic data are finished downloading, the script will unzip the folders and will:
1: Clean the tabular data to rid it of any non-numerical characters and prepare it for processing.
2: For each of the five tables, calculate quantiles for the tabular data into five classes. Each class receives 20% of the data.
3: For each of the five tables, calculate a score of 1-5 based on the quantile and its impact of susceptibility to gentrification. 1 indicates a low susceptibility (or that the area is already gentrified) and 5 indicates a high susceptibility. A score of 0 indicates that there was no data for that indicator in a certain Block Group.
4: For each of the five tables, output a CSV showing the data used to calculate scores.
5: Total the scores and calculate an average score using only the indicators for which there are non-zero values (remember a score of 0 indicates no data). This is done because not all indicators have values for all Block Groups so just totaling the scores would misrepresent the data.
6: Output a CSV showing data used to calculate scores as well as the total and average scores.
Finally, the final calculated CSV is joined to the geographic data and saved to the Downloads folder as GentrificationSusceptibility.shp. This file can be imported into ESRI ArcGIS of QuantumGIS (QGIS) software for visualization.

Visualization:
Within your preferred GIS software, add the GentrificationSusceptibility.shp from your Downloads folder. The attribute table contains all the data used to calculate the scores for each indicator so that the user can visualize each indicator individually or the average indicator score for each Block Group. If the user plans to visualize the overall score, use the ‘Average’ column because it calculates the average score for all indicators with non-zero scores (zero indicates no data) for each Block Group whereas the ‘Total’ column is simply the sum of the all indicator scores (including zero) for each Block Group.
By visualizing the GentrificationSusceptibility.shp ‘Average’ column, the user will see each Block Group’s overall susceptibility based on the previously stated indicators. Typically, the areas most susceptible to gentrification are the most underprivileged areas and are not necessarily the most likely to gentrify. In general, the user should visually identify areas with higher scores (3,4,5) that are in close proximity to areas with lower scores (1,2) as it is more likely that those areas will gentrify due to their proximity to areas that are already gentrified.
