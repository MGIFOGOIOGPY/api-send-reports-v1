from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_user_info(username):
    """استخراج معرف المستخدم بناءً على اسم المستخدم."""
    try:
        headers = {
            'Host': 'www.woodrowpoe.top',
            'Connection': 'keep-alive',
            'package': 'woodrowpoe.tik.realfans',
            'apptype': 'android',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; ANY-LX2 Build/HONORANY-L22CQ; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.124 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'version': '1.1',
            'Origin': 'http://www.woodrowpoe.top',
            'X-Requested-With': 'woodrowpoe.tik.realfans',
            'Referer': 'http://www.woodrowpoe.top//',
            'Accept-Language': 'ar-IQ,ar;q=0.9,en-IQ;q=0.8,en-US;q=0.7,en;q=0.6',
        }
        data = {'username': username}
        response = requests.post('http://www.woodrowpoe.top/api/v1/tikTokGetUserProfileInfo', headers=headers, data=data)
        
        if response.status_code == 200:
            response_data = response.json()
            if 'data' in response_data and 'pk' in response_data['data']:
                return response_data['data']['pk']
            return None
        return None
    except Exception as e:
        print(f"خطأ في استخراج معرف المستخدم: {e}")
        return None

def send_reports(user_id, count):
    """إرسال البلاغات بناءً على معرف المستخدم وعدد البلاغات المطلوب."""
    cookies = {
        'odin_tt': '40c40ad4772022e96afc8c9e5ce6440a94936ed1bd537e7879ee88784cfe22fca0848fe32c54174d839784124b12b8c27d20352b659177c2f833576358d3c1579c239bd3c573702ec998bbcd2e1e8878',
    }
    headers = {
        'Host': 'api16-normal-c-alisg.tiktokv.com',
        'User-Agent': 'com.zhiliaoapp.musically/2021306050 (Linux; U; Android 13; ar_IQ_#u-nu-latn; ANY-LX2; Build/HONORANY-L22CQ; Cronet/TTNetVersion:57844a4b 2019-10-16)',
    }
    results = []
    for i in range(count):
        try:
            response = requests.get(
                f'https://api16-normal-c-alisg.tiktokv.com/aweme/v2/aweme/feedback/?object_id={user_id}&owner_id={user_id}&report_type=user&reason=90061',
                cookies=cookies,
                headers=headers
            )
            if response.status_code == 200:
                results.append({'report_number': i + 1, 'status': 'success'})
            else:
                results.append({'report_number': i + 1, 'status': 'failed', 'status_code': response.status_code})
        except Exception as e:
            results.append({'report_number': i + 1, 'status': 'error', 'error_message': str(e)})
    return results

@app.route('/get_user_id', methods=['POST'])
def api_get_user_id():
    """واجهة API للحصول على معرف المستخدم."""
    data = request.get_json()
    username = data.get('username', '').strip()
    if not username:
        return jsonify({'error': 'اسم المستخدم مطلوب'}), 400
    user_id = get_user_info(username)
    if user_id:
        return jsonify({'user_id': user_id})
    return jsonify({'error': 'لم يتم العثور على معرف المستخدم'}), 404

@app.route('/send_reports', methods=['POST'])
def api_send_reports():
    """واجهة API لإرسال البلاغات."""
    data = request.get_json()
    user_id = data.get('user_id')
    count = data.get('count', 0)
    
    if not user_id or not isinstance(count, int) or count <= 0:
        return jsonify({'error': 'يجب توفير معرف المستخدم وعدد صحيح للبلاغات'}), 400
    
    results = send_reports(user_id, count)
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
