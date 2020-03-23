#!/usr/bin/env python3.8
# -*- coding : utf-8 -*-
from discord_webhook import DiscordWebhook, DiscordEmbed
import bs4
import requests
import time

# lien vers RSS de RuneScape français.
rss_url = "https://secure.runescape.com/m=news/l=2/a=13/latest_news.rss"
# lien du webhook discord.
webhook_url = ""
# Icône auteur dans les posts.
icon_url = ""


def _get_text(text):
    """ Retirer le formattage XML """
    ret = text.get_text().strip("\n")
    return ret


def send_to_webhook(list_elements):
    """ Publier les éléments sur Discord """
    webhook = DiscordWebhook(url=webhook_url)
    emb = DiscordEmbed(
        title=list_elements[0],
        description=list_elements[2],
        url=list_elements[1],
        color=237
    )

    emb.set_author(
        name='RuneScape News',
        icon_url=icon_url
    )
    emb.set_footer(
        text=list_elements[3]
    )
    emb.set_image(
        url=list_elements[4]
    )
    webhook.add_embed(emb)
    webhook.execute()


def _get_rss_posts():
    """ Copie la page RSS et sépare les posts """
    rss_posts = []
    rss_page = requests.get(rss_url)
    soup = bs4.BeautifulSoup(rss_page.text, features="lxml")
    for item in soup.find_all("item"):
        titre = _get_text(item.find("title"))
        lien = _get_text(item.find('guid'))
        description = _get_text(item.find('description'))
        categorie = _get_text(item.find('category'))
        image = ""
        if item.find('enclosure') is not None:
            image = item.find('enclosure')['url']
        list1 = [titre, lien, description, categorie, image]
        rss_posts.append(list1)
    return rss_posts


# Vérifier les anciennes données avec les nouvelles.
# 15 mins d'intervale
old = _get_rss_posts()[:10]
print("Program as started")
while True:
    new = _get_rss_posts()[:3]
    for num, val in enumerate(new):
        if val in old:
            pass
        else:
            old.insert(num, val)
            old.pop()
            send_to_webhook(val)
            print("A RSS post have been sent to Discord.")
    time.sleep(900)
