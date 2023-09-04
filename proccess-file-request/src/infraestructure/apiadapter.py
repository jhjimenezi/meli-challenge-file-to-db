import requests

class ApiAdapter:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self, endpoint, key=None):
        url = f'{self.base_url}/{endpoint}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                data = data[0]
                if data['code'] == 200:
                    return data[key]
                else:
                    return None
            else:
                if key in data:
                    return data[key]
                else:
                    return None
        else:
            print('Error:', response.status_code)
    
    def get_item(self, item_id):
        item = self.get_data(f'items?ids={item_id}', 'body')
        return item
    
    def get_category_name(self, category_id):
        return self.get_data(f'categories/{category_id}', 'name')
    
    def get_currency_description(self, currency_id):
        return self.get_data(f'currencies/{currency_id}', 'description')
    
    def get_seller_nickname(self, seller_id):
        return self.get_data(f'users/{seller_id}', 'nickname')