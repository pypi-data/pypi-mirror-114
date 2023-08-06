%%%%%%%%
% Title: template_registration_mscene.m
%
% Author: Young, Jenny, bue
% License: GPLv>=3
% Version: 2021-04-23
%
% Description: 
%   Template script for matlab based IF registration for
%   one slide, one microscopy scene, all microscopy channel cyclic images.
%
% Intructions:
%   Use mplex_image.regist.registration function to edit and run this template.
%
% Input :
%   Tiffs or big tiffs (>4GB) with filename eding in m_regex_ext.
%   There can be as many files in the m_src_dir input folder as they want,
%   though m_regex_round, m_regex_marker, m_regex_micchannel and
%   m_imgall_glob, m_imgdapi_glob, m_imgdapi_ref_glob have to be slide_mscene specific,
%   what ever naming convention you follow.
%
%   E.g. ChinLab filename convention is:
%   Rx_Bi.o.mark.ers_Slidename-Section(-Scene)_xxx_xx_x_cx_ORG.tif,
%   where c1 is DAPI and x can be variable (i.e. from axioscan)
%
% Output:
%    The output tiff files in m_dst_dir folder will follow the namingconvention:
%    Registered-round<>marker<>slidepxscene<>micchanel<>ext
%    Make sure that you integarte a separater (symbolized by <>) into your regex patterns.
%%%%%%%%%%%%%%%%

% input parameters
m_slide = 'peek_s_slide';  % slide label which will be used in the filename
m_mscene = 'peek_s_mscene';  % bue 20210423: will this be used at all?
m_pxscene = peek_sls_pxscene;  % list of pxscene label strings string
m_crop = peek_sll_pxcrop;  % list of list of crop coordinates string
m_regex_ext = 'peek_s_regex_ext';  % file extension rexgex pattern
m_regex_round = 'peek_s_regex_round';  % staining round regexp pattern
m_regex_marker = 'peek_s_regex_marker';  % stain regex pattern
m_regex_micchannel = 'peek_s_regex_micchannel';  % microscopy channel regex pattern
m_imgall_glob = 'peek_s_imgall_glob';  % slide_mscene specific image glob pattern for all channels
m_imgdapi_glob = 'peek_s_imgdapi_glob';  % slide_mscene specific dapi channel image glob pattern
m_imgdapi_ref_glob = 'peek_s_imgdapi_ref_glob';  % slide_mscene specific round 1 dapi channel image glob pattern
m_src_dir = 'peek_s_src_dir';  % location of raw images folder
m_dst_dir = 'peek_s_dst_dir';  % location of folder where registered images will be stored
m_npoint = peek_i_npoint;  % number of features to detect in image (default = 10000)


% specify run
sprintf('\nrun slide mscene: %s%s', m_slide, m_mscene)
sprintf('input path: %s', m_src_dir)
sprintf('output path: %s', m_dst_dir)

% get dapi reference file name
m_filedapi_ref = dir(strcat(m_src_dir, m_imgdapi_ref_glob));
if length(m_filedapi_ref) < 1
   sprintf(strcat('Error: no reference file found with glob:', m_src_dir, m_imgdapi_ref_glob))
   %exit
elseif length(m_filedapi_ref) > 1
   sprintf(strcat('Error: more then 1 reference file found with glob:', m_src_dir, m_imgdapi_ref_glob))
   %exit
end

% get dapi file name for all rounds
m_filedapi = dir(strcat(m_src_dir, m_imgdapi_glob));
if length(m_filedapi) < 1
   sprintf(strcat('Error: no DAPI files found with glob:', m_src_dir, m_imgdapi_glob))
   %exit
end

% get all file name for all rounds
m_fileall = dir(strcat(m_src_dir, m_imgall_glob));
if length(m_fileall) < 1
   sprintf(strcat('Error: no files found with glob:', m_src_dir, m_imgall_glob))
   %exit
end


%% handle refernce round %%
sprintf('get keypoints reference round DAPI image: %s', m_filedapi_ref.name)

% load dapi refernce file and get key points
m_dapi_ref = imread(strcat(m_src_dir, m_filedapi_ref.name));  % load DAPI reference file
m_dapi_ref = imadjust(m_dapi_ref);  % adjust DAPI R1
m_point_ref = detectSURFFeatures(m_dapi_ref);  % detect features of DAPI refernce (alternative methode detectKAZEFeatures)
m_point_ref = m_point_ref.selectStrongest(m_npoint);  % select m_point (e.g. 10000) strongest feature
[m_feature_ref, m_validpoint_ref] = extractFeatures(m_dapi_ref, m_point_ref);  % get features and locations of DAPI R1

% get reference coordinate system
m_outputview_ref = imref2d(size(m_dapi_ref));

% clear
clear m_dapi_ref;
clear m_point_ref;

% extract round, marker, and file extension metadata from file name
m_round = regexp(m_filedapi_ref.name, m_regex_round, 'tokens');
m_round = m_round{1}{1};
m_marker = regexp(m_filedapi_ref.name, m_regex_marker, 'tokens');
m_marker = m_marker{1}{1};
m_ext = regexp(m_filedapi_ref.name, m_regex_ext, 'tokens');
m_ext = m_ext{1}{1};

% for each file form this round
for i = 1:length(m_fileall)
    if contains(m_fileall(i).name, m_round)
        sprintf('process reference round DAPI and non-DAPI image: %s', m_fileall(i).name)

        % extract microscopy metadata for file name
        m_micchannel = regexp(m_fileall(i).name, m_regex_micchannel, 'tokens');
        m_micchannel = m_micchannel{1}{1};

        % load file
        m_img = imread(strcat(m_src_dir, m_fileall(i).name));

        % for each pxscene
        for j = 1:length(m_crop)

            % crop
            if strcmp(m_crop{j},'none')
                m_imgj = m_img;
            else
                m_imgj = imcrop(m_img, m_crop{j});
            end

            % save file
            s_pathfilename = sprintf('%s%s%s/Registered-%s%s%s%s%s%s', m_dst_dir, m_slide, m_pxscene{j}, m_round, m_marker, m_slide, m_pxscene{j}, m_micchannel, m_ext);
            sprintf('write file: %s', s_pathfilename)
            mkdir(strcat(m_dst_dir, m_slide, m_pxscene{j}));
            imwrite(m_imgj, s_pathfilename);

            % clean
            clear m_imgj;
        end
        clear m_img;
    end
end


%% registration loop %%
for i = 1:length(m_filedapi)

    % for each non reference dapi file
    if not(strcmp(m_filedapi(i).name, m_filedapi_ref.name))
        sprintf('\nget keypoints non-reference round DAPI image: %s', m_filedapi(i).name)

        % load non-reference dapi file and get key points
        m_dapi = imread(strcat(m_src_dir, m_filedapi(i).name));  % load non-reference DAPI file
        m_dapi = imadjust(m_dapi);  % adjust non-refrence DAPI image
        m_point = detectSURFFeatures(m_dapi);  % detect features of non-reference DAPI (alternative methode detectKAZEFeatures)
        m_point = m_point.selectStrongest(m_npoint);  % select m_point (e.g. 10000) strongest feature
        [m_feature_obj, m_validpoint_obj] = extractFeatures(m_dapi, m_point);  % get features and locations of non-refrence DAPI

        % get key point reference on reference pairs
        m_indexpair = matchFeatures(m_feature_ref, m_feature_obj);
        m_matched_ref = m_validpoint_ref(m_indexpair(:,1));  % validPtsRef
        m_matched_obj = m_validpoint_obj(m_indexpair(:,2));  % validPtsObj

        % actual registration
        [m_tform, m_inlier_distorted, m_inlier_original, m_status] = estimateGeometricTransform(m_matched_obj, m_matched_ref,  'similarity', 'MaxNumTrials',20000, 'Confidence',95, 'MaxDistance',10);
        [m_dapi_registered, m_dapiref_registered] = imwarp(m_dapi, m_tform, 'OutputView',m_outputview_ref);

        % clear
        clear m_dapi;
        clear m_point
        clear m_indexpair;
        clear m_matched_ref;
        clear m_matched_obj;
        clear m_feature_obj;
        clear m_validpoint_obj;
        clear m_inlier_distorted;
        clear m_inlier_original;
        clear m_status;
        clear m_dapi_registered;
        clear m_dapiref_registered;

        % extract round, marker metadata from file name
        m_round = regexp(m_filedapi(i).name, m_regex_round, 'tokens');
        m_round = m_round{1}{1};
        m_marker = regexp(m_filedapi(i).name, m_regex_marker, 'tokens');
        m_marker = m_marker{1}{1};

        % for each file form this round
        for i = 1:length(m_fileall)
            if contains(m_fileall(i).name, m_round)
                sprintf('process non-reference round DAPI and non-DAPI image: %s', m_fileall(i).name)

                % extract microscopy metadata for file name
                m_micchannel = regexp(m_fileall(i).name, m_regex_micchannel, 'tokens');
                m_micchannel = m_micchannel{1}{1};

                % load file
                m_img = imread(strcat(m_src_dir, m_fileall(i).name));

                % transform
                [m_marker_registered, m_markerref_registered] = imwarp(m_img, m_tform, 'OutputView',m_outputview_ref); %transform all rounds 2 and higher

                % clear
                clear m_img;
                clear m_markerref_registered;

                % for each pxscene
                for j = 1:length(m_crop)

                    % crop
                    if strcmp(m_crop{j}, 'none')
                        m_marker_registeredj = m_marker_registered;
                    else
                        m_marker_registeredj = imcrop(m_marker_registered, m_crop{j});
                    end

                    % save file
                    s_pathfilename = sprintf('%s%s%s/Registered-%s%s%s%s%s%s', m_dst_dir, m_slide, m_pxscene{j}, m_round, m_marker, m_slide, m_pxscene{j}, m_micchannel, m_ext);
                    sprintf('write file: %s', s_pathfilename)
                    imwrite(m_marker_registeredj, s_pathfilename);

                    % clear
                    clear m_marker_registeredj;
                end
                clear m_marker_registered;
             end
        end
    end
    clear m_tform;
end
%exit
