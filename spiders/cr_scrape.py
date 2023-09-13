import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urlencode

class MySpider(scrapy.Spider):
    name = 'cr_scrape'

    def start_requests(self):
        login_url = 'https://www.cr.lt/'
        login_data = {
            'username': 'popo00',
            'password': '3t52HCC',
        }
        login_data_encoded = urlencode(login_data)

        
        yield SplashRequest(
            login_url,
            self.parse_login,
            endpoint='render.html',  
            args={
                'wait': 5,  
                'html': 1,   
            body=login_data_encoded  
        )

    def parse_login(self, response):
        
        if 'Atsijungti' in response.text:
            print('Log In Successful!')
            with open('login_html.html', 'w', encoding='utf-8') as file:
                file.write(response.text)

          
            search_query = '305485432'

      
            search_url = 'https://www.cr.lt/imones/n/noriu/search/'

            #cookies = {}
            #for set_cookie in response.headers.getlist('Set-Cookie'):
            #    key, value = set_cookie.decode('utf-8').split('=', 1)
            #    cookies[key] = value.split(';')[0]

            
            yield SplashRequest(
                search_url,
                self.parse_search_results,
                endpoint='render.html', 
                args={
                    'wait': 5, 
                    'html': 1,   
                    'lua_source': self.get_search_script(search_query), 
                }
                #cookies=cookies
            )
        else:
            print('Log In Unsuccessful')

    def get_search_script(self, query):
        # Lua script to fill out and submit the search form
        script = f"""
        function main(splash)
            splash:go(splash.args.url)
            splash:wait(5)
            local search_input = splash:select('input[name="Company"]')  
            local search_button = splash:select('btn.btn-success')  
            search_input:send_text("{query}")
            search_button:mouse_click()
            splash:wait(5)
            return splash:html()
        end
        """
        return script

    def parse_search_results(self, response):
        

        with open('search_html.html', 'w', encoding='utf-8') as file:
                file.write(response.text)
        
        
        
       

       