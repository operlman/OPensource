%--------------------------- Script description---------------------------%
% Purpose: 
% Created: XX/XX/XX by Or Perlman (or@ieee.org)
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

%Reseting paths to default to avoid ambiguity
pathtool %Then choose default

