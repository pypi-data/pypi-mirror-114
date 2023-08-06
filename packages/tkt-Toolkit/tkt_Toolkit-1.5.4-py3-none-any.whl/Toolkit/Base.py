from TikTokApi import TikTokApi
from termcolor import colored
from . import __ext_TTA__

if __ext_TTA__ == True:
    ttapi = TikTokApi(debug=True)
else:
    ttapi = None
    #print(colored("__ext_TTA__ == False, so the API won't work"))
"""
For the TikTokApi to work please set __ext_TTA__ = True
"""