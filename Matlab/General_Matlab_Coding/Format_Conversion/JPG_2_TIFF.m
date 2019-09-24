%--------------------------- Script description---------------------------%
% Purpose: Converting JPEG images to TIFF
% Created: 04/09/19 by Or Perlman (or@ieee.org)
% Notes: 
% Cnanges log:
%-------------------------------------------------------------------------%

close all;clc;
 
%making figures to have white background
set(0,'defaultfigurecolor',[1 1 1])

% initializing graphic parameters
set(0, 'DefaultAxesLineWidth', 1.2, 'DefaultAxesFontSize', 12, ...
          'DefaultAxesFontWeight', 'bold', 'DefaultAxesFontname','Times New Roman',...
          'DefaultLineLineWidth', .2, 'DefaultLineMarkerSize', 8);

%Docking figures
set(0,'DefaultFigureWindowStyle','docked')
% set(0,'DefaultFigureWindowStyle','normal') %undocking figures

% Strings for original and output file names
Original_File_Name='Figure1.jpg';
New_File_Name='Figure1.tiff';

%Reading JPEG Im
JPEG_Im=imread(Original_File_Name);

%Saving as TIFF
imwrite(JPEG_Im,New_File_Name);
