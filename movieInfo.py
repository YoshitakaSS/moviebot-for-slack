import requests;
from bs4 import BeautifulSoup;
import json;

# 映画情報サイトのURL
rootUrl = "https://eiga.com";

# 映画情報一覧画面のURL
movieListUrl = "https://eiga.com/now/";

# slack-webhock-urlを入力
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
	text += "ポスター画像：" + str(botContent[3]) + '\n';
	requests.post(webhokckUrl, data = json.dumps({
			'text': text,
			'username': 'movie-bot',
		}));

def getReview(soup):
	rv = soup.find(class_="rv");
	review = rv.find('strong').string;
	return review;

def getPosterImg(soup):
	imgInfo = soup.find(class_="pictBox");
	img = imgInfo.find('img')['src'];
	return img;


# 映画の詳細情報（レビュー、ポスター画像を取得する）
def getDetailInfo(detailUrl):
	detailres = requests.get(detailUrl);
	soup = BeautifulSoup(detailres.text, "html.parser");
	# レビューの取得 # ポスターの取得
	return {
		"review" : getReview(soup), 
		"posterImg" : getPosterImg(soup),
	};


# 映画情報を取得する
def getContent(contents):
	for content in contents:	
			title = content.find('h3').string;
			link = content.find('a').get('href');
			detailUrl = rootUrl + link;
			detailInfo = getDetailInfo(detailUrl);
			review = detailInfo['review'];
			posterImg = detailInfo['posterImg'];
			botContent = [title, detailUrl, review, posterImg];
			
			# Logに出力
			print("###########################");
			print("映画タイトル：" + title);
			print("詳細URL：" + detailUrl);
			print("レビュー：" + review);
			print("ポスター画像：" + posterImg);

			postSlack(webhokckUrl, botContent);

print("今週の映画情報を紹介します");
getContent(contents);

