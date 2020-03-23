from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

EXE_PATH = "../geckodriver"

class VideoPlayer:
    def __init__(self, playlist = None):
        if playlist != None:
            self.__Playlist = playlist
            self.__PlaylistSet = True
        else:
            self.__PlaylistSet = False
        self.__Started = False
    
    def init(self, playlist):
        if not self.__PlaylistSet:
            self.__Playlist = playlist
            self.__PlaylistSet = True

    def startPlaylist(self):
        if not self.__PlaylistSet:
            raise Exception("Playlist wasn't set")
        self.__Started = True
        self.__Browser = self.__getBrowser()        
        self.__Browser.get("https://www.youtube.com/playlist?list=" + self.__Playlist)
        self.__Browser.find_element_by_xpath('//*[@id="thumbnail"]').click()
        self.__loopTrigger()

    def nextSong(self):
        self.__getBodyElement().send_keys(Keys.SHIFT, 'n')

    def pauseplay(self):
        self.__getBodyElement().send_keys(Keys.SPACE)

    def started(self):
        return self.__Started

    def __getBrowser(self):
        ffprofile = webdriver.FirefoxProfile()
    
        adblockfile = 'browser_extensions/adblock_plus-3.8-an+fx.xpi'
        ffprofile.add_extension(adblockfile)

        return webdriver.Firefox(executable_path=EXE_PATH, firefox_profile=ffprofile)

    def __getBodyElement(self):
        return self.__Browser.find_element_by_xpath('//body')

    def __loopTrigger(self):
        tag = "button"
        attribute = 'aria-label="Loop playlist"'
        try:
            element_present = EC.presence_of_element_located((By.XPATH, f'//{tag}[@{attribute}]'))
            WebDriverWait(self.__Browser, timeout = 5).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        
        self.__Browser.execute_script(f'document.querySelector(\'{tag}[{attribute}]\').click()')
 