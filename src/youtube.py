import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

class YouTubeApi():
    base_url = "https://www.youtube.com/watch?v="

    def __init__(self):
        with open("configs/config.json", "r") as config_file:
            __config = json.load(config_file)
            self.__ApiKey = __config["keys"]["yt-api-key"]
            self.__Playlist = __config["playlist"]
        self.__YoutubeObject = self.__getYoutubeObject()
        self.__YoutubeObject_Oauth2 = self.__getYoutubeObject_Oauth2()
    
    def __getYoutubeObject(self):
        return build("youtube", "v3", developerKey=self.__ApiKey)

    def __getYoutubeObject_Oauth2(self):
        credentials = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file = "configs/client_secret.json",
            scopes = [
                "https://www.googleapis.com/auth/youtube"
            ]
        ).run_console()

        return build('youtube', 'v3', credentials=credentials)

    def __getResponse(self, request):
        return request.execute()

    def __getRequest(self, query, results):
        return self.__YoutubeObject.search().list(q=query, part="snippet", type="video", maxResults=results if results <= 50 else 50)

    def __getAvtpRequest(self, youtube, videoId, playlistId):
        return youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlistId,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": videoId
                    }
                }
            }
        )

    def getYoutubeVideos(self, query, results=5):
        items = json.loads(json.dumps(self.__getResponse(self.__getRequest(query, results=results))))["items"]
        info = []
        for item in items:
            snippet = item["snippet"]
            videoId = item["id"]["videoId"]
            thumbnail = snippet["thumbnails"]["medium"]

            info.append(
                YoutubeVideo(
                    title = snippet["title"], 
                    url = self.base_url + videoId, 
                    videoId = videoId,
                    thumbnailUrl = thumbnail["url"], 
                    thumbnailDimensions = {
                        "width": thumbnail["width"], 
                        "height": thumbnail["height"]
                    }
                )
            )

        return info

    def addVideoToPlaylist(self, videoId):
        youtubeObject = self.__YoutubeObject_Oauth2

        avtpRequest = self.__getAvtpRequest(youtubeObject, videoId, self.__Playlist)

        avtpResponse = self.__getResponse(avtpRequest)
        return avtpResponse

class YoutubeVideo():
    def __init__(self, title, url, videoId, thumbnailUrl, thumbnailDimensions):
        self.__title = title
        self.__url = url
        self.__videoId = videoId
        self.__thumbnailUrl = thumbnailUrl
        self.__thumbnailDimensions = thumbnailDimensions
    
    def getTitle(self):
        return self.__title
    
    def getUrl(self):
        return self.__url

    def getVideoId(self):
        return self.__videoId

    def getThumbnailUrl(self):
        return self.__thumbnailUrl
    
    def getThumbnailDimensions(self):
        return self.__thumbnailDimensions
