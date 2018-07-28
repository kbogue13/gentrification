#Script written by K.Bogue as part of his 2018 Master of Science in Geospatial Technoogies degree at the University of Washington
'''
It is expected that you have read the README accompanying this script before running it.

For this script to run you must have the Google Chrome web browser as well as the python libraries for
selenium, zipfile, pandas and geopandas installed.

Additionally, you will need a Chrome webdriver. One has been provided for you in the GitHub repository or your own can be found
at https://sites.google.com/a/chromium.org/chromedriver/downloads

You will be asked to provide a path to your 'Downloads' folder and a path to the Chrome webdriver.

By default the Chrome browser downloads to your computer's downloads folder. If you have altered Chrome's download destination,
this script may fail.

If running this script multiple times, best practice is to empty the 'Downloads' folder before running again

Running this script behind a VPN can cause it to fail. It is recommended you desconnect from your VPN before proceeding.

This script was written in Python 3.6
'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import zipfile
import geopandas as gpd
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
import csv
import functools
import time

#User set downloads folder
while True:
    dPath = input(r"Please enter the path to your 'Downloads' folder: ")
    try:
        if os.path.exists(dPath) == True:
            pass
    except:
        pass
    if os.path.exists(dPath)==False:
        print ('The provided folder does not exist')
        print ('Please try again')
        continue
    if dPath.endswith('Downloads') == True:
        break
    if dPath.endswith('Downloads') == False:
        dPath = dPath + "\Downloads"
        pass
        if os.path.exists(dPath) == True:
            break
        else:
            continue

downloadPath = dPath

#User provide path to Chrome driver
while True:
    try:
        cPath = input(r'Please enter the FULL path to the Google Chrome web driver (including \chromedriver.exe): ')
        if os.path.exists(cPath) == True:
            pass
        if cPath.endswith('chromedriver.exe') == True:
            print('Please wait...')
            break
    except:
        pass
    if (os.path.exists(cPath))==False:
        print ('The provided path is invalid')
        print ('Please try again')
        continue
    if (cPath.endswith('chromedriver.exe')) == False:
        print ("Don't forget to include \chromeDriver.exe in the path")
        print ('Please try again')
        continue

chromePath = cPath

driver = webdriver.Chrome(chromePath)

#minimize window
#driver.set_window_position(-2000,0)

#time how long the code takes
start = time.time()
#Delete files in 'Downloads folder

folder = downloadPath
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)
#functions making selenium wait for specific circumstances

def smallWait():
    timeout = .33 #second
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="filterDimensionListId'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        pass

def medWait():
    timeout = 1 #second
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="filterDimensionListId'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        pass

def wait():
    timeout =  100#second
    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="dummy"]'))
    smallWait()
    if element_present == True:
        WebDriverWait(driver, timeout).until(element_present == False)
        smallWait()

def nextButtonWait(): #this is for a specific next button
    timeout = .01
    while True:
        try:
            element_present = EC.element_to_be_clickable((By.XPATH, '''//*[@id="nextButton"]'''))
            WebDriverWait(driver, timeout).until(element_present)
            break
        except TimeoutException:
            pass
        if element_present == False:
            WebDriverWait(driver, timeout).until(element_present)

def downloadWait(): #continually checks for 'download' button to be clickable
    timeout = .01 #seconds
    while True:
        try:
            element_present = EC.element_to_be_clickable((By.XPATH, '''//*[@id="yui-gen2-button"]'''))
            WebDriverWait(driver, timeout).until(element_present)
            break
        except TimeoutException:
            pass
        if element_present == False:
            WebDriverWait(driver, timeout).until(element_present)


'''Make driver navigate to American Fact Finder Download Center and download data'''

driver.get('https://factfinder.census.gov/faces/nav/jsf/pages/download_center.xhtml')
#Make driver click 'Next' to go to Dataset
smallWait()
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="nextButton"]''')))
driver.find_element_by_xpath('''//*[@id="nextButton"]''').click() #needs to be triple quoted

#Choose Ameriacn Community Survey from drop down
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="filterDimensionListId"]/option[2]''')))
driver.find_element_by_xpath('''//*[@id="filterDimensionListId"]/option[2]''').click()
wait()
#choose ACS 5-year from drop down
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="listDimensionListId"]/option[1]''')))
driver.find_element_by_xpath('''//*[@id="listDimensionListId"]/option[1]''').click()
wait()
#click 'Add to selection'
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="button_container"]/a''')))
driver.find_element_by_xpath('''//*[@id="button_container"]/a''').click()
wait()
#medWait()

#click 'Next' to move to 'Geographies' page
driver.find_element_by_xpath('''//*[@id="nextButton"]''').click()
wait()
#select 'Block Group' as the geographic type
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="summaryLevel"]/option[15]''')))
driver.find_element_by_xpath('''//*[@id="summaryLevel"]/option[15]''').click()

#User select state

state = str()
while True:
    try: 
        state = str(input("What state is the area you are interested in located?  ").title())
        selectState = Select(driver.find_element_by_id("state"))
        for option in selectState.options:
            if option.text == state:
                selectState.select_by_visible_text(state)
                break
    except:
        if state != str():
            print ("Invalid input")

    if option.text != state:
        print ("State not recognized. Please try again")
        continue
    else:
        break
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, '''county''')))

#User select county
county = str()
while True:
    try:
        county = str(input("What is the name of the county of interest? ").title())
        selectCounty = Select(driver.find_element_by_id("county"))
        for option in selectCounty.options:
            if option.text == county:
                selectCounty.select_by_visible_text(county)
                break
    except:
        if county != str():
            print ("Invalid input")

    if county.endswith('County') == True:
        county = county[:-7]
        pass
        for option in selectCounty.options:
            if option.text == county:
                selectCounty.select_by_visible_text(county)
                break
        else:
            print ("County not recognized. Please try again")
            continue
    if option.text != county:
        print ("County not recognized. Please try again")
        continue
    else:
        break

print('Acquiring tabular demographic data...')
medWait()
wait()

#click on All Block Groups for X
driver.find_element_by_xpath('''//*[@id="geoAssistList"]/option''').click()
smallWait()
wait()

#click 'ADD TO YOUR SELECTIONS' button
driver.find_element_by_xpath('''//*[@id="addtoyourselections"]''').click()
smallWait()
wait()
medWait()
wait()
smallWait()
#click 'NEXT' to move to SEARCH RESULTS page
WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="nextButton"]''')))
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="nextButton"]''')))
driver.find_element_by_xpath('''//*[@id="nextButton"]''').click()

#Enter B19013, B02001, B25071, B25077, B15003  into search bar this is Median Income, Race, Rent as % of Household Income, Median Home Value, and Educational Attainment
#smallWait()
wait()
smallWait()
medWait()
WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="prodautocomplete"]''')))
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="prodautocomplete"]''')))
inputElement = driver.find_element_by_xpath('''//*[@id="prodautocomplete"]''')
inputElement.click()
inputElement.clear()
inputElement.send_keys('B19013, B02001, B25071, B25077, B15003')
inputElement.send_keys(Keys.ENTER)

#Click 'Check All' button
#smallWait()
wait()
medWait()
WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="check_all_btn_below"]''')))
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="check_all_btn_below"]''')))
driver.find_element_by_xpath('''//*[@id="check_all_btn_below"]''').click()

#Click 'Next'
medWait()
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="nextButton"]/img''')))
driver.find_element_by_xpath('''//*[@id="nextButton"]/img''').click()

#download all selected tables
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="dnld_conf_chk"]''')))
driver.find_element_by_xpath('''//*[@id="dnld_conf_chk"]''').click()
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="yui-gen0-button"]''')))
driver.find_element_by_xpath('''//*[@id="yui-gen0-button"]''').click()
downloadWait()

#Click 'Download' once it appears
driver.find_element_by_xpath('''//*[@id="yui-gen2-button"]''').click()
print('Downloading tabular demographic data')

'''Download TIGER shapefiles'''

print('Acquiring geographic data...')
driver.get('https://www.census.gov/cgi-bin/geo/shapefiles/index.php')
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="year"]/option[2]''')))

#Choose year 2016 to match ACS
driver.find_element_by_xpath('''//*[@id="year"]/option[2]''').click()
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="layergroup"]/option[3]''')))
#Choose block groups
driver.find_element_by_xpath('''//*[@id="layergroup"]/option[3]''').click()
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="left-column"]/div/form/table/tbody/tr[3]/td[2]/input''')))
#Click 'Submit'
driver.find_element_by_xpath('''//*[@id="left-column"]/div/form/table/tbody/tr[3]/td[2]/input''').click()
#Choose State
while True:
    try: 
        selectState = Select(driver.find_element_by_id("fips_34"))
        for option in selectState.options:
            if option.text == state:
                selectState.select_by_visible_text(state)
                break
    except:
        pass

    if option.text != state:
        print ("State not recognized. Please try again")
        continue
    else:
        break
    
#Click 'Download'
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="middle-column"]/div/ul/li/input''')))
driver.find_element_by_xpath('''//*[@id="middle-column"]/div/ul/li/input''').click()

print('Downloading geographic data')

#unzip American Fact Finder zip when it finishes downloading
while True:
    try:
        dx = [f for f in listdir(downloadPath) if isfile(join(downloadPath, f))]
        for x in dx:
            if x.endswith("aff_download.zip"):
                file = downloadPath + "\\" + x
                zip_Tiger = zipfile.ZipFile(file , 'r')
                zip_Tiger.extractall(downloadPath)
                zip_Tiger.close()
                break
    except:
        pass
    if x.endswith("aff_download.zip")==False:
        continue
    else:
        break


#unzip TIGER shapefile when it finishes downloading
while True:
    try:
        dl = [f for f in listdir(downloadPath) if isfile(join(downloadPath, f))]
        for x in dl:
            if x.endswith("bg.zip"):
                file = downloadPath + "\\" + x
                zip_Tiger = zipfile.ZipFile(file , 'r')
                zip_Tiger.extractall(downloadPath)
                zip_Tiger.close()
                break
    except:
        pass
    if x.endswith("bg.zip")==False:
        continue
    else:
        break
    
print('Calculating...')

#Close Chrome
driver.quit()

#Turn off warnings for calculating only slices of data
pd.options.mode.chained_assignment = None  # default='warn'

#Identify CSVs
fname = downloadPath + '\ACS_16_5YR_B02001_with_ann.csv' #Race
fname1 = downloadPath + '\ACS_16_5YR_B19013_with_ann.csv' #Median Income
fname2 = downloadPath + '\ACS_16_5YR_B25071_with_ann.csv' #Rent as % of MI
fname3 = downloadPath + '\ACS_16_5YR_B25077_with_ann.csv' #Housing Value
fname4 = downloadPath + '\ACS_16_5YR_B15003_with_ann.csv' #Educational Attainment

#RACE
outF = downloadPath + '\Race.csv'
with open(fname, 'r') as inFile, open(outF, 'w') as outFile:
    r = csv.reader(inFile)
    w = csv.writer(outFile)
    
    #read the header
    header = next(r)
    
    #change header titles
    header[1] = 'GEOID'
    header[3] = 'TotalPop'
    header[5] = 'WhitePpl'
    header[6] = 'PctWhite'
    header[7] = 'Score'
    w.writerow(header)
    
    #copy the rest of the data
    for row in r:
        w.writerow(row)

#Calculate percentage of white people
df1=pd.read_csv(outF, usecols = ['GEOID', 'TotalPop', 'PctWhite', 'WhitePpl', 'Score'], converters={'GEOID': lambda x: str(x)})
df1['PctWhite'] = df1['WhitePpl'] / df1['TotalPop']

#Calculate quantiles
below20 = df1.PctWhite.quantile((.2), 'lower')
below40 = df1.PctWhite.quantile((.4), 'lower')
below60 = df1.PctWhite.quantile((.6), 'lower')
below80 = df1.PctWhite.quantile((.8), 'lower')

#write quantiles to CSV
pctWhite = df1['PctWhite']

df1.Score.loc[pctWhite <= below20] = 5
df1.Score.loc[pctWhite > below20] = 4
df1.Score.loc[pctWhite > below40] = 3
df1.Score.loc[pctWhite > below60] = 2
df1.Score.loc[pctWhite > below80] = 1  
df1.Score.loc[df1.Score > 5] = 0 #gives a zero to block groups whose scores aren't compatible

df1.to_csv(outF)

#MEDIAN INCOME
outF1 = downloadPath + '\MedianIncome.csv'
with open(fname1, 'r') as inFile, open(outF1, 'w') as outFile:
    r = csv.reader(inFile)
    w = csv.writer(outFile)
    
    #read the header
    header = next(r)
    
    #change header titles
    header[1] = 'GEOID'
    header[3] = 'MI'
    header[4] = 'MI_Score'
    
    w.writerow(header)
    #copy the rest of the data
    for row in r:
        w.writerow(row)
        
#Remove characters that casue MI to be read as a string
df99 = pd.read_csv(outF1, usecols = ['GEOID', 'MI', 'MI_Score'], converters={'GEOID': lambda x: str(x)})
MI = df99['MI']
for i in MI:
    if i == '-':
        df99.MI.loc[MI == ('-')] = 0
    if i == '2,500-':
        df99.MI.loc[MI == '2,500-'] = 2500
    if i == '5,000-':
        df99.MI.loc[MI == '5,000-'] = 5000
    if i == '250,000+':
        df99.MI.loc[MI == '250,000+'] = 250000

df99.to_csv(outF1)

#Calculate quantiles for median income
df2 = pd.read_csv(outF1, usecols = ['GEOID', 'MI', 'MI_Score'], converters=({'GEOID': lambda x: str(x), 'MI': lambda y: int(y)}))

MIbelow20 = df2.MI.quantile((.2), 'lower')
MIbelow40 = df2.MI.quantile((.4), 'lower')
MIbelow60 = df2.MI.quantile((.6), 'lower')
MIbelow80 = df2.MI.quantile((.8), 'lower')

medIncome = df2['MI']

df2.MI_Score.loc[medIncome <= MIbelow20] = 5
df2.MI_Score.loc[medIncome > MIbelow20] = 4
df2.MI_Score.loc[medIncome > MIbelow40] = 3
df2.MI_Score.loc[medIncome > MIbelow60] = 2
df2.MI_Score.loc[medIncome > MIbelow80] = 1
df2.MI_Score.loc[medIncome == 0] = 0 


df2.to_csv(outF1)
#RENT AS % OF MEDIAN INCOME
outF2 = downloadPath + '\RentPct.csv'
with open(fname2, 'r') as inFile, open(outF2, 'w') as outFile:
    r = csv.reader(inFile)
    w = csv.writer(outFile)
    
    #read the header
    header = next(r)
    
    #change header titles
    header[1] = 'GEOID'
    header[3] = 'RentPct'
    header[4] = 'Rent_Score'
    
    w.writerow(header)
    #copy the rest of the data
    for row in r:
        w.writerow(row)

df98 = pd.read_csv(outF2, usecols = ['GEOID', 'RentPct', 'Rent_Score'], converters={'GEOID': lambda x: str(x)})
RentPct = df98['RentPct']
for a in RentPct:
    if a == '-':
        df98.RentPct.loc[RentPct == ('-')] = 0
    if a == '50.0+':
        df98.RentPct.loc[RentPct == ('50.0+')] = 50.0
    if a == '10.0-':
        df98.RentPct.loc[RentPct == ('10.0-')] = 10.0

df98.to_csv(outF2) 
       
df3 = pd.read_csv(outF2, usecols = ['GEOID', 'RentPct', 'Rent_Score'], converters=({'GEOID': lambda x: str(x), 'RentPct': lambda y: str(y)}))

RENTbelow20 = df3.RentPct.quantile((.2), 'lower')
RENTbelow40 = df3.RentPct.quantile((.4), 'lower')
RENTbelow60 = df3.RentPct.quantile((.6), 'lower')
RENTbelow80 = df3.RentPct.quantile((.8), 'lower')

rent = df3['RentPct']

df3.Rent_Score.loc[rent <= RENTbelow20] = 1
df3.Rent_Score.loc[rent > RENTbelow20] = 2
df3.Rent_Score.loc[rent > RENTbelow40] = 3
df3.Rent_Score.loc[rent > RENTbelow60] = 4
df3.Rent_Score.loc[rent > RENTbelow80] = 5
df3.Rent_Score.loc[RentPct == 0] = 0

df3.to_csv(outF2)

#HOUSING VALUE
outF3 = downloadPath + '\HousingValue.csv'
with open(fname3, 'r') as inFile, open(outF3, 'w') as outFile:
    r = csv.reader(inFile)
    w = csv.writer(outFile)
    
    #read the header
    header = next(r)
    
    #change header titles
    header[1] = 'GEOID'
    header[3] = 'HouseVal'
    header[4] = 'HV_Score'
    
    w.writerow(header)
    #copy the rest of the data
    for row in r:
        w.writerow(row)

df97 = pd.read_csv(outF3, usecols = ['GEOID', 'HouseVal', 'HV_Score'], converters={'GEOID': lambda x: str(x)})
HouseVal = df97['HouseVal']

for h in HouseVal:
    if h == '-':
        df97.HouseVal.loc[HouseVal == ('-')] = 0
    if h == '10,000-':
        df97.HouseVal.loc[HouseVal == ('10,000-')] = 10000
    if h == '2,000,000+':
        df97.HouseVal.loc[HouseVal == ('2,000,000+')] = 2000000

df97.to_csv(outF3)
       
df4 = pd.read_csv(outF3, usecols = ['GEOID', 'HouseVal', 'HV_Score'], converters={'GEOID': lambda x: str(x)})

HVbelow20 = df4.HouseVal.quantile((.2), 'lower')
HVbelow40 = df4.HouseVal.quantile((.4), 'lower')
HVbelow60 = df4.HouseVal.quantile((.6), 'lower')
HVbelow80 = df4.HouseVal.quantile((.8), 'lower')

HV = df4['HouseVal']
HV_S = df4['HV_Score']
df4.HV_Score.loc[HV <= HVbelow20] = 5
df4.HV_Score.loc[HV > HVbelow20] = 4
df4.HV_Score.loc[HV > HVbelow40] = 3
df4.HV_Score.loc[HV > HVbelow60] = 2
df4.HV_Score.loc[HV > HVbelow80] = 1
df4.HV_Score.loc[HV == 0] = 0

df4.to_csv(outF3)

#EDUCATIONAL ATTAINMENT (Degree >= Bachelor's)
outF5 = downloadPath + '\Education.csv'
with open(fname4, 'r') as inFile, open(outF5, 'w') as outFile:
    r = csv.reader(inFile)
    w = csv.writer(outFile)
    
    #read the header
    header = next(r)
    header[1] = 'GEOID'
    
    w.writerow(header)
    #copy the rest of the data
    for row in r:
        w.writerow(row)

df5 = pd.read_csv(outF5, usecols = ['GEOID', 'HD01_VD22', 'HD01_VD23', 'HD01_VD24', 'HD01_VD25'], converters={'GEOID': lambda x: str(x)})
df5['CollegeDegree'] = df5['HD01_VD22'] + df5['HD01_VD23'] + df5['HD01_VD24'] + df5 ['HD01_VD25']

df5.to_csv(outF5)

df6 = pd.read_csv(outF5, usecols = ['GEOID', 'CollegeDegree'], converters={'GEOID': lambda x: str(x)})

df6.to_csv(outF5)

#Combine all csv's into one
outF4 = downloadPath + '\FINAL.csv'

dfs = [df1, df2, df3, df4, df6]

df_final = functools.reduce(lambda left,right: pd.merge(left,right,on='GEOID'), dfs)

#Calculate % of people with a Bachelor's Degree or higher
df_final['DegreePct'] = df6['CollegeDegree'] / df1['TotalPop']

DGbelow20 = df_final.DegreePct.quantile((.2), 'lower')
DGbelow40 = df_final.DegreePct.quantile((.4), 'lower')
DGbelow60 = df_final.DegreePct.quantile((.6), 'lower')
DGbelow80 = df_final.DegreePct.quantile((.8), 'lower')

df_final['Degree_Score'] = 0
DG = df_final['DegreePct']

df_final.Degree_Score.loc[DG <= DGbelow20] = 5
df_final.Degree_Score.loc[DG > DGbelow20] = 4
df_final.Degree_Score.loc[DG > DGbelow40] = 3
df_final.Degree_Score.loc[DG > DGbelow60] = 2
df_final.Degree_Score.loc[DG > DGbelow80] = 1

#Total all scores
df_final['TotalScore'] = df1['Score'] + df2['MI_Score'] + df3['Rent_Score'] + df4['HV_Score'] + df_final['Degree_Score']

#calculate number of scores for which there is data
df_final['Num_of_Values'] = 0

df_final.to_csv(outF4)

#Divide total score by number of actual score entries
df7 = pd.read_csv(outF4, converters={'GEOID': lambda x: str(x)})

div = df7['Num_of_Values']
Score = df1['Score']
Score2 = df2['MI_Score']
Score3 = df3['Rent_Score']
Score4 = df4['HV_Score']
Score5 = df_final['Degree_Score']

df7.Num_of_Values.loc[Score > 0] = div + 1
df7.Num_of_Values.loc[Score2 > 0] = div + 1
df7.Num_of_Values.loc[Score3 > 0] = div + 1
df7.Num_of_Values.loc[Score4 > 0] = div + 1
df7.Num_of_Values.loc[Score5 > 0] = div + 1

df7['AvgScore'] = (df7['TotalScore'] / df7['Num_of_Values'])

df7.to_csv(outF4)

df8 = pd.read_csv(outF4, usecols = ['GEOID', 'TotalPop', 'PctWhite', 'Score', 'MI', 'MI_Score', 'RentPct', 'Rent_Score', 'HouseVal', 'HV_Score', 'CollegeDegree', 'DegreePct', 'Degree_Score', 'TotalScore', 'AvgScore' ],converters={'GEOID': lambda x: str(x)})
df8.to_csv(outF4)
#read Block Groups shapefile
ifiles = [f for f in listdir(downloadPath) if isfile(join(downloadPath, f))]
for i in ifiles:
    if i.endswith(".shp"):
        ifile = downloadPath + "\\" + i

blockGroups = gpd.GeoDataFrame.from_file(ifile)

#converters={'GEOID': lambda x: str(x)} This stops Pandas from deleting leading 0 in census numbers
final = pd.read_csv(outF4, converters={'GEOID': lambda x: str(x)})

#Merge tabular data with geometry in that order
finalBG = pd.merge(final, blockGroups, on='GEOID')

#Save to new shapefile
outF5 = downloadPath + '\GentrificationSusceptibility.shp'

shapefile = gpd.GeoDataFrame(finalBG, geometry='geometry')

# proj WGS84
shapefile.crs= "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

shapefile.to_file(outF5, driver='ESRI Shapefile')

elapsed = (time.time() - start)

print('FINISHED!') 
print('A shapefile named "GentrificationSusceptibility.shp" can be found in your Downloads folder. It can be viewed using either ESRI ArcGIS or QuantumGIS (QGIS) software.')
print('The process took '+ str(elapsed) + ' seconds')
