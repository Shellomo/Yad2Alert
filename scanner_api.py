import json
import os
import requests
# from settings import *
from settings_temp import *  # ToDo remove this
from publisher import Publisher
from s3_db_files import get_db_file, put_db_file


class Scanner:
    def __init__(self, project, test_mode=False):
        print('Starting scanner: ' + project['name'])
        self.project_name = project['name']
        self.pages_to_scan = project['pages_to_scan']
        self.urls = project['urls']
        self.alert_on_price_change = project['alert_on_price_change']
        self.telegram_channel = project['telegram_channel']
        self.fixed_urls = self.generate_urls()
        self.response = {}
        self.test = test_mode
        self.project_db_file_name = self.project_name + '.json'
        self.db = get_db_file(self.project_db_file_name)
        self.publisher = Publisher(self.telegram_channel)

    def generate_urls(self):
        urls = [u.replace('https://www.yad2.co.il/products/',
                          'https://gw.yad2.co.il/feed-search-legacy/products/') for u in self.urls]

        if self.pages_to_scan > 1:
            for page in range(2, self.pages_to_scan + 1):
                for url in urls:
                    urls.append(url + '&page=' + str(page))
        return urls

    def get_page_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            self.response = response.json()
        else:
            raise Exception('Error getting page: ' + url)

    def validate_page_content(self):
        if self.response == {}:
            print('Page content is empty')
            raise Exception('Page content is empty')

        elif not any(ad['type'] == 'ad' for ad in self.response['data']['feed']['feed_items']):
            print('no ads for this url')
            raise Exception('no ads for this url')
        else:
            return True

    def extract_ads(self):
        ads = []
        business_ads = 0
        ads_objects = self.response['data']['feed']['feed_items']
        if self.test:
            with open('ads.txt', 'w', encoding='utf8') as f:
                print('Writing ads to file')
                json.dump(ads_objects, f, ensure_ascii=False, indent=4)

        for ad_obj in ads_objects:
            if ad_obj['type'] != 'ad':
                continue

            ad = {}
            is_private = ad_obj['feed_source'] == 'private'
            if not is_private:
                business_ads += 1
                continue
            ad['id'] = ad_obj['id']
            print('Extracting ad: ' + ad['id'])
            ad['title'] = ad_obj['row_1']
            ad['description'] = ad_obj['search_text']
            ad['city'] = ad_obj['city']
            ad['product_condition'] = ad_obj['SaleCondition_text']
            ad['category_name'] = ad_obj['SalesSubCatID_text']
            ad['contact_name'] = ad_obj['contact_name']
            ad['price'] = ad_obj['price']
            ad['img_url'] = ad_obj['img_url']
            ad['all_item_images'] = ad_obj['images_urls']

            # delete img_url from all_item_images if exists
            if ad['img_url'] in ad['all_item_images']:
                ad['all_item_images'].remove(ad['img_url'])

            ads.append(ad)

        print('Found ' + str(len(ads)) + ' ads, ' + str(business_ads) + ' business ads')
        if len(ads) == 0:
            print('No ads found')

        return ads

    def scan(self):
        print('Scanning project: ' + self.project_name)
        new_ads = 0
        changed_price_ads = 0

        if self.test:
            print('Test mode is on')
            if not os.path.exists(os.path.join(self.project_name, 'page_content.txt')):
                with open(os.path.join(self.project_name, 'page_content.txt'), 'w',
                          encoding='utf8') as f:
                    self.get_page_content(self.urls)
                    json.dump(self.response, f, ensure_ascii=False, indent=4)
            with open(os.path.join(self.project_name, 'page_content.txt'), 'r', encoding='utf8') as f:
                self.response = json.load(f)

        for url in self.fixed_urls:
            self.get_page_content(url)

            self.validate_page_content()

            try:
                ads_dict = self.extract_ads()
                if len(ads_dict) == 0:
                    print('No ads found')
                    raise Exception('No ads found')
            except Exception as e:
                print(e)
                self.publisher.close()
                return

            for ad in ads_dict:
                if ad['id'] not in self.db:
                    new_ads += 1
                    print('Publishing new ad: ' + ad['id'])
                    is_publish = self.publisher.publish(ad)
                    if is_publish:
                        self.db[ad['id']] = ad

                # price changed alert

                elif ad['price'] != self.db[ad['id']]['price']:
                    changed_price_ads += 1
                    old_price = self.db[ad['id']]['price']
                    old_price = ''.join([s for s in old_price if s.isdigit()])
                    if old_price:
                        old_price = int(old_price)
                    else:
                        old_price = 0

                    new_price = ad['price']
                    new_price = ''.join([s for s in new_price if s.isdigit()])
                    if new_price:
                        new_price = int(new_price)

                    # user don't want to receive alerts on price change
                    if not self.alert_on_price_change:
                        continue

                    # nothing exciting to update
                    if not new_price:
                        continue

                    if old_price > new_price:

                        print(f'Publishing ad {ad["id"]}, with new price: {ad["price"]}')
                        is_publish = self.publisher.publish(ad, new_price=True)
                        if is_publish:
                            self.db[ad['id']] = ad

        self.publisher.close()
        print('Found ' + str(new_ads) + ' new ads')

        # save db
        print('Saving db')
        put_db_file(self.project_db_file_name)


if __name__ == '__main__':
    project = {
        'name': 'test',
        'url': 'https://www.yad2.co.il/products/furniture?category=2',
        'pages_to_scan': 1,
        'test': True

    }
    scanner = Scanner(project, test_mode=True)
    scanner.scan()
