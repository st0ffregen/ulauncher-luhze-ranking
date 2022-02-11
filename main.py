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


def format_row(rank):
    diff = str(rank['rankingScoreDiff'])
    if not diff.startswith('-'):
        diff = '+' + diff
                
    return rank['name'] + '\t\t' + str(rank['rankingScore']) + '\t\t\t\t' + diff


class LuhzeRankingExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def add_ranking_data(self, items):

        payload = {
            'dateBackInTime': datetime.strftime(datetime.utcnow(), '%Y-%m-%d')
        }

        response = requests.get('https://stoffregen.io/luhzeStats/api/ranking', params=payload)
        
        if response.status_code != 200:
            return
        
        data = response.json()

        for rank in data[:5]:
            
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=format_row(rank),
                                             description='',
                                             on_enter=DoNothingAction()))


    def add_single_ranking_data(self, items, name):
        
        payload = {
            'dateBackInTime': datetime.strftime(datetime.utcnow(), '%Y-%m-%d'),
            'name': name
        }
        
        response = requests.get('https://stoffregen.io/luhzeStats/api/singleRanking', params=payload)

        if response.status_code != 200:
            return

        data = response.json()

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=format_row(data),
                                         description='',
                                         on_enter=DoNothingAction()))


    def on_event(self, event, extension):
        items = []
        name = event.get_query()[6:] # remove beginning "luhze "

        if name:
            self.add_single_ranking_data(items, name)
        else:
            self.add_ranking_data(items)

        return RenderResultListAction(items)


if __name__ == '__main__':
    LuhzeRankingExtension().run()