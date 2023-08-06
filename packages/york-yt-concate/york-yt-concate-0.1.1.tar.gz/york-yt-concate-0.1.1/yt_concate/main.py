import sys
import getopt

from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_v_links import GetVideoList
from yt_concate.pipeline.steps.initialize_yto import InitializeYTO
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_captions import ReadCaptions
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_video import DownLoadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.utils import Utils

CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'
SEARCH_WORD = 'incredible'
# 輸入字典
inputs = {
    'channel_id': CHANNEL_ID,
    'search_word': SEARCH_WORD,
    'limit': 10,
}


def print_usage():
    print('說明書在此:')
    print('python yt-concat.py OPERATIONS')
    print('OPERATION:')
    print('{:>6}  {:<16}{}'.format('-c', '--channel_id', 'channel_id for video channel'))
    print('{:>6}  {:<16}{}'.format('-s', '--search_word',
                                   '--search_word for the word you want to search in channel video'))
    print('{:>6}  {:<16}{}'.format('-l', '--limit', 'limit for download video clips'))


def main():
    # 步驟清單，裝著所有步驟，讓底下的for loop一個一個去call
    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYTO(),
        DownloadCaptions(),
        ReadCaptions(),
        Search(),
        DownLoadVideos(),
        EditVideo(),
        Postflight(),
    ]

    # Command Line Arguments 程式參數化
    short_opts = 'hc:s:l:'
    long_opts = 'help channel_id= search_word= limit='.split()
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit(0)
        elif opt in ("-c", "--channel_id"):
            inputs['channel_id'] = arg
        elif opt in ("-s", "--search_word"):
            inputs['search_word'] = arg
        elif opt in ("-l", "--limit"):
            inputs['limit'] = int(arg)

    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
