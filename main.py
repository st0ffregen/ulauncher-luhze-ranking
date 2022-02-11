from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction

import requests
from datetime import datetime
import json


class LuhzeRankingExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def add_newest_zeit_online_articles(self, items):
        url = build_url(self.feed)
        NewsFeed = feedparser.parse(url)


        for entry in NewsFeed.entries[:10]:

            if self.is_corona_ticker_and_maps_included == 'False' and entry.link in corona_ticker_and_maps_articles:
                continue

            if len(items) == 5:
                return

            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=entry.title,
                                             description=entry.description,
                                             on_enter=OpenUrlAction(entry.link)))


    def on_event(self, event, extension):
        items = []
        
        response = requests.get('https://stoffregen.io/luhzeStats/api/ranking?dateBackInTime=' + datetime.strftime(datetime.utcnow(), '%Y-%m-%d'))
        data = response.json()

        for rank in data[:5]:
            diff = str(rank['rankingScoreDiff'])
            if not diff.startswith('-'):
                diff = '+' + diff
                
            row = rank['name'] + '\t\t\t' + str(rank['rankingScore']) + '\t\t\t\t' + diff

            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=row,
                                             description='',
                                             on_enter=DoNothingAction()))


        return RenderResultListAction(items)


if __name__ == '__main__':
    LuhzeRankingExtension().run()