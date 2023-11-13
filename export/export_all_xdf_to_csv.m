% Add the required path
% addpath('xdf-Matlab-1.14');

% Base file name
base_file_name = '';  % You can change this to your desired base name
counter = 1;

% Get all files in the current directory
files = dir();

% Loop through each file
for i = 1:length(files)
    [~, ~, ext] = fileparts(files(i).name);
    if strcmp(ext, '.xdf')
        % Define the csv name based on the base file name and counter
        csv_name = sprintf('%s%d.csv', base_file_name, counter);
        xdf2csv_func(files(i).name, csv_name);
        counter = counter + 1;
    end
end

function xdf2csv_func(xdf_name, csv_name)
    streams = load_xdf(xdf_name);
    wh = size(streams);
    fp = fopen(csv_name, 'w+');
    for h = 1:wh(1)
        for w = 1:wh(2)
            cell_data = streams{h, w};
            if ~strcmp('Mocap', cell_data.info.type)
                continue
            end
            desc = cell_data.info.desc;
            
            channels = desc.channels.channel;
          
            time_series = cell_data.time_series;
            time_stamps  = cell_data.time_stamps;

            time_series_size = size(time_series);
            
            num_channals  = time_series_size(1);
            num_frames = time_series_size(2);

            % Write header
            fprintf(fp, ',Name');
            for c = 1:num_channals
                if isfield(channels{1, c}, 'marker')
                    fprintf(fp, ', %s', channels{1, c}.marker);
                else
                    fprintf(fp, ', %s', channels{1, c}.object);
                end
            end
            fprintf(fp, '\n');
            fprintf(fp, ',');
            for c = 1:num_channals
                fprintf(fp, ', %s', channels{1, c}.type(1: length(channels{1, c}.type) - 1)); 
            end
            fprintf(fp, '\n');
            fprintf(fp, 'Frame, Time(Seconds)');
            for c = 1:num_channals
                fprintf(fp, ', %s', channels{1, c}.type(length(channels{1, c}.type): length(channels{1, c}.type))); 
            end
            fprintf(fp, '\n');
            
            for f = 1:num_frames
                d = time_series(:, f);
                len = size(d);

                fprintf(fp, '%d, %f', f - 1, time_stamps(1, f));
                for i = 1:len
                   fprintf(fp, ', %f', d(i)); 
                end
                fprintf(fp, '\n');
            end
        end
    end
    
    fclose(fp);
end
