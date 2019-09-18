# -*- coding: utf-8 -*-
"""
Entry point of the socat collection.

Parses command line arguments and validate.

To list all commands type in: python socat.py -h
"""
import sys
import argparse

from analyze.log_analyzer import LogAnalyzer
from stream.tweet_streamer import TweetStreamer
from analyze.topic_detector import TopicDetector


def create_parser():
    """
    Creates a argparse parser.

    return:
    parser -- a argparse parser
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help='choose the mode which is either stream or analyze',
        metavar='stream or analyze',
        dest='mode'
    )
    subparsers.required = True

    # Subparser for stream commands
    stream_parser = subparsers.add_parser(
        'stream',
        help='Start streaming social media entries from source'
    )
    stream_parser.add_argument(
        'tweets',
        help='choose twitter as source'
    )
    stream_parser.add_argument(
        '-m',
        '--maximum',
        type=int,
        default=100,
        help='maximum entries'
    )
    stream_parser.add_argument(
        '-l',
        '--log',
        action='store_true',
        help='create an logfile in the output directory'
    )
    stream_parser.add_argument(
        '-p',
        '--path',
        help='output path for recived data'
    )
    stream_parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='verbose'
    )

    # Subparser for analyze commands
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze logfiles or perform topic detection'
    )
    analyze_parser.add_argument(
        '-p',
        '--path',
        required=True,
        help='path to data folder',
    )
    analyze_subparser = analyze_parser.add_subparsers(
        help='choose analyze logs or text',
        metavar='logs or text',
        dest='source'
    )
    analyze_subparser.required = True

    analyze_subparser.add_parser(
        'logs',
        help='analyze logsfiles'
    )
    analyze_text_parser = analyze_subparser.add_parser(
        'text',
        help='Use text data for topic detection'
    )
    analyze_text_parser.add_argument(
        '-m',
        '--methode',
        help='methode used for topic detection (KM or LDA)',
    )
    analyze_text_parser.add_argument(
        '-lang',
        '--language',
        help='used to filter entries by language',
    )
    return parser


def main(parser, args):
    """
    main function executes the right module
    with the selected options.

    Keyword arguments:
    parser -- a argparse parser
    args -- some arguments as string list
    """
    try:
        args = parser.parse_args(args)
        if args.mode == 'stream':
            # Start streaming tweets
            if args.tweets:
                TweetStreamer(
                    ret_max=args.maximum,
                    ver=args.verbose,
                    path=args.path,
                    log=args.log
                ).start_streaming()
        elif args.mode == 'analyze':
            # Start analyzing logs
            if args.source == 'logs':
                LogAnalyzer(path=args.path).create_bar_plot()
            # Start analyzing data
            elif args.source == 'text':
                TopicDetector(
                    path=args.path,
                    methode=args.methode,
                    lang=args.language
                ).start()

    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main(create_parser(), sys.argv[1:]))
