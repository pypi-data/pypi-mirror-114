"""
MIT License
Copyright (c) 2021 Samuel Cheng
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import requests as r
import random
import json


# Utilities
class Utilities:
    def __init__(self):
        pass
    # easy_api.Utilities().url_shortener({url})
    def url_shortener(self, url):
        return r.get(f"https://tinyurl.com/api-create.php?url={url}").text
    # easy_api.Utilities().uuid_generator(*{count})
    def uuid_generator(self, *args):
        if not args:
            count = 1
        else:
            count = int(args[0])
        uuid = json.loads(r.get(f"https://www.uuidtools.com/api/generate/v1/count/{count}").text)
        
        if count == 1:
            return uuid[0]
        elif count > 1:
            return uuid
        



# ANIMALS
class Animals:
    def __init__(self):
        pass
    # easy_api.Animals().cat_facts()
    def cat_facts(self):
        return r.get("https://catfact.ninja/fact").text
    # easy_api.Animals().cat_random()
    def cat_random(self):
        return r.get("https://aws.random.cat/meow").text
    # easy_api.Animals().dog_random()
    def dog_random(self):
        return r.get("https://random.dog/woof.json").text


# FUN
class Fun:
    def __init__(self):
        pass
    # easy_api.Fun().dad_jokes()
    def dad_jokes(self):
        return r.get("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"}).text
    # easy_api.Fun().yes_or_no()
    def yes_or_no(self):
        return r.get("https://yesno.wtf/api").json()


# WAIFU
# https://github.com/weeebdev/waifu.pics
class Waifu:
    def __init__(self):
        self.sfw_types = [
        'waifu',
        'neko',
        'shinobu',
        'megumin',
        'bully',
        'cuddle',
        'cry',
        'hug',
        'awoo',
        'kiss',
        'lick',
        'pat',
        'smug',
        'bonk',
        'yeet',
        'blush',
        'smile',
        'wave',
        'highfive',
        'handhold',
        'nom',
        'bite',
        'glomp',
        'slap',
        'kill',
        'kick',
        'happy',
        'wink',
        'poke',
        'dance',
        'cringe'
    ]
        self.nsfw_types = [
        'waifu',
        'neko',
        'trap',
        'blowjob'
    ]
    # easy_api.Waifu().waifu_pic()
    def waifu_pic(self):
        return r.get("https://api.waifu.pics/sfw/waifu").json()
    # easy_api.Waifu.waifu_with_context()
    def waifu_with_context(self):
        return random.choice(list(r.get("https://waifu-generator.vercel.app/api/v1").json()))
    # easy_api.Waifu.sfw({category})
    def sfw(self, category):
        """Retrieve sfw media using a custom endpoint specified by the user
        Returns:
            url: json
        """
        if not category in self.sfw_types:
            return f"(sfw) Please choose one of the following categories:\n{self.sfw_types}"
        return r.get(f"https://api.waifu.pics/sfw/{category}").json()
    # easy_api.Waifu.nsfw({category})
    def nsfw(self, category):
        """Retrieve nsfw media using a custom endpoint specified by the user
        Returns:
            url: json
        """
        if not category in self.nsfw_types:
            return f"(nsfw) Please choose one of the following categories:\n{self.nsfw_types}"
        return r.get(f"https://api.waifu.pics/nsfw/{category}").json()
    


"""
def fuck_off():
    return r.get("https://www.foaas.com/version", headers={"Accept": "text/plain",'Accept-Language': 'en-us'}.text)
"""
