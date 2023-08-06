import argparse
from argparse import ArgumentParser
from typing import List

from cli.Match import Match
from cli.MatchSegment import MatchSegment
from key_passager.KeyPassager import KeyPassager
from key_passager.TextWithMatches import TextWithMatches
from lotte.Lotte import Lotte
import json
import time
from os.path import join, isfile, splitext, basename
from os import listdir
from shutil import copyfile
import multiprocessing
from datetime import datetime
from pathlib import Path
from key_passager.CitationSource import CitationSource
from key_passager.CitationSourceLink import CitationSourceLink
from key_passager.ImportantSegment import ImportantSegment
from key_passager.ImportantSegmentLink import ImportantSegmentLink
from key_passager.SourceSegment import SourceSegment
from key_passager.TargetLocation import TargetLocation
from key_passager.TargetLocationSelection import TargetLocationSelection
from key_passager.TargetText import TargetText
from key_passager.TargetTextLocationLink import TargetTextLocationLink
from visualization.Info import Info
from visualization.TargetTextWithContent import TargetTextWithContent
from visualization.Visualizer import Visualizer


class IntCheckAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):

        if option_string == '--min-match-length':
            if int(values) < 3:
                parser.error("Minimum value for {0} is 3".format(option_string))
        elif option_string == '--look-back-limit':
            if int(values) < 0:
                parser.error("{0} must be positive".format(option_string))
        elif option_string == '--look-ahead-limit':
            if int(values) < 0:
                parser.error("{0} must be positive".format(option_string))
        elif option_string == '--max-merge-distance':
            if int(values) < 0:
                parser.error("{0} must be positive".format(option_string))
        elif option_string == '--max-merge-ellipsis-distance':
            if int(values) < 0:
                parser.error("{0} must be positive".format(option_string))
        elif option_string == '--max-num-processes':
            if int(values) <= 0:
                parser.error("{0} must be greater 0".format(option_string))

        setattr(namespace, self.dest, values)


def __json_decoder_matches(json_input):
    if 'source_match_segment' in json_input and 'target_match_segment' in json_input:
        return Match(json_input['source_match_segment'], json_input['target_match_segment'])
    else:
        return MatchSegment(json_input['character_start_pos'], json_input['character_end_pos'])


def __json_decoder_citation_source(json_input):
    if 'source_segments' in json_input:
        return CitationSource(json_input['my_id'], json_input['source_segments'], json_input['important_segments'],
                              json_input['text'])
    elif 'source_segment_ids' in json_input:
        return ImportantSegment(json_input['my_id'], json_input['source_segment_ids'], json_input['frequency'],
                                json_input['token_length'], json_input['text'])
    else:
        return SourceSegment(json_input['my_id'], json_input['start'], json_input['end'], json_input['frequency'],
                             json_input['token_length'], '')


def __json_decoder_citation_source_link(json_input):
    if 'citation_source_id' in json_input:
        return CitationSourceLink(json_input['citation_source_id'], json_input['target_location_selections'])
    elif 'target_text_id' in json_input:
        return TargetLocationSelection.from_list(json_input['target_text_id'], json_input['target_location_ids'])


def __json_decoder_target_text(json_input):
    if 'filename' in json_input:
        return TargetText(json_input['my_id'], json_input['filename'], json_input['target_locations'])
    else:
        return TargetLocation(json_input['my_id'], json_input['start'], json_input['end'], json_input['text'])


def __json_encoder_lotte(obj):
    if isinstance(obj, MatchSegment):
        result_dict = obj.__dict__

        if not result_dict['text']:
            del result_dict['text']

        return result_dict

    return obj.__dict__


def __json_encoder_key_passager(obj):
    return __json_encoder(obj, False)


def __json_encoder_visualization(obj):
    return __json_encoder(obj, True)


def __json_encoder(obj, strip):
    if isinstance(obj, set):
        return list(obj)

    if isinstance(obj, (TargetText, CitationSourceLink, TargetLocationSelection, TargetTextLocationLink,
                        ImportantSegmentLink, Info)):
        return obj.__dict__

    if isinstance(obj, CitationSource):
        if not strip:
            return obj.__dict__

        result_dict = obj.__dict__

        if len(result_dict['text']) > 40:
            text = result_dict['text']
            result_dict['text'] = text[0:20] + ' [\u2026] ' + text[-20:]

        return result_dict

    if isinstance(obj, TargetLocation):
        if not strip:
            return obj.__dict__

        result_dict = obj.__dict__

        if 'start' in result_dict:
            del result_dict['start']

        if 'end' in result_dict:
            del result_dict['end']

        if len(result_dict['text']) > 40:
            text = result_dict['text']
            result_dict['text'] = text[0:20] + ' [\u2026] ' + text[-20:]

        return result_dict

    if isinstance(obj, ImportantSegment):
        if not strip:
            return obj.__dict__

        result_dict = obj.__dict__

        if len(result_dict['text']) > 40:
            text = result_dict['text']
            result_dict['text'] = text[0:20] + ' [\u2026] ' + text[-20:]

        return result_dict
    elif isinstance(obj, SourceSegment):
        if not strip:
            return obj.__dict__

        result_dict = obj.__dict__

        if 'citation_targets' in result_dict:
            del result_dict['citation_targets']

        if 'text' in result_dict:
            del result_dict['text']

        return result_dict

    return obj


def __run_compare(source_file_path, target_path, export_text, output_type, min_match_length, look_ahead_limit,
                  look_back_limit, max_merge_distance, max_merge_ellipsis_distance, output_folder_path,
                  num_of_processes):
    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        source_file_content = source_file.read()

    if isfile(target_path) and target_path.endswith(".txt"):

        with open(target_path, 'r', encoding='utf-8') as target_file:
            target_file_content = target_file.read()

        filename = splitext(basename(target_path))[0]

        __process_file(source_file_content, target_file_content, export_text, output_type, min_match_length,
                       look_ahead_limit, look_back_limit, max_merge_distance, max_merge_ellipsis_distance,
                       output_folder_path, filename)
    else:
        pool = multiprocessing.Pool(num_of_processes)

        for file_or_folder in listdir(target_path):
            full_path = join(target_path, file_or_folder)

            if isfile(full_path) and full_path.endswith(".txt"):
                with open(full_path, 'r', encoding='utf-8') as target_file:
                    target_file_content = target_file.read()

                filename = splitext(basename(full_path))[0]
                pool.apply_async(__process_file, args=(source_file_content, target_file_content, export_text,
                                                       output_type, min_match_length, look_ahead_limit,
                                                       look_back_limit, max_merge_distance,
                                                       max_merge_ellipsis_distance, output_folder_path,
                                                       filename))

        pool.close()
        pool.join()


def __process_file(source_file_content, target_file_content, export_text, output_type, min_match_length,
                   look_ahead_limit, look_back_limit, max_merge_distance, max_merge_ellipsis_distance,
                   output_folder_path, filename):
    lotte = Lotte(min_match_length, look_back_limit, look_ahead_limit, max_merge_distance, max_merge_ellipsis_distance)
    matches = lotte.compare(source_file_content, target_file_content)

    output_matches = []

    for match in matches:
        source_match_segment = match.source_match_segment
        target_match_segment = match.target_match_segment

        source_output_match_segment = MatchSegment(source_match_segment.character_start_pos,
                                                   source_match_segment.character_end_pos)

        target_output_match_segment = MatchSegment(target_match_segment.character_start_pos,
                                                   target_match_segment.character_end_pos)

        if export_text:
            source_text = source_file_content[source_match_segment.character_start_pos:
                                              source_match_segment.character_end_pos]
            target_text = target_file_content[target_match_segment.character_start_pos:
                                              target_match_segment.character_end_pos]

            source_output_match_segment.text = source_text
            target_output_match_segment.text = target_text

        output_match = Match(source_output_match_segment, target_output_match_segment)
        output_matches.append(output_match)

    if output_type == 'json':
        result = json.dumps(output_matches, default=__json_encoder_lotte)
        file_ending = 'json'
    else:
        result = ''

        for match in output_matches:
            match_literature = match.source_match_segment
            match_scientific = match.target_match_segment

            result += f'\n\n{match_literature.character_start_pos}\t{match_literature.character_end_pos}'

            if export_text:
                result += f'\t{match_literature.text}'

            result += f'\n{match_scientific.character_start_pos}\t{match_scientific.character_end_pos}'

            if export_text:
                result += f'\t{match_scientific.text}'

        result = result.strip()
        file_ending = 'txt'

    if output_folder_path:
        filename = f'{filename}.{file_ending}'
        with open(join(output_folder_path, filename), 'w', encoding='utf-8') as output_file:
            output_file.write(result)

    else:
        print('Ergebnisse:')
        print(result)


def __run_key_passager(source_file_path, target_folder_path, matches_folder_path, output_folder_path):
    key_passager = KeyPassager()

    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        source_content = source_file.read()

    target_text_matches_list = []

    for fileOrFolder in listdir(matches_folder_path):
        matches_file_path = join(matches_folder_path, fileOrFolder)

        if isfile(matches_file_path) and matches_file_path.endswith(".json"):
            filename = splitext(basename(matches_file_path))[0]

            with open(join(target_folder_path, filename + '.txt'), 'r', encoding='utf-8') as target_file:
                target_content = target_file.read()

            with open(matches_file_path, 'r', encoding='utf-8') as matches_file:
                matches = json.load(matches_file, object_hook=__json_decoder_matches)
                matches.sort(key=lambda x: x.source_match_segment.character_start_pos)

            target_text_matches_list.append(TextWithMatches(filename, target_content, matches))

    analyzed_work = key_passager.generate(target_text_matches_list, source_content)

    with open(join(output_folder_path, 'target_texts.json'), 'w', encoding='utf-8') as target_works_output_file:
        content = json.dumps(analyzed_work.target_texts, default=__json_encoder_key_passager)
        target_works_output_file.write(content)

    with open(join(output_folder_path, 'citation_sources.json'), 'w', encoding='utf-8') as segments_output_file:
        content = json.dumps(list(analyzed_work.citation_sources), default=__json_encoder_key_passager)
        segments_output_file.write(content)

    with open(join(output_folder_path, 'target_text_location_links.json'), 'w', encoding='utf-8') as \
            target_text_location_links_output_file:
        content = json.dumps(analyzed_work.target_text_location_links, default=__json_encoder_key_passager)
        target_text_location_links_output_file.write(content)

    with open(join(output_folder_path, 'citation_source_links.json'), 'w', encoding='utf-8') as \
            citation_source_links_output_file:
        content = json.dumps(analyzed_work.citation_source_links, default=__json_encoder_key_passager)
        citation_source_links_output_file.write(content)

    with open(join(output_folder_path, 'important_segment_links.json'), 'w', encoding='utf-8') as \
            important_segment_links_output_file:
        content = json.dumps(analyzed_work.important_segment_links, default=__json_encoder_key_passager)
        important_segment_links_output_file.write(content)


def __run_visualize(source_file_path, target_folder_path, key_passages_folder_path, output_folder_path, title, author,
                    year, censor):
    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        source_content = source_file.read()

    with open(join(key_passages_folder_path, 'citation_sources.json'), 'r', encoding='utf-8') as citation_sources_file:
        citation_sources = json.load(citation_sources_file, object_hook=__json_decoder_citation_source)

    with open(join(key_passages_folder_path, 'citation_source_links.json'), 'r', encoding='utf-8') as \
            citation_source_links_file:
        citation_source_links = json.load(citation_source_links_file, object_hook=__json_decoder_citation_source_link)

    with open(join(key_passages_folder_path, 'target_texts.json'), 'r', encoding='utf-8') as target_texts_file:
        target_texts = json.load(target_texts_file, object_hook=__json_decoder_target_text)

    target_texts_with_content: List[TargetTextWithContent] = []

    for target_text in target_texts:
        filename = target_text.filename
        with open(join(target_folder_path, f'{filename}.txt'), 'r', encoding='utf-8') as target_text_file:
            target_content = target_text_file.read()

        target_texts_with_content.append(TargetTextWithContent(target_text, target_content))

    visualizer = Visualizer(censor, 25)
    visualization = visualizer.visualize(title, author, year, source_content, citation_sources, citation_source_links,
                                         target_texts_with_content)

    with open(join(output_folder_path, 'info.json'), 'w', encoding='utf-8') as info_output_file:
        content = json.dumps(visualization.info, default=__json_encoder_visualization)
        info_output_file.write(content)

    with open(join(output_folder_path, 'source' + '.html'), 'w', encoding='utf-8') as source_html_output_file:
        source_html_output_file.write(visualization.source_html)

    Path(join(output_folder_path, 'target')).mkdir(parents=True, exist_ok=True)

    for target_html in visualization.targets_html:
        with open(join(output_folder_path, 'target/' + target_html.filename + '.html'), 'w', encoding='utf-8') as \
                target_html_output_file:
            target_html_output_file.write(target_html.text)

    copyfile(join(key_passages_folder_path, 'citation_source_links.json'), join(output_folder_path,
                                                                                'citation_source_links.json'))
    copyfile(join(key_passages_folder_path, 'important_segment_links.json'), join(output_folder_path,
                                                                                  'important_segment_links.json'))
    copyfile(join(key_passages_folder_path, 'target_text_location_links.json'), join(output_folder_path,
                                                                                     'target_text_location_links.json'))

    with open(join(output_folder_path, 'citation_sources.json'), 'w', encoding='utf-8') as citation_sources_output_file:
        content = json.dumps(citation_sources, default=__json_encoder_visualization)
        citation_sources_output_file.write(content)

    with open(join(output_folder_path, 'target_texts.json'), 'w', encoding='utf-8') as target_texts_output_file:
        content = json.dumps(target_texts, default=__json_encoder_visualization)
        target_texts_output_file.write(content)


def main():
    compare_description = "Lotte compare allows the user to find quotations in two texts, a source text and a target " \
                          "text. If known, the source text should be the one that is quoted by the target text. " \
                          "This allows the algorithm to handle things like ellipsis in quotations."

    argument_parser = ArgumentParser(description="Lotte is a tool to find quotations in texts and to visualize the"
                                                 " matching segments.")

    subparsers = argument_parser.add_subparsers(dest='command')
    subparsers.required = True

    parser_compare = subparsers.add_parser('compare', help=compare_description, description=compare_description)

    parser_compare.add_argument("source_file_path", nargs=1, metavar="source-file-path",
                                help="Path to the source text file")
    parser_compare.add_argument("target_path", nargs=1, metavar="target-path",
                                help="Path to the target text file or folder")
    parser_compare.add_argument('--text', dest="export_text", default=True, action='store_true',
                                help="Include matched text in the returned data structure")
    parser_compare.add_argument('--no-text', dest='export_text', action='store_false',
                                help="Don't include matched text in the returned data structure")
    parser_compare.add_argument('--output-type', choices=['json', 'text'], dest="output_type", default="json",
                                help="The output type")
    parser_compare.add_argument('--output-folder-path', dest="output_folder_path",
                                help="The output folder path. If this option is set the output will be saved to a file"
                                     " created in the specified folder")
    parser_compare.add_argument('--min-match-length', dest="min_match_length", action=IntCheckAction,
                                default=5, type=int, help="The length of the shortest match (>= 3, default: 5)")

    parser_compare.add_argument('--look-back-limit', dest="look_back_limit", action=IntCheckAction,
                                default=10, type=int, help="The number of tokens to skip when looking backwards"
                                                           " (>= 0, default: 10), (Very rarely needed)")
    parser_compare.add_argument('--look-ahead-limit', dest="look_ahead_limit", action=IntCheckAction,
                                default=3, type=int, help="The number of tokens to skip when looking ahead"
                                                          " (>= 0, default: 3)")
    parser_compare.add_argument('--max-merge-distance', dest="max_merge_distance", action=IntCheckAction,
                                default=2, type=int, help="The maximum distance in tokens between two matches"
                                                          " considered for merging (>= 0, default: 2)")
    parser_compare.add_argument('--max-merge-ellipsis-distance', dest="max_merge_ellipsis_distance",
                                action=IntCheckAction, default=10, type=int,
                                help="The maximum distance in tokens between two matches considered for merging where"
                                     " the target text contains an ellipsis between the matches (>= 0, default: 10)")
    parser_compare.add_argument('--create-dated-subfolder', dest="created_dated_subfolder", default=False,
                                action='store_true',
                                help="Create a subfolder named with the current date to store the results")
    parser_compare.add_argument('--no-create-dated-subfolder', dest="created_dated_subfolder",
                                action='store_false',
                                help="Don't create a subfolder named with the current date to store the results")
    parser_compare.add_argument('--max-num-processes', dest="max_num_processes", action=IntCheckAction, default=1,
                                type=int, help="Maximum number of processes to use for parallel processing")

    keypassage_description = 'Lotte keypassage allows the user to extract key passages from the found matches.'

    parser_key_passage = subparsers.add_parser('keypassage', help=keypassage_description,
                                               description=keypassage_description)

    parser_key_passage.add_argument("source_file_path", nargs=1, metavar="source-file-path",
                                    help="Path to the source text file")
    parser_key_passage.add_argument("target_folder_path", nargs=1, metavar="target-folder-path",
                                    help="Path to the target texts folder path")
    parser_key_passage.add_argument("matches_folder_path", nargs=1, metavar="matches-folder-path",
                                    help="Path to the folder with the match files, i.e. the results from lotte compare")
    parser_key_passage.add_argument("output_folder_path", nargs=1, metavar="output-folder-path",
                                    help="Path to the output folder")

    parser_visualize = subparsers.add_parser('visualize',
                                             help="Lotte visualize allows the user to create the files needed"
                                                  " for a website that visualizes the lotte algorithm results.",
                                             description="Lotte visualize allows the user to create the files needed"
                                                         " for a website that visualizes the lotte algorithm results.")

    parser_visualize.add_argument("source_file_path", nargs=1, metavar="source-file-path",
                                  help="Path to the source text file")
    parser_visualize.add_argument("target_folder_path", nargs=1, metavar="target-folder-path",
                                  help="Path to the target texts folder path")
    parser_visualize.add_argument("key_passages_folder_path", nargs=1, metavar="key-passages-folder-path",
                                  help="Path to the folder with the key passages files, i.e. the resulting files from"
                                       " lotte keypassage")
    parser_visualize.add_argument("output_folder_path", nargs=1, metavar="output-folder-path",
                                  help="Path to the output folder")
    parser_visualize.add_argument("--title", dest="title", help="Title of the work", default="NN")
    parser_visualize.add_argument("--author", dest="author", help="Author of the work", default="NN")
    parser_visualize.add_argument("--year", dest="year", help="Year of the work", default="0", type=int)
    parser_visualize.add_argument('--censor', dest="censor", default=False, action='store_true',
                                  help="Censor scholarly works to prevent copyright violations")

    args = argument_parser.parse_args()

    if args.command == 'compare':
        source_path = args.source_file_path[0]
        target_path = args.target_path[0]
        export_text = args.export_text
        output_type = args.output_type
        output_folder_path = args.output_folder_path
        min_match_length = args.min_match_length
        look_ahead_limit = args.look_ahead_limit
        look_back_limit = args.look_back_limit
        max_merge_distance = args.max_merge_distance
        max_merge_ellipsis_distance = args.max_merge_ellipsis_distance
        created_dated_subfolder = args.created_dated_subfolder
        max_num_processes = args.max_num_processes

        if output_folder_path and created_dated_subfolder:
            now = datetime.now()
            date_time_string = now.strftime("%Y_%m_%d_%H_%M_%S")
            output_folder_path = join(args.output_folder_path, date_time_string)
            Path(output_folder_path).mkdir(parents=True, exist_ok=True)

        start_time = time.time()

        __run_compare(source_path, target_path, export_text, output_type, min_match_length, look_ahead_limit,
                      look_back_limit, max_merge_distance, max_merge_ellipsis_distance, output_folder_path,
                      max_num_processes)

        end_time = time.time()
        print(f'\n--- Runtime: {end_time - start_time: .2f} seconds ---')
    elif args.command == 'keypassage':
        source_file_path = args.source_file_path[0]
        target_folder_path = args.target_folder_path[0]
        matches_folder_path = args.matches_folder_path[0]
        output_folder_path = args.output_folder_path[0]

        __run_key_passager(source_file_path, target_folder_path, matches_folder_path, output_folder_path)
    elif args.command == 'visualize':
        source_file_path = args.source_file_path[0]
        target_folder_path = args.target_folder_path[0]
        key_passages_folder_path = args.key_passages_folder_path[0]
        output_folder_path = args.output_folder_path[0]
        title = args.title

        author = args.author
        year = args.year
        censor = args.censor

        start_time = time.time()
        __run_visualize(source_file_path, target_folder_path, key_passages_folder_path, output_folder_path, title,
                        author, year, censor)
        end_time = time.time()
        print(f'\n--- Runtime: {end_time - start_time: .2f} seconds ---')


if __name__ == '__main__':
    main()
