clear all; clc
%% import
in = dlmread('../data/IMU_data.txt', ' ', 2);
channel = [2,3,4]
t = in(:, 1);

%% calc
T = in(end,1)-in(1,1)
k = 1:length(in(:,channel));
freqs = T./k;
f = fft(in(:, channel))/length(in(:, channel));

%% plots
subplot(3, 1, 1)
plot(t, in(:, channel))
title('Acceleration of IMU')
legend('a_x','a_y','a_z')
xlabel('number of samples')
grid on

subplot(3, 1, 2)
plot(freqs,f)
title('Frequency spectrum of acceleration')

subplot(3, 1, 3)
plot(t, in(:, 5))

saveas(gcf, 'fig/imu_accel_data.svg')