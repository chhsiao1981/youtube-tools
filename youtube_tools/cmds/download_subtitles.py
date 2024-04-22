# -*- coding: utf-8 -*-

import argparse
import os
from youtube_transcript_api import YouTubeTranscriptApi
import yaml


def download_subtitles(video_ids: list[str], root_dir: str) -> None:
    for video_id in video_ids:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for idx, transcript in enumerate(transcript_list):
            print(f'({idx}/{len(transcript_list)}) video_id: {transcript.video_id} lang: {transcript.language} code: {transcript.language_code} generated: {transcript.is_generated} translatable: {transcript.is_translatable} translation_languages: {transcript.translation_languages}')

            out_dir = os.sep.join([root_dir, video_id, f'{idx:02d}-{transcript.language}'])
            os.makedirs(out_dir)
            metadata = {
                'video_id': transcript.video_id,
                'lang': transcript.language,
                'lang_code': transcript.language_code,
                'generated': transcript.is_generated,
            }
            out_filename = os.sep.join(out_dir, 'metadata.yaml')
            with open(out_filename, 'w') as f:
                yaml.dump(metadata, f)

            text = transcript.fetch()
            out_filename = os.sep.join(out_dir, 'text.yaml')
            with open(out_filename, 'w') as f:
                yaml.dump(text, f)


def parse_args() -> argparse.ArgumentParser:
    '''
    Returns:
        TYPE: Description
    '''
    parser = argparse.ArgumentParser(description='download youtoube subtitle')
    parser.add_argument('-v', '--video_ids', type=str, required=True, help="list of video-id, comma separated")
    parser.add_argument('-o', '--out_dir', type=str, required=False, default='./subtitles', help="output-base-dir")

    return parser


def _main():
    """Summary
    """
    args = parse_args()

    video_ids = args.video_ids.split(',')

    download_subtitles(video_ids, args.out_dir)


if __name__ == '__main__':
    _main()
