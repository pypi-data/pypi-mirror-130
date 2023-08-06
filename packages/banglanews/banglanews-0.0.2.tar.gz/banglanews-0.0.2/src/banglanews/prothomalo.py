import      json
import      time
import      math
import      pathlib
import      urllib.parse
from        urllib.parse import quote
from        urllib.request import urlopen, Request
from        datetime import datetime, timedelta
from        base64 import b64encode

class scraper:

    def __init__(self, start_date = None, end_date = None, output_dir = None):
        if start_date == None:
            raise Exception("start_date is not specified.")
        elif end_date == None:
            raise Exception("end_date is not specified.")
        elif output_dir == None:
            raise Exception("output_dir is not specified.")

        self.start_date = start_date
        self.end_date = end_date
        self.output_dir = output_dir
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    def UnixToDate(self, unix_date):
        regular_date = datetime.fromtimestamp(int(unix_date)/1000)
        return regular_date.strftime('%Y-%m-%d')

    def DateToUnix(self, regular_date):
        time_tuple = time.mktime(datetime.strptime(regular_date, '%Y-%m-%d').timetuple())*1000
        unix_date = math.floor(time_tuple) #we don't want anything after the decimal point
        return unix_date
    
    def StringToDate(self, date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%d')
        return date_object

    def GetURLInfo(self, start_date, end_date,  offset, limit, search_text='', fetch_content=False):
        base_url = 'https://www.prothomalo.com/api/v1/advanced-search?'
        
        if(search_text.strip()==''):
            if fetch_content:
                api_url = base_url + 'fields=headline,url,published-at,cards&offset=' + str(offset) + '&limit=' + str(limit) + '&sort=latest-published&published-after=' + str(self.DateToUnix(start_date)) + '&published-before=' + str(self.DateToUnix(end_date))    
            else:
                api_url = base_url + 'fields=headline,url,published-at&offset=' + str(offset) + '&limit=' + str(limit) + '&sort=latest-published&published-after=' + str(self.DateToUnix(start_date)) + '&published-before=' + str(self.DateToUnix(end_date))    
        else:
            if fetch_content:
                api_url = base_url + 'fields=headline,url,published-at,cards&offset=' + str(offset) + '&limit=' + str(limit) + '&sort=latest-published&published-after=' + str(self.DateToUnix(start_date)) + '&published-before=' + str(self.DateToUnix(end_date)) + '&q=' + quote(search_text)   
            else:
                api_url = base_url + 'fields=headline,url,published-at&offset=' + str(offset) + '&limit=' + str(limit) + '&sort=latest-published&published-after=' + str(self.DateToUnix(start_date)) + '&published-before=' + str(self.DateToUnix(end_date)) + '&q=' + quote(search_text)   

        try:
            request = Request(url=api_url, headers=self.headers)
            response = urlopen(request).read()
            json_data = json.loads(response)
            url_count = json_data['total']
            url_items = json_data['items']
            return url_count, url_items
        except:
            pass

    def GetDateSegments(self, start_date, end_date, search_text='', fetch_content=False):
        date_list = []
        dummy_var = None
        max_url_fetch_count = 10000

        total_url_count, dummy_var = self.GetURLInfo(start_date, end_date, 0, 1, search_text, fetch_content)

        print('Estimated total URL found in the given criteria: ' + str(total_url_count))
        
        first_date = datetime.strptime(start_date,'%Y-%m-%d')
        last_date = datetime.strptime(end_date,'%Y-%m-%d') 
        total_days = (last_date - first_date).days

        if fetch_content == True:

                max_days_split_size = 1

                next_date = first_date
                date_list.append(next_date.strftime('%Y-%m-%d')) 
                for day_loop in range(0, total_days, max_days_split_size):
                    next_date = next_date + timedelta(days=max_days_split_size)
                    date_list.append(next_date.strftime('%Y-%m-%d')) 
                
                last_listed_date = self.StringToDate(date_list[len(date_list) - 1]) 
                if last_listed_date < last_date:
                    remaining_days = (last_date - last_listed_date).days 
                    next_date = last_listed_date + timedelta(days=remaining_days)
                    date_list.append(next_date.strftime('%Y-%m-%d'))
                else:
                    date_list.pop()
                    date_list.append(last_date.strftime('%Y-%m-%d'))
        else:
            if total_url_count > max_url_fetch_count:

                avg_url_count_perday = total_url_count / total_days
                max_days_split_size = max_url_fetch_count / avg_url_count_perday
                max_days_split_size = math.floor(max_days_split_size/2)

                next_date = first_date
                date_list.append(next_date.strftime('%Y-%m-%d')) 
                for day_loop in range(0,total_days,max_days_split_size):
                    next_date = next_date + timedelta(days=max_days_split_size)
                    date_list.append(next_date.strftime('%Y-%m-%d')) 
                
                last_listed_date = self.StringToDate(self, date_list[len(date_list) - 1]) 
                if last_listed_date < last_date:
                    remaining_days = (last_date - last_listed_date).days 
                    next_date = last_listed_date + timedelta(days=remaining_days)
                    date_list.append(next_date.strftime('%Y-%m-%d'))
                else:
                    date_list.pop()
                    date_list.append(last_date.strftime('%Y-%m-%d'))
            else:
                date_list.append(start_date)
                date_list.append(end_date)

        return date_list

    def GetURLList(self, start_date, end_date, search_text=''):

        process_start_time = datetime.now().strftime('%H:%M:%S')

        url_list = []
        headline_list = []
        published_date_list = []

        print('Calculating batch process size...')
        date_segments = self.GetDateSegments(start_date, end_date, search_text)
        print('Calculating batch process size done.')

        print('Process started...')
        try:
            if len(date_segments) == 2:
                url_count, dummy_var = self.GetURLInfo(start_date, end_date, 0, 1, search_text)
                print('URL found : ' + str(url_count))
                total_url_count, url_items = self.GetURLInfo(start_date, end_date, 0, url_count, search_text)
                for item in url_items:
                    content = ''
                    url_list.append(item['url'])
                    headline_list.append(item['headline'])
                    published_date_list.append(self.UnixToDate(str(item['published-at'])))
            else:
                for date_part_loop in range(len(date_segments)-1):

                    print('Processing batch job ' + str(date_part_loop+1) + ' out of ' + str(len(date_segments)) + ' : at ' + str(datetime.today().strftime("%I:%M:%S %p")))
                    next_start_date = date_segments[date_part_loop]

                    total_url_count, dummy_var = self.GetURLInfo(next_start_date, date_segments[date_part_loop + 1], 0, 1, search_text)
                    print('URL found in this batch: ' + str(total_url_count))

                    dummy_var, url_items = self.GetURLInfo(next_start_date, date_segments[date_part_loop + 1], 0, total_url_count, search_text)

                    for item in url_items:
                        content = ''
                        url_list.append(item['url'])
                        headline_list.append(item['headline'])
                        published_date_list.append(self.UnixToDate(str(item['published-at'])))
        except:
            pass

        process_end_time = datetime.now().strftime('%H:%M:%S')

        print('Process done.')
        print('Time elapsed: ' + str(datetime.strptime(process_end_time, '%H:%M:%S') - datetime.strptime(process_start_time, '%H:%M:%S')))

        return url_list, headline_list, published_date_list


    def GetCommentList(self, start_date, end_date,search_text=''):
        
        comments = []           # List to hold comments
        headlines = []          # List to hold headlines of the news article that shows the corresponding comments
        urls = []               # List to hold the URLs of the news article corresponding to the comments
        comment_dates = []      # List to hold comment dates
        
        process_start_time = datetime.now().strftime('%H:%M:%S')

        base_url = 'https://www.metype.com/api/v1/accounts/1000444/pages/'

        print('Getting URL list...')
        url_list, dummy_var1, dummy_var2 = self.GetURLList(start_date, end_date, search_text)    

        tot_urls_count = len(url_list)
        print('Getting URL list Done.')

        url_process_count = 0
        
        print('Processing Comments started...')
        for page_url in url_list:
            # Before calling the mettype API to get the comments, the following encoding is required.
            encoded_url = urllib.parse.quote(page_url,safe='~()*!.%\'')
            encoded_byte = b64encode(bytes(encoded_url, 'utf-8'))
            decoded_text = encoded_byte.decode("utf-8")
            comment_count = 0
            url_process_count += 1

            # Now making the API URL
            comment_count_api_url = base_url + str(decoded_text) + '/comments.json?parent_comments_limit=0'

            try:
                # First we are hitting the URL just with very basic params to get the counts of the comments in an URL 

                request = Request(url=comment_count_api_url, headers=self.headers)
                response = urlopen(request).read()
                json_data = json.loads(response)            
                total_comment_count = json_data['total_count'] # We got the comments count

                # Now build the URL to get all comments according to the total comment count
                if total_comment_count is not None and total_comment_count>0:
                    api_url = base_url + str(decoded_text) + '/comments.json?parent_comments_limit=' + str(total_comment_count) + '&parent_comments_offset=0&sort_order=desc&child_comments_sort_order=asc'

                    request = Request(url=api_url, headers=self.headers)
                    response = urlopen(request).read()
                    json_data = json.loads(response)            
                    comment_sections = json_data['comments']
                    comment_count = len(comment_sections)

                    if comment_count > 0:                                                       # Checking if the URL conatains any comment
                        for comment_section in comment_sections:
                            if 'body' in comment_section:                                       # Sometimes there is no comment found, so first check that
                                comments.append(comment_section['body']['ops'][0]['insert'])    # This JSON path contains the comment
                                headlines.append(comment_section["headline"])                   # This JSON path contains the headline
                                urls.append(comment_section["page_url"])                        # This JSON path contains the URL
                                comment_dates.append(comment_section["created_at"])             # This JSON path contains the date           
                print('Processing url ' + str(url_process_count) + ' out of ' + str(tot_urls_count) + ' : Comments found ' + str(comment_count) + ' : at ' + str(datetime.today().strftime("%I:%M:%S %p")))
            except Exception as ex:
                print(ex)
                pass    # If any exception occurs we'll skip to the next URL processing
        
        print('Processing comments completed.')
        process_end_time = datetime.now().strftime('%H:%M:%S')
        print('Time elapsed: ' + str(datetime.strptime(process_end_time, '%H:%M:%S') - datetime.strptime(process_start_time, '%H:%M:%S')))

        return comments, headlines, urls, comment_dates


    def PrintContents(self, search_text=''):

        process_start_time = datetime.now().strftime('%H:%M:%S')

        print('Calculating batch process size...')
        date_segments = self.GetDateSegments(self.start_date, self.end_date, search_text, True)
        print('Calculating batch process size done.')

        print('Process started...')
        if len(date_segments) == 2:
            url_count, dummy_var = self.GetURLInfo(self.start_date, self.end_date, 0, 1, search_text)
            print('URL found : ' + str(url_count))

            total_url_count, url_items = self.GetURLInfo(self.start_date, self.end_date, 0, url_count, search_text, True)

            for item in url_items:
                headline = item['headline'].replace('?','').replace('\\','').replace('/','').replace('*','').replace(':',' ').replace('|','').replace('\n','').replace('\r','')
                if len(headline) > 50:
                    headline = headline[:47] + '...'
                if self.output_dir[-1] != '\\':
                    self.output_dir = self.output_dir + '\\'
                pathlib.Path(self.output_dir).mkdir(parents=True, exist_ok=True)

                filename = self.output_dir + '[CONTENT]-' + '[' + self.UnixToDate(str(item['published-at'])) + ']-[' + headline + '].txt'
                
                f = open(filename, 'w', encoding='utf-8')

                content = ''
                f.write(item['headline'] + '\n')
                f.write(self.UnixToDate(str(item['published-at'])) + '\n')
                f.write(item['url'] + '\n')
                f.write(str('-' * len(item['url'])) + '\n\n')

                for card in item['cards']:
                    for story_element in card['story-elements']:
                        if 'text' in story_element:
                            story_segment = story_element['text'] 
                            if story_segment[0:4].strip() == '<h2>':
                                sub_headline_ends =  story_segment.index('</h2>')
                                sub_headline = story_segment[0:sub_headline_ends + 5]
                                story_segment = story_segment.replace(sub_headline,'')
                            if  story_segment[0:3].strip() == '<p>':                     
                                content = content + story_segment.replace('<p>','').replace('</p>','').replace('<br>','')
                    f.write(content)
                f.close()

        else:
            for date_part_loop in range(len(date_segments)-1):

                print('Processing batch job ' + str(date_part_loop+1) + ' out of ' + str(len(date_segments)) + ' : at ' + str(datetime.today().strftime("%I:%M:%S %p")))
                next_start_date = date_segments[date_part_loop]

                total_url_count, dummy_var = self.GetURLInfo(next_start_date, date_segments[date_part_loop + 1], 0, 1, search_text)
                print('URL found in this batch: ' + str(total_url_count))

                dummy_var, url_items = self.GetURLInfo(next_start_date, date_segments[date_part_loop + 1], 0, total_url_count, search_text, True)

                for item in url_items:
                    headline = item['headline'].replace('?','').replace('\\','').replace('/','').replace('*','').replace(':',' ').replace('|','').replace('\n','').replace('\r','')
                    if len(headline) > 50:
                        headline = headline[:47] + '...'
                    if self.output_dir[-1] != '\\':
                        self.output_dir = self.output_dir + '\\'

                    filename = self.output_dir + '[CONTENT]-' + '[' + self.UnixToDate( str(item['published-at'])) + ']-[' + headline + '].txt'
                    f = open(filename, 'w', encoding='utf-8')
                    content = ''
                    f.write(item['headline'] + '\n')
                    f.write(self.UnixToDate(str(item['published-at'])) + '\n')
                    f.write(item['url'] + '\n')
                    f.write(str('-' * len(item['url'])) + '\n\n')
                    for card in item['cards']:
                        for story_element in card['story-elements']:
                            if 'text' in story_element:
                                story_segment = story_element['text'] 
                                if story_segment[0:4].strip() == '<h2>':
                                    sub_headline_ends =  story_segment.index('</h2>')
                                    sub_headline = story_segment[0:sub_headline_ends + 5]
                                    story_segment = story_segment.replace(sub_headline,'')
                                if  story_segment[0:3].strip() == '<p>':                     
                                    content = content + story_segment.replace('<p>','').replace('</p>','').replace('<br>','')
                        f.write(content)
                    f.close()

        process_end_time = datetime.now().strftime('%H:%M:%S')

        print('Process done.')
        print('Time elapsed: ' + str(datetime.strptime(process_end_time, '%H:%M:%S') - datetime.strptime(process_start_time, '%H:%M:%S')))



    def PrintURLs(self, search_text=''):

        urls = []
        headline = []
        publishdates = []

        urls, headline, publishdates =  self.GetURLList(self.start_date, self.end_date, search_text) 

        if self.output_dir[-1] != '\\':
            self.output_dir = self.output_dir + '\\'
        pathlib.Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        file_name = self.output_dir + '[URL]_[' + str(self.start_date) + ']_TO_[' + str(self.end_date) + '].csv'

        with open(file_name, "w", encoding="utf-8") as f:
            f.write('ID|Headline|URL|Published Date\n')
            try:
                for position in range(len(urls)):
                    f.write(str(position + 1) + '|'  + headline[position].replace('\n',' ').replace('\r','').replace('|',' ') + '|' + urls[position] + '|' + publishdates[position] + '\n')
            except Exception as ex:
                print(ex)
                pass



    def PrintComments(self, search_text=''):

        comment_list, headline_list, url_list, comment_date_list = self.GetCommentList(self.start_date, self.end_date, search_text)

        if self.output_dir[-1] != '\\':
            self.output_dir = self.output_dir + '\\'
        pathlib.Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        file_name = self.output_dir +  '[COMMENTS]_[' + self.start_date + ']_To_[' + self.end_date + ']_[' + search_text + '].csv'

        with open(file_name, "w", encoding="utf-8") as f:
            f.write('ID|Comment|Headline|URL|Date\n')
            comment_id = 0
            for comment in comment_list:
                comment = str(comment)
                if (comment is not None) and ("{'mentions': True}" not in comment):
                    comment_date_part = str(comment_date_list[comment_id-1]).split('T')
                    try:
                        f.write(str(comment_id + 1) + '|' + comment.replace('|','।').replace('"','').replace('\n',' ').replace('\r','') + '|' + headline_list[comment_id-1].replace('|','।').replace('\n',' ').replace('\r','') + '|' + url_list[comment_id-1] + '|' + comment_date_part[0] + '\n')
                        comment_id += 1
                    except Exception as ex:
                        print(ex)
                        pass