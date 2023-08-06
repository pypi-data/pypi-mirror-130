'''This module interacts with the HTML interface, allowing users to
        schedule updates to news articles and covid data'''
import sched
import time
import logging

from flask import Flask
from flask import render_template
from flask import request

from covid_data_handler import FORMAT
from covid_data_handler import get_config_data
from covid_data_handler import covid_API_request
from covid_news_handling import news_API_request
from covid_news_handling import update_news
from time_handler import seconds_to_set_time

app = Flask(__name__)

s = sched.scheduler(time.time, time.sleep)

logging.basicConfig(format=FORMAT,filename='system.log',level=logging.DEBUG)
config = get_config_data('config.json')

updates = []
removed_news = []

news = news_API_request()
live_covid_data = covid_API_request(config['location'],\
                                     config['location_type'])
nation_covid_data = covid_API_request(config['nation'], 'Nation')

logging.info('Program initialized')

def update_covid_data(time: str) -> dict:
    '''updates the live covid data
       arguments: time: a string containing the time the update should
                        trigger'''
    logging.debug('update_covid_data triggered')
    global live_covid_data, nation_covid_data
    live_covid_data = covid_API_request(config['location'],\
                                        config['location_type'])
    nation_covid_data = covid_API_request(config['nation'], 'Nation')
    for update in updates:
        if update['content'].find(time) != -1:
            if update['content'].find('repeated') == -1:
                updates.remove(update)
            else:
                logging.debug('data update scheduled')
                update = s.enter(seconds_to_set_time(time), 1,\
                                 update_covid_data, (time,))
    logging.info('Covid data updated')


def update_news_list(title: str, removed_news: list, time: str) -> list:
    '''updates the news articles stored in news
       arguments: title: string containg the title of the update
                  removed_news: list containg the titles of previously
                                removed news articles
                  time: a string containing the time the update should
                                trigger'''
    logging.debug('update_news_list triggered')
    global news
    news = update_news(title, removed_news)
    for update in updates:
        if update['content'].find(time) != -1:
            if update['content'].find('repeated') == -1:
                updates.remove(update)
            else:
                logging.debug('news update scheduled')
                update = s.enter(seconds_to_set_time(time), 1,\
                            update_news_list, (title, removed_news, time,))
    logging.info('News updated')

def schedule_updates(title, time, content):
    '''used to schedule updates to covid data, news or both
       arguments: title: string containing the title of the update
                  time: string containing the time for the update to occur
                  content: string containing details of the update'''
    logging.debug('schedule_update triggered')
    updates.append({
        'title': title,
        'content': content
        })

    if content.find('news') != -1:
        logging.debug('news update scheduled')
        update = s.enter(seconds_to_set_time(time), 1, update_news_list,\
                         (title, removed_news, time,))

    if content.find('covid data') != -1:
        logging.debug('data update scheduled')
        update = s.enter(seconds_to_set_time(time), 1, update_covid_data,\
                         (time,))

    logging.info('Update scheduled for ' + time)

@app.route('/index')
def main():
    '''interacts with the HTML interface, both passing and receiving data'''
    logging.debug('main triggered')
    s.run(blocking=False)

    text_field = request.args.get('two')
    update_time = request.args.get('update')
    update_news = request.args.get('news')
    update_data = request.args.get('covid-data')
    repeat = request.args.get('repeat')
    remove_update = request.args.get('update_item')
    remove_news = request.args.get('notif')

    if remove_update:
        for update in updates:
            if update['title'] == remove_update:
                updates.remove(update)
                logging.info('Covid data update cancelled')

    if remove_news:
        for article in news:
            if article['title'] == remove_news:
                removed_news.append(article['title'])
                news.remove(article)
                logging.info('News article removed')

    if text_field:
        update_content = ''
        if update_time:
            update_content = update_content + 'update scheduled for ' + \
                             str(update_time)
        if repeat:
            update_content = update_content + ' and will be repeated daily'
        if update_news:
            update_content = update_content + ' updating news'
        if update_data:
            update_content = update_content + ' updating covid data'

        schedule_updates(text_field, update_time, update_content)

    if seconds_to_set_time('00:00') % 21600 == 0:
        update_covid_data()
        logging.info('Covid data automatically updated')

    if seconds_to_set_time('00:00') % 14400 == 0:
        update_news_lists('automatic update', removed_news)
        logging.info('News articles automatically updated')

    return render_template('index.html',
                            title='TESTING',
                            image = 'image.jpg',
                            news_articles = news,
                            updates = updates,
                            location = config['location'],
                            local_7day_infections = \
                           live_covid_data['last7days_cases'],
                            nation_location = config['nation'],
                            national_7day_infections = \
                           nation_covid_data['last7days_cases'],
                            hospital_cases = \
                           live_covid_data['current_hospital_cases'],
                            deaths_total = live_covid_data['total_deaths']
                           )


if __name__ == '__main__':
    app.run()
