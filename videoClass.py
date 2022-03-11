from googleapiclient.discovery import build
from plyer import notification
import public_constants
import private_constants
import time


def buildApi(apiKey):
    youtube = build(public_constants.YOUTUBE, public_constants.VERSION, developerKey=apiKey)
    return youtube

def executeVideosData(youtubeApi):
    pl_request = youtubeApi.playlistItems().list(
        part=public_constants.SECOND_TAG,
        playlistId=private_constants.PLAYLISTID
    )
    pl_response = pl_request.execute()
    return pl_response


def writeToFile(path, text):
    f = open(path, "w")
    f.write(text)
    f.close()


class Channel:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.videoDict = {}

    def setVideosList(self, playlists):
        self.videoDict = playlists

    def setVideoDetails(self, videos):
        for i in range(len(videos[public_constants.FIRST_TAG])):
            title_video = videos[public_constants.FIRST_TAG][i][public_constants.SECOND_TAG][public_constants.THIRD_TAG_FIRSTPLACE_DICT]
            date_video = videos[public_constants.FIRST_TAG][i][public_constants.SECOND_TAG][public_constants.THIRDTAG_SECONDPLACE_DICT]
            self.videoDict[title_video] = date_video
            return i

    def executeVideosData1(self, apiKey):
        while (True):
            youtubeApi = buildApi(apiKey)
            while 1:
                videos = executeVideosData(youtubeApi)
                self.setVideoDetails(videos)
                text_file = open(public_constants.FILENAME, "r")
                data = text_file.read()
                if (data != str(self.videoDict)):
                    notification.notify(
                        title=public_constants.TITLE,
                        message=str(self.videoDict),
                        app_icon=public_constants.APP_ICON

                    )
                    writeToFile(public_constants.FILENAME,str(self.videoDict))
                    time.sleep(public_constants.TIME)
