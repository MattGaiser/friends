# name is name="user[email]"
# name is user[password]
# token is Q9/+/MO2P3t7LBw1BQG2IAepZ/fdw54X2vmmp9dRi1Gc77aR6SifP/T86H23tMlXA5oxDTFPh/fXlcJTcU1tlg==
import requests
from lxml import html

session_requests = requests.session()

login_url = "https://www.mindsumo.com/login"
result = session_requests.get(login_url)
print(result)
tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//meta[@name='csrf-token']/@content")))[0]
print(authenticity_token)

payload = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0',
    "user[email]" : "13mdg5@queensu.ca",
    "user[password]": "fauj848",
    "csrf-token": str(authenticity_token)
}
result = session_requests.post(
	login_url,
	data = payload,
	headers = dict(referer=login_url)
)
print(result);
url = 'https://www.mindsumo.com/user/13mdg5?sort=rating'
result = session_requests.get(
	url,
	headers = dict(referer = url)
)
tree = html.fromstring(result.content)
#bucket_names = tree.xpath("//div[@class='repo-list--repo']/a/text()")
print(tree)

