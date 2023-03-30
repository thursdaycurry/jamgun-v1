# Job Hunting Machine

- Purpose : 이력서 지원 업무 자동화 
- Site : Intellipick

## News
- 2023-03-29 : basic scraping func success

## Issues Solved
- Scrap only 60 datas not all of the page(2023-03-30)

## Who need this?
- Job seekers who want to automate applying job
- Researcher who want to get job post statistics in the job platform

## How to use

### download
Simply download or git clone this repository.

### set environment file
create `.env` file in root directory and put your id, pw like below.
```
SPARTA_ID=<your-email>
SPARTA_PASSWORD=<your-password>
```

### driver
If driver-related problem occurs, make sure to use proper chromedriver. In this root directory, you will find chromedriver for mac arm64.  

Check driver that fits your browser's version(https://chromedriver.chromium.org/)
