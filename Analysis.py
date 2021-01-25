import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)

import time
import datetime
import requests
import re
import json
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns
import torch
import flair
import nltk
# import stemmer
from nltk.stem import SnowballStemmer
from nltk.stem.snowball import DutchStemmer
from gensim import corpora

def clean_string(column):
    return column.apply(lambda x: x.replace("\n",' ',2)).apply(lambda x: x.replace('  ',' '))

def scrape_reviews(PATH, n_pages, sleep_time = 0.3):

    names = []
    ratings = []
    headers = []
    reviews = []
    dates = []
    locations = []

    for p in range(n_pages):

        time.sleep(sleep_time)

        http = requests.get(f'{PATH}{p}')
        bsoup = BeautifulSoup(http.text, 'html.parser')

        review_containers = bsoup.find_all('div', class_ = 'review-content__body')
        user_containers = bsoup.find_all('div', class_ = 'consumer-information__name')
        rating_container = bsoup.find_all('div',class_ = "star-rating star-rating--medium")
        date_container = bsoup.find_all('div',class_ = "review-content-header__dates")
        for d in date_container:
            dates.append(datetime.datetime.strptime(d.text[20:30], '%Y-%m-%d').date())
        for x in range(len(review_containers)):
            try:
                review_c = review_containers[x]
                headers.append(review_c.h2.a.text)
                reviews.append(review_c.p.text)
                reviewer = user_containers[x]
                names.append(reviewer.text)
                rating = rating_container[x]
                ratings.append(rating.img.attrs['alt'])

            #dates.append(datetime.datetime.strptime(date.attrs['datetime'][0:10], '%Y-%m-%d').date())
            except:
                pass



    rev_df = pd.DataFrame(list(zip(headers, reviews, ratings, names, dates)),
                  columns = ['Header','Review','Rating', 'Name', 'Date'])

    rev_df.Review = clean_string(rev_df.Review)
    rev_df.Name = clean_string(rev_df.Name)
    #rev_df.Location = clean_string(rev_df.Location)
    #rev_df.Location = rev_df.Location.apply(lambda x: x.split(',',1)[-1])
    #rev_df.Rating = rev_df.Rating.astype('int')
    rev_df.Date = pd.to_datetime(rev_df.Date)

    return rev_df
In [3]:
Bol= scrape_reviews(PATH = 'https://www.trustpilot.com/review/www.bol.com?languages=nl&page=',
                   n_pages = 1151 )
Bol.to_csv(r'Bol.csv')



In [63]:
Bol_word = Bol.explode('Word')
aa = Bol_word.groupby('Rating')['Word'].value_counts().unstack().fillna(0).T
aaa = aa['1 star: Bad'].sort_values(ascending = False).head(13).to_frame()[3:14]
bbb = aa['2 stars: Poor'].sort_values(ascending = False).head(13).to_frame()[3:14]
ccc = aa['3 stars: Average'].sort_values(ascending = False).head(13).to_frame()[3:14]
ddd = aa['4 stars: Great'].sort_values(ascending = False).head(13).to_frame()[3:14]
eee = aa['5 stars: Excellent'].sort_values(ascending = False).head(13).to_frame()[3:14]
In [64]:
sns.set_style("darkgrid")
sns.set_palette("husl")

f, axes = plt.subplots(2, 3, figsize=(14, 7), sharex=False)
f.delaxes(axes[1,2])


sns.barplot(data = aaa, y =aaa.index, x=aaa['1 star: Bad'], color="pink", orient = "h", ax=axes[0, 0])
sns.barplot(data = bbb, y =bbb.index, x=bbb['2 stars: Poor'], color="brown", orient = "h", ax=axes[0, 1])
sns.barplot(data = ccc, y =ccc.index, x=ccc['3 stars: Average'], color="green", orient = "h", ax=axes[0, 2])
sns.barplot(data = ddd, y =ddd.index, x=ddd['4 stars: Great'], color="cyan", orient = "h", ax=axes[1, 0])
sns.barplot(data = eee, y =eee.index, x=eee['5 stars: Excellent'], color="lightblue", orient = "h", ax=axes[1, 1])

for ax in axes.flatten():
    ax.set_ylabel('')
plt.tight_layout()


Bol['YearMonth'] = pd.to_datetime(Bol['Date']).apply(lambda x: '{year}-{month}'.format(year=x.year, month=x.month))
a = Bol.groupby('YearMonth')['Rating'].value_counts().unstack().fillna(0)
a = a.set_index(pd.to_datetime(a.index)).sort_index()
sns.set_style("darkgrid")
sns.set_palette("husl")
a.plot(kind='line', figsize=(17, 5))
plt.legend(loc='upper left')
Out[78]:
<matplotlib.legend.Legend at 0x7fdd9c21bad0>
