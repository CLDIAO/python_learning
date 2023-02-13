import requests
from bs4 import BeautifulSoup
import pandas as pd

# 请求获取网页数据
# 解析网页提取有价值数据
# 存储爬取的数据

f = open('movies.txt', 'w', encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                  'KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}

titles_csv, nums_csv, images_csv, intros_csv, ratings_csv, quotes_csv = [], [], [], [], [], []

# 自动翻页,共10页
for i in range(1, 11):
    url = 'https://movie.douban.com/top250?start=' + str((i-1)*25) + '&filter='
    data = requests.get(url, headers=headers)
    print(data.status_code)
    data_text = data.text

    soup = BeautifulSoup(data_text, 'lxml')
    movies = soup.find('ol', class_='grid_view').find_all('li')

    for movie in movies:
        movie_title = movie.find('div', class_='info').find('span', class_='title')
        movie_num = movie.find('div', class_='item').find('div', class_='pic').find('em')
        movie_url = movie.find('div', class_='item').find('a')
        movie_people = movie.find('div', class_='info').find('div', class_='bd').find('p')
        movie_rating = movie.find('div', class_='star').find('span', class_='rating_num')
        movie_quote = movie.find('div', class_='info').find('p', class_='quote')

        if all([movie_title, movie_num, movie_url, movie_people, movie_rating, movie_quote]):
            title = movie_title.text
            num = movie_num.text
            image = movie_url.get('href')
            intro = movie_people.text.strip()
            rating = movie_rating.get_text()
            quote = movie_quote.get_text().strip()

            # 输出txt文件
            f.write('\n'.join([
                ('影片名称：' + title + '\n'),  # title_txt,
                ('电影排名：' + num + '\n'),  # num_txt,
                ('电影评分：' + rating + '\n'),  # rating_txt,
                ('电影评论：' + '\t' + quote + '\n'),  # quote_txt,
                ('电影链接：' + '\t' + image + '\n'),  # image_txt,
                ('演职人员：' + '\n\t' + intro + '\n'),  # intro_txt,
                ('\n'+'******************************'+'\n'),
            ]))

            # for csv输出
            titles_csv.append(title)
            nums_csv.append(num)
            images_csv.append(image)
            intros_csv.append(intro)
            ratings_csv.append(rating)
            quotes_csv.append(quote)

        else:
            pass


if all([titles_csv, nums_csv, images_csv, intros_csv, ratings_csv, quotes_csv]):

    result = pd.DataFrame({
        '电影名称': titles_csv,
        '电影排名': nums_csv,
        '电影评分': ratings_csv,
        '电影评语': quotes_csv,
        '电影链接': images_csv,
        '演职人员': intros_csv,
        })

    # encoding参数修正中文乱码
    result.to_csv('Result.csv', index=False, encoding='utf_8_sig')
else:
    pass
