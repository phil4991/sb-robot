clear all; clc
in = dlmread('IMU_data.txt')
%dt = diff(in(:, 1))

T = in(end,1)-in(1,1)
k = 1:length(in(:,2));
freqs = T./k
f = fft(in(:, 2))/length(in(:, 2))

subplot(2, 1, 1)
plot(in(:, 2))

subplot(2, 1, 2)
plot(freqs,f)
