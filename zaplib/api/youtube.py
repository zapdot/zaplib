
from apiclient.discovery import build
from zaplib.configbox import config

class YouTubeAPI(object):

    def __init__(self, config_id = None):

        YOUTUBE_SERVICE_NAME = 'youtube'
        YOUTUBE_API_VERSION = 'v3'

        self.api = build(YOUTUBE_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=config["api"].youtube)

    # get channel metadata based on Youtube Channel ID or Youtube Username.
    # quota: 9 (w/ default settings)
    # docs: https://developers.google.com/youtube/v3/docs/channels/list
    def get_channel(self, id=None, username=None, parts=[]):

        if not (id or username) or (id and username):
            raise ValueError("Must use 'id' or 'username' argument.")

        # setup default params
        if not parts:
            parts = ["id", "snippet", "statistics", "brandingSettings", "contentDetails"] 

        # args passed to YT api
        args = {'part': ",".join(parts) }

        if id: 
            args['id'] = id
        else:
            args['forUsername'] = username

        query = self.api.channels().list(**args).execute()

        if not query['items']:
            return None

        result = query['items'][0]

        # collect results
        channel = {}

        if "id" in result:
            channel['id'] = result['id']

        if "snippet" in result:
            channel['title'] = result['snippet'].get('title','')
            channel['description'] = result['snippet'].get('description','')
            channel['custom_url'] = result['snippet'].get('customUrl','')
            channel['date_joined'] = result['snippet'].get('publishedAt','')
            channel['country'] = result['snippet'].get('country','')

        if "contentDetails" in result:
            channel['playlist_id'] = result['contentDetails']['relatedPlaylists']['uploads']

        if "brandingSettings" in result:
            channel['title'] = result['brandingSettings']['channel'].get('title','')
            channel['description'] = result['brandingSettings']['channel'].get('description','')
            channel['keywords'] = result['brandingSettings']['channel'].get('keywords','')
            channel['featured_channel_ids'] = result['brandingSettings']['channel'].get('featuredChannelsUrls','')
            channel['country'] = result['brandingSettings']['channel'].get('country','')

        if "statistics" in result:
            channel['view_count'] = result['statistics'].get('viewCount',0)
            channel['comment_count'] = result['statistics'].get('commentCount',0)
            channel['subscriber_count'] = result['statistics'].get('subscriberCount',0)
            channel['video_count'] = result['statistics'].get('videoCount',0)

        return channel

    # grab only update information for the channel (new stats and potentially new title/keywords/descriptions)
    # quota: 5 
    def get_channel_update(self, id):
        return get_channel(id=id, parts=["id", "statistics", "brandingSettings"])

    # grab videos in a given playlist_id, up to maxResults
    # * setting maxResults to negative will return all results
    # * note: be very careful with the maxResults, as it _directly_ affects the quota per call
    # quota: 1 + (2 * (totalResults/50))
    # docs: https://developers.google.com/youtube/v3/docs/playlistItems/list
    def get_playlist_videos(self, playlist_id, maxResults=50):

        args = {}
        args['playlistId'] = playlist_id
        args['part'] = "snippet"
        args['maxResults'] = 50 if maxResults < 0 else min(max(1, maxResults), 50)

        query = self.api.playlistItems().list(**args)

        videos = []

        while query:
            result = query.execute()

            for item in result['items']:
                video = {}
                video['video_id'] = item['snippet']['resourceId']['videoId']
                video['title'] = item['snippet']['title']
                video['description'] = item['snippet'].get('description','')
                video['publish_date'] = item['snippet']['publishedAt']

                videos.append(video)

                if len(videos) >= maxResults:
                    break

            if len(videos) < maxResults or maxResults < 0:
                query = self.api.playlistItems().list_next(query, result)
            else:
                break

        return videos

    # get specific details about a video, such as tags, and interaction data (views, comments, likes/dislikes)
    # note: if duration is needed, use the part 'contentDetails'
    # quota: 1 + (4 * numOfIds)
    # docs: https://developers.google.com/youtube/v3/docs/videos/list
    def get_video(self, id, parts=[]):

        if not parts:
            parts = ['id', 'snippet', 'statistics']

        many_ids = not isinstance(id, basestring)

        maxResults = len(id) if many_ids else 1

        args = {}
        args['part'] = ",".join(parts)
        args['id'] = ",".join(id) if many_ids else id
        args['maxResults'] = min(max(1, maxResults), 50)

        query = self.api.videos().list(**args)

        if many_ids:
            videos = []

            while query:
                result = query.execute()

                for item in result['items']:
                    video = self.__parse_video_item(item)
                    videos.append(video)

                    if len(videos) >= maxResults:
                        break

                if len(videos) < maxResults or maxResults < 0:
                    query = self.api.videos().list_next(query, result)
                else:
                    break

            return videos

        else:
            result = query.execute()

            return self.__parse_video_item(result['items'][0])


    def __parse_video_item(self, item):
        video = {}

        if "id" in item:
            video['video_id'] = item['id']

        if "snippet" in item:
            video['title'] = item['snippet']['title']
            video['description'] = item['snippet'].get('description','')
            video['publish_date'] = item['snippet']['publishedAt']
            video['tags'] = ",".join(item['snippet']['tags'])
            video['category_id'] = item['snippet']['categoryId']

        if "contentDetails" in item:
            video['duration'] = item['contentDetails']['duration']

        if "statistics" in item:
            video['view_count'] = item['statistics']['viewCount']
            video['like_count'] = item['statistics']['likeCount']
            video['dislike_count'] = item['statistics']['dislikeCount']
            video['comment_count'] = item['statistics']['commentCount']

        return video

