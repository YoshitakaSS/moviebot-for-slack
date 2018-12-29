import requests;
from bs4 import BeautifulSoup;
import json;

# 映画情報サイトのURL
rootUrl = "https://eiga.com";

# 映画情報一覧画面のURL
movieListUrl = "https://eiga.com/now/";

# slack-webhock-url入力
webhokckUrl = "";


res = requests.get(movieListUrl);

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(res.text, "html.parser");

# 映画コンテンツを取得する
contents = soup.find_all(class_="m_unit");

# slackに送るように枠だけ作成
title = '';
detailUrl = '';
review = '';

# slackに送る
def postSlack(webhokckUrl, botContent):
	text = "映画タイトル：" + str(botContent[0]) + '\n';
	text += "詳細URL：" + str(botContent[1]) + '\n';
	text += "レビュー：" + str(botContent[2]) + '\n';
	requests.post(webhokckUrl, data = json.dumps({
			'text': text,
			'username': 'movie-bot',
		}));

# レビューを取得する
def getReview(detailUrl):
	detailres = requests.get(detailUrl);
	soup = BeautifulSoup(detailres.text, "html.parser");
	rv = soup.find(class_="rv");
	review = rv.find('strong').string;
	return review;

# 映画情報を取得する
def getContent(contents):
	for content in contents:	
		title = content.find('h3').string;
		link = content.find('a').get('href');
		detailUrl = rootUrl + link;
		review = getReview(detailUrl);
		botContent = [title, detailUrl, review];
		
		# Logに出力
		print("###########################");
		print("映画タイトル：" + title);
		print("詳細URL：" + detailUrl);
		print("レビュー：" + review);

		postSlack(webhokckUrl, botContent);

print("今週の映画情報を紹介します");
getContent(contents);

