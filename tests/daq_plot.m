clear all; clc
%% import
in = dlmread('../data/IMU_data.txt')
channel = [2,3,4]

%% calc
T = in(end,1)-in(1,1)
k = 1:length(in(:,channel));
freqs = T./k;
f = fft(in(:, channel))/length(in(:, channel));

%% plots
subplot(2, 1, 1)
plot(in(:, channel))
title('Acceleration of IMU')
legend('a_x','a_y','a_z')
xlabel('number of samples')
grid on

subplot(2, 1, 2)
plot(freqs,f)
title('Frequency spectrum of acceleration')
