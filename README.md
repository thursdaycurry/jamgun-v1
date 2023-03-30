![Please-enter-a-title_-001](https://user-images.githubusercontent.com/87453411/228857059-6f2f4c79-bacf-43e0-b6da-6bb58c26abd1.png)

# Project JAMGUN
- Project : Sellenium-based job applying Python application
- Character name : 잼군(JAMGUN, Job-Application-Machine Gun)
- Purpose : Automate job applying job. Study CS more. 
- Site : job platform(Jumpit, Intellipick) in South Korea

## News
- 2023-03-29 : basic scraping func success
- 2023-03-30 : target site added(JUMPIT).

## Issues Solved
- Scrap only 60 datas not all of the page(2023-03-30) -> solved different type of condition for while loop 
- dataframe shows nothing(2023-03-30) -> fixed initiated twice to once  

## Who need this?
- Job seekers who want to automate applying job
- Researcher who want to get job post statistics in the job platform

## What can I do
- You can automate job application tasks(2023-03-30, Intellipick, Jumpit)
- You can get summary about jobs you applied in CSV file at `/data` directory.

## Check this out before using

### robots.txt
check '<target-website>/robots.txt' if it allows specific site to be scrapped.

### set environment file
create `.env` file in root directory and put your id, pw like below.
```
SPARTA_ID=<your-email>
SPARTA_PASSWORD=<your-password>
JUMPIT_ID=<your-email>
JUMPIT_PASSWORD=<your-password>
```

### get proper driver
If driver-related problem occurs, make sure to use proper chromedriver. In this root directory, you will find chromedriver for mac arm64.  

Check driver that fits your browser's version(https://chromedriver.chromium.org/)
