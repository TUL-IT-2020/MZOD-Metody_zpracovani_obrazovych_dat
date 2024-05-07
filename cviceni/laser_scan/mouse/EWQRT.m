fileID = fopen('FileList.txt','r'); %otevreni seznamu
textdata = textscan(fileID,'%s');  %nacten
fclose(fileID); % zavreni seznamu
files = string(textdata{:}); %pole souboru i s cestami