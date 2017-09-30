import math
import re

from fixerio import Fixerio
from measurement.measures import Volume

fxrio = Fixerio(base='USD')
conversion = fxrio.latest()


def my_va_transform(s):
    """Function to transform brand
    * make lower
    * do specific regex replacements
    * remove product types ex: 'bourbon', 'whiskey'
    * sort the words in the brand
    """
    s = s.lower()

    replacements = {"^gentleman jack whiskey$": "jack daniel's gentleman jack",
                    "^pritchard": "prichard",
                    "^balcones baby blue corn whiskey$": "balcones baby blue",
                    "^canadian club rye whisky$": "canadian club",
                    "^catoctin creek roundstone rye whisky$": "catoctin creek roundstone rye",
                    "^e h taylor jr. straight rye$": "colonel e.h. taylor straight rye",
                    "^e h taylor seasoned wood$": "colonel e.h. taylor seasoned wood",
                    "^james e. pepper 1776 rye": "james e. pepper 1776 straight rye",
                    "^lock stock & barrel 16 yr straight rye whiskey$": "lock stock and barrel 16 straight rye",
                    "^michter's us 1 single barrel straight rye$": "michter's us*1",
                    "^michter's us-1 barrel strength rye": "michter's barrel strength rye",
                    "^old overholt$": "old overholt rye",
                    "^wild turkey russell's reserve rye$": "russell's reserve rye 6",
                    "\s7\s": " seven ",
                    "^defiant whisky$": "defiant",
                    "^michter's us1 sour mash$": "michter sour mash",
                    "^red stag": "jim beam red stag",
                    "^four roses 2015 limited edition small batch$": "four roses limited edition 2015",
                    "^four roses 2016 limited edition small batch$": "four roses small batch limited edition 2016",
                    "^i w harper bourbon$": "i.w. harper",
                    "^jesse james bourbon whiskey$": "original jesse james",
                    "^the": " ",
                    "scotch$": " ",
                    "-": " ",
                    }
    for k, v in replacements.items():
        s = re.sub(k, v, s)

    replace = ['bourbon', 'craft',
               'Year Single Barrel Bourbon',
               '-year Single Barrel Bourbon',
               'whiskey', 'tennessee whiskey', 'tennessee',
               'year', 'yr', '-year single barrel',
               'year single barrel', 'label', "'s",
               'decades', 'whisky', '&', 'single malt', "(", ")",
               "yo", "no.", "irish", "’", "us1",
               ]

    for item in replace:
        s = s.replace(item, '')

    s = s.split() # remove extra spaces betwen words and sort
    s.sort()
    s = " ".join(s)

    return s.strip()


def my_size_transform(s):
    if 'ml' in s:
        v = Volume(milliliter=s.replace('ml', ''))
    elif 'L' in s:
        v = Volume(liter=s.replace('L', ''))
    return v.us_oz


def isnumber(num):
    return all(char.isdigit() for char in num)


def transform_currency(s):
    if 'CAD' in str(s) or 'CDN' in str(s):
        price = re.sub(r"""[^0-9]+""", '', s)
        new_price = float(price) / float(conversion['rates']['CAD'])
        return new_price
    elif '£' in str(s) or 'GBP' in str(s):
        price = re.sub(r"""[^0-9]+""", '', s)
        new_price = float(price) / float(conversion['rates']['GBP'])
        return new_price
    elif 'AUD' in str(s) or 'AUS' in str(s):
        price = re.sub(r"""[^0-9]+""", '', s)
        new_price = float(price) / float(conversion['rates']['AUD'])
        return new_price
    elif 'NZD' in str(s):
        price = re.sub(r"""[^0-9]+""", '', s)
        new_price = float(price) / float(conversion['rates']['NZD'])
        return new_price
    elif 'EUR' in str(s) or '€' in str(s) or 'Euro' in str(s):
        price = re.sub(r"""[^0-9]+""", '', s)
        new_price = float(price) / float(conversion['rates']['EUR'])
        return new_price
    elif 'SEK' in str(s):
        price = re.sub(r"""[^0-9]+""", '', s)
        new_price = float(price) / float(conversion['rates']['SEK'])
        return new_price
    elif 'RMB' in str(s):
        price = re.sub(r"""[^0-9]+""", '', s)
        new_price = float(price) / float(conversion['rates']['CNY'])
        return new_price
    elif 'DKR' in str(s):
        price = re.sub(r"""[^0-9]+""", '', s)
        new_price = float(price) / float(conversion['rates']['DKK'])
        return new_price
    elif 'HKD' in str(s):
        price = re.sub(r"""[^0-9]+""", '', s)
        new_price = float(price) / float(conversion['rates']['HKD'])
        return new_price
    elif 'JPY' in str(s):
        price = re.sub(r"""[^0-9]+""", '', s)
        new_price = float(price) / float(conversion['rates']['JPY'])
        return new_price
    elif 'ZAR' in str(s):
        price = re.sub(r"""[^0-9]+""", '', s)
        new_price = float(price) / float(conversion['rates']['ZAR'])
        return new_price
    elif type(s) == str and isnumber(s):
        # USD
        return s
    elif type(s) == float and math.isnan(s):
        # NAN
        return s
    elif re.match(r"""^\$*\d+\.*\d+$""", s):
        s = s.replace('$', '')
        return s
    else:
        # Convert everything else to NAN
        #print(s)
        return None


def my_wc_transform(s):
    """Function to transform brand
    * make lower
    * remove product types ex: 'bourbon', 'whiskey'
    """


    replacements = {"yo\W": " ",
                    "^prichard’s rye$": " prichard ",
                    "^reserve rye straight woodford$": "reserve rye woodford",
                    "^kentucky rebel yell": "rebel yell",
                    "laphroaig triple wood": "laphroaig triplewood",
                    "barrel four roses single": "four roses",
                    "founder glenlivet reserve": "founders glenlivet reserve",
                    "founder’s irishman reserve": "founders irishman reserve",
                    "carribean": "caribbean",
                    "12 glendronach original": "12 glendronach",
                    "dalwhinnie distillers edition": "dalwhinnie distiller edition",
                    "all distiller edition editions glenkinchie": "distiller edition glenkinchie",
                    "dalwhinnie distillers edition": "dalwhinnie distiller edition",
                    "ardbeg uigeadail": "ardbeg uigeadall",
                    "all daniel distiller jack master series": "daniel distiller jack master",
                    "21 balvenie port wood": "21 balvenie portwood",
                    "21 fine macallan oak": "21 fine macallan oak old",
                    "american auchentoshan oak": "american auchentosahn oak",
                    "basil haydens kentucky": "basil hayden",
                    "2016 cairdeas laphroaig madeira": "cairdeas laphroaig madeira",
                    "cooper croze jameson": "cooper croze",
                    "all distillers edition oban vintages": "distillers edition oban",
                    "16 glenlivet nadurra": "glenlivet nadurra",
                    "all midleton rare very vintages": "midleton rare",
                    "mortlach old rare": "mortlach rare",
                    "and rare rich": "rare rich",
                    "high redemption rye": "redemption rye",
                    "1792 finished port": "1792 finish port",
                    }
    for k, v in replacements.items():
        s = re.sub(k, v, s)

    replace = ["nas", ]

    for item in replace:
        s = s.replace(item, '')

    s = s.split() # remove extra spaces between words
    s.sort()
    s = " ".join(s)

    return s.strip()


def my_proof_transform(s):
    """Function to transform brand
    * make lower
    * remove product types ex: 'bourbon', 'whiskey'
    """


    replacements = {"101 8 turkey wild": "101 turkey wild",
                    "114 dad grand old proof": "114 dad grand old",
                    "81 turkey wild": "81 rye turkey wild",
                   }
    for k, v in replacements.items():
        s = re.sub(k, v, s)

    replace = [ ]

    for item in replace:
        s = s.replace(item, '')

    s = s.split() # remove extra spaces between words
    s.sort()
    s = " ".join(s)

    return s.strip()
