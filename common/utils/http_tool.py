import requests


def http_get_url_params(url: str, params: str):
    url_path = url + "?" + params
    r = requests.get(url_path)
    return r.text


def http_get_url(url: str):
    url_path = url
    r = requests.get(url_path)
    return r.text


def http_post_json(url: str, params: str):
    url_path = url
    r = requests.post(url=url_path, json=params)
    r.headers['content-type'] = 'application/json; charset=utf-8'
    r.encoding = 'utf-8'
    return r.text


def http_post(url, params):
    r = requests.post(url, params)
    return r.text


if __name__ == '__main__':
    json_str = """
    {
	"category_id": "1",
	"main_question": "叫什么",
	"relate_questions": [{
		"question": "你叫什么名字？"
	}, {
		"question": "你是谁"
	}, {
		"question": "你是哪个"
	}, {
		"question": "你是谁啊"
	}, {
		"question": "叫啥"
	}],
	"answers": [{
		"answer": "小明的名字"
	}, {
		"answer": "我叫小明"
	}, {
		"answer": "小明2"
	}, {
		"answer": "小明3"
	}, {
		"answer": "小明5"
	}, {
		"answer": "小明6"
	}],

	"start_time": "2020-02-06 23:59:59",
	"end_time": "2020-02-06 23:59:59"
}
    """
    result = http_post_json(
        "http://localhost:8082/smart_qa/v2/open/knowledge/greeting/add", json_str)
    print(result)
