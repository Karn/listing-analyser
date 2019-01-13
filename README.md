## Listing Analyser
Create better Android Play Store App listings by figuring out what others are doing.

Scan Google Play listings for applications matching a search query and pull out keywords and their frequencies. This is particularly useful when you want to figure out what apps have high ratings and rating numbers and what keywords they use in their titles and descriptions. 

#### GETTING STARTED
You need to have Python installed as well as a number of secondary tools: `nltk`, `numpy`, and `play_scraper` (all of which can be installed using `pip`).


#### USAGE
The most basic case is as follows:

```Bash
./analyser -q "facebook tools" -f "com.facebook.katana,com.facebook.lite"
```

The output is stored as a markdown file within the `reports` directory.

#### CONTRIBUTING
There are many ways to [contribute](./.github/CONTRIBUTING.md), you can
- submit bugs,
- help track issues,
- review code changes.