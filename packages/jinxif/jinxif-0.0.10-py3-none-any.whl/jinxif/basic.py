#####
# title: basic.py
#
# language: python3
# author: Jenny, bue
# license: GPLv>=3
# date: 2021-04-00
#
# description:
#     jinxif python3 basic function library that are used other jinxif libraries.
#####


# library
from jinxif import config
from jinxif import imgmeta # bue: add_exposure
import os
import pandas as pd
import re

# development
#import importlib
#importlib.reload()

# function

###################
# parse fielnames #
###################
def _parse_file(
        s_regex,
        di_regex,
        b_fname_ugly = False,
        s_wd = './',
    ):
    '''
    version: 2021-06-28
    internal function

    input:
        s_regex: regex string with regex groups () to parse the particulare filenames.

        di_regex: dictionary to link regex label (string)
            to the corresponding group () in the regexstring
            (integer which specifies the position of the group in the string).

        b_fname_ugly: boolien to specify if the filename still might follow the old
            chinlab nameing convention which was unable to propper separate slide and mscens
            by a single separator character.

        s_wd: working directory. default is present working directory.

    output:
        df_img: dataframe with extracted information.
            index is filename, index.name is file system path.

    description:
        generic function to find files in the s_wd specified work directory,
        that matches the regex string s_regex and extract the information,
        defined as regex groups () in the s_regex string and labeled in di_regex.
    '''
    # set column and index
    ls_column = sorted(di_regex.keys())
    ls_index = []
    lls_data = []

    for s_file in sorted(os.listdir(s_wd)):
        # deal with legacy slide_pxscene in file name. there has to be an underscore, the rest does not matter.
        s_input = s_file
        if b_fname_ugly:
            s_input = s_file.replace('-Scene-','_scene')
        # for each file that matches the regex
        #print('check:', s_regex, s_input)
        o_found = re.search(s_regex, s_input)
        if not (o_found is None):
            # update index
            ls_index.append(s_file)
            # extract information
            ls_row = []
            for s_column in ls_column:
                ls_row.append(o_found[di_regex[s_column]])
            # update data block
            lls_data.append(ls_row)

    # generate dataframe
    df_img = pd.DataFrame(lls_data, index=ls_index, columns=ls_column)

    # handle slide mscene and scene
    if ('slide' in ls_column) and ('mscene' in ls_column):
        df_img['slide_mscene'] = df_img.slide + '_' + df_img.mscene
    if ('slide' in ls_column) and ('scene' in ls_column):
        df_img['slide_scene'] = df_img.slide + '_' + df_img.scene

    # handle round
    # bue 20210614: why are all of those needed? round_int, round_ord, and round_num
    # bue 20210629: int (int) real (ord) order (num) would be more precise!
    df_img['round_int'] = [int(re.sub('[^0-9-]','', s_item)) for s_item in df_img.loc[:,'round']]
    df_img['round_real'] = [float(re.sub('[^0-9.-]','', re.sub(config.d_nconv['s_quenching'],'.5', s_item))) for s_item in df_img.loc[:,'round']] # round_ord
    df_img['round_order'] = None
    for i_order, r_round in enumerate(sorted(df_img.round_real.unique())):
        df_img.loc[df_img.round_real == r_round, 'round_order'] = i_order  # round_num

    # working directory information
    df_img.index.name = s_wd

    # output
    #print(df_img)
    return(df_img)


def _handle_colormarker(df_img):
    '''
    version: 2021-06-29

    input:
        df_img: dataframe with parsed filenames.

    output:
        df_img: updated dataframe

    decscription:
        this function will extract the single file related marker
        from ther already parese color, round, and markers infromation.
    '''
    # handle input
    ls_color =  config.d_nconv['ls_color_order'].copy()
    ls_color.pop(ls_color.index(config.d_nconv['s_color_dapi']))

    # parse file name for biomarker
    df_img['marker'] = ''
    for s_index in df_img.index:
        #print(f'process: {s_index}')
        # get marker by channel
        s_color = df_img.loc[s_index,'color']
        if (s_color == config.d_nconv['s_color_dapi']):
            r_round = df_img.loc[s_index,'round_real']
            i_round = df_img.loc[s_index,'round_int']
            if (i_round < r_round):
                s_marker = config.d_nconv['s_marker_dapi'] + str(i_round) + config.d_nconv['s_quenching']  # or str(round(r_round,1))
            else:
                s_marker = config.d_nconv['s_marker_dapi'] + str(i_round)
        else:
            ls_marker = df_img.loc[s_index,'markers'].split(config.d_nconv['s_sep_marker'])
            s_marker = ls_marker[ls_color.index(s_color)]
        # update marker
        df_img.loc[s_index,'marker'] = s_marker

    # output
    #print(df_img.info())
    return(df_img)


def parse_czi_original(s_wd='./'):
    '''
    version: 2021-06-28

    input:
        s_wd: working directory.

    output:
        df_img: dataframe with parsed filenames.

    decscription:
        wraper function to parse oroginal czi image splitscenes.
    '''
    df_img = _parse_file(
        s_regex = config.d_nconv['s_regex_czi_original'],
        di_regex = config.d_nconv['di_regex_czi_original'],
        s_wd = s_wd,
    )
    return(df_img)


def parse_czi_stitched(s_wd='./'):
    '''
    version: 2021-06-28

    input:
        s_wd: working directory.

    output:
        df_img: dataframe with parsed filenames.

    decscription:
        wraper function to parse stitched czi image splitscenes.
    '''
    df_img = _parse_file(
        s_regex = config.d_nconv['s_regex_czi_stitched'],
        di_regex = config.d_nconv['di_regex_czi_stitched'],
        s_wd = s_wd,
    )
    return(df_img)


def parse_czi_splitscene(s_wd='./'):
    '''
    version: 2021-06-28

    input:
        s_wd: working directory.

    output:
        df_img: dataframe with parsed filenames.

    decscription:
        wraper function to parse raw czi image splitscenes.
    '''
    df_img = _parse_file(
        s_regex = config.d_nconv['s_regex_czi_splitscene'],
        di_regex = config.d_nconv['di_regex_czi_splitscene'],
        s_wd = s_wd,
    )
    return(df_img)


def parse_tiff_raw(s_wd='./'):
    '''
    version: 2021-06-29

    input:
        s_wd: working directory.

    output:
        df_img: dataframe with parsed filenames

    decscription:
        wraper function to parse raw tiff image filenames.
    '''
    df_img = _parse_file(
        s_regex = config.d_nconv['s_regex_tiff_raw'],
        di_regex = config.d_nconv['di_regex_tiff_raw'],
        s_wd = s_wd,
    )
    _handle_colormarker(df_img=df_img)
    return(df_img)


def parse_tiff_reg(s_wd='./'):
    '''
    version: 2021-06-29

    input:
        s_wd: working directory.

    output:
        df_img: dataframe with parsed filenames

    decscription:
        wraper function to parse registered tiff image filenames.
    '''
    df_img = _parse_file(
        s_regex = config.d_nconv['s_regex_tiff_reg'],
        di_regex = config.d_nconv['di_regex_tiff_reg'],
        s_wd = s_wd,
        b_fname_ugly = True,
    )
    _handle_colormarker(df_img=df_img)
    return(df_img)


##################
# exposure time  #
##################
def add_exposure(
        df_img,
        s_metadir = config.d_nconv['s_metadir'],  #'./MetaImages/'
    ):
    '''
    version: 2021-06-22

    input:
        df_img: dataframe of images with columns [ 'color', 'exposure', 'marker','sub_image','sub_exposure'] and index with image names
        s_metadir: folder where the extracted image metadata is stored.

    output:
        df_img: updated dataframe

    description:
        load exposure time csv (generated with imgmeta.fetch_meta_batch)
        and merge this information
        with the parsed filename imput data provided by df_img.
    '''
    # handle input
    s_wd = df_img.index.name
    df_img = df_img.reset_index()

    # load metadata
    df_exposure = pd.DataFrame()
    for s_slide in df_img.slide.unique():
        df_load = imgmeta.load_exposure_df(
            s_slide = s_slide,
            s_metadir = s_metadir,
        )
        df_exposure = df_exposure.append(df_load)

    # merge
    df_img = pd.merge(df_img, df_exposure, on=['slide','markers','round','round_int','round_real','round_order','color','marker'])
    df_img.set_index(s_wd, inplace=True)

    # output
    return(df_img)


#########
# util #
########

def find_last_round(
        df_img,  # can be any paresd filename dataframe, also the tresholdli file!
        es_marker_needed,  # e.g. ('DAPI2','DAPI11_nuc','Ecad')  #
    ):
    '''
    version: 2021-06-16

    input:
        df_img: dataframe that have parsed all relevant registed images filenames.
        es_marker_needed: marker that have to be in the final dataset.

    output:
        i_last_round: the last round.
        es_marker_drop: marker appearing after the last round.

    description:
        find i_last_round accoruing to an ok marker set.
        this function will preserve adjacent quenching round used e.g. for autofluorescent subtraction.
    '''
    # find the rounds from all the needed marker
    es_marker = set([s_marker.split('_')[0] for s_marker in es_marker_needed])
    print('bue', es_marker)
    i_last_round = df_img.loc[df_img.marker.isin(es_marker),'round_int'].max() # function will keep the quenching round, if it is adjacent to the last marker round.
    es_marker_drop = set([s_marker + '_' for s_marker in df_img.loc[df_img.round_int > i_last_round, 'marker'].unique()])  # all marker that are higher then the detected round.
    print(f'markers occuring after round {i_last_round}: {sorted(es_marker_drop)}')
    return(i_last_round, es_marker_drop)


def marker_table(
        s_slide_pxscene,
        s_batch = '',
        s_regdir = config.d_nconv['s_regdir'],  #'./RegisteredImages/',
        s_format_regdir = config.d_nconv['s_format_regdir'],  #'{}{}/',  # s_regdir, s_slide_pxscene
    ):
    '''
    version: 2021-06-03

    input:
        s_slide_pxscene: slides_pxscene from which the marker_table wil be generated.
            note: only one pxscene have to be given, thouth
            the spit out marker table will be valid for its entier batch.
        s_batch: batch id. if empty, file will be generated,
            though filename and index.name will mis batch information.
        s_regdir: registartion directory.
        s_format_regdir: format string for registration dir subdirectory where the images are.

    output:
        MarkerTable.csv file in the s_regdir directory

    description:
        generate marker table for a batch.
        one slide_scene is enough to generate the whole table.
        this is just nice rounds/channels/markers table for display.
    '''
    print(f'run jinxif.basic.marker_table for: {s_slide_pxscene}')

    # generate table
    df_img = parse_tiff_reg(s_wd=s_format_regdir.format(s_regdir, s_slide_pxscene))
    df_marker = df_img.loc[
        df_img.slide_scene == s_slide_pxscene,
        ['marker','round','color']
    ].pivot(index='round',columns='color', values='marker')
    df_marker.index.name = 'index'
    df_marker.columns.name = ''

    # order table
    df_marker['order'] = df_marker.index
    df_marker.order = [float(re.sub(r'[^\d.]','', s_round.replace(config.d_nconv['s_quenching'],'.5'))) for s_round in df_marker.order]
    df_marker.sort_values('order', inplace=True)
    df_marker.drop('order', inplace=True, axis=1)

    # ouput
    s_ofile = 'MarkerTable.csv'
    if s_batch != '':
        df_marker.index.name = s_batch
        s_ofile = f'{s_batch}_' + s_ofile
    df_marker.to_csv(s_regdir + s_ofile)
    print('df_marker:', df_marker.info())
    print(f'write to file: {s_regdir}{s_ofile}')
    return(df_marker)

