%% robot control parameter script 2019-10-01
% 
clear all; clc


%% parameters
% simulation
t_sim = 5; % s
dt = 1e-5;

% system
m = 1;
g = 9.81;
l = 0.2;
J = m*l^2;

phi_start = 0;
w_start = 0;

G_s_num = [1/(m*g)];
G_s_denom = [-J/(m*g*l) 0 1];

% signal IN
% ramped
t0 = 0;
t1 = .3; t2 = 1;
a0 = .1; a1 = -.2; a2 = .1;

% sine
f_F = 2;
F_amp = 0.1;

% controller
KP = -50;
KI = 0;
KD = 3;

G_cInum = [KI];
G_cIdenom = [1 0];

G_cDnum = [KD];
G_cDdenom = [0];

%% simulation

sim('robot_control_model')


%% analysis 

H = tf(G_s_num, G_s_denom);

ax = bodeplot(H);
xlim([1e-1 1e2])
grid on

opt = getoptions(ax);
% setoptions(ax, opt)

