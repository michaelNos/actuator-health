clear
clc
close all

%% Parameters
R = 1000;
C = 100e-9;

fc = 1/(2*pi*R*C);

%% Frequency axis
f = logspace(1,5,1000);
omega = 2*pi*f;

%% One-pole filter
H1 = 1 ./ (1 + 1j*omega*R*C);

mag1_dB = 20*log10(abs(H1));
phase1_deg = angle(H1)*180/pi;

%% Two identical poles
H2 = 1 ./ (1 + 1j*omega*R*C).^2;

mag2_dB = 20*log10(abs(H2));
phase2_deg = angle(H2)*180/pi;

%% Magnitude
figure

semilogx(f, mag1_dB, 'LineWidth', 1.5)
hold on
semilogx(f, mag2_dB, 'LineWidth', 1.5)

xline(fc, '--')

grid on
xlabel('Frequency (Hz)')
ylabel('Magnitude (dB)')
title('One Pole vs Two Poles - Magnitude')
legend('1 pole','2 poles','Location','best')

%% Phase
figure

semilogx(f, phase1_deg, 'LineWidth', 1.5)
hold on
semilogx(f, phase2_deg, 'LineWidth', 1.5)

xline(fc, '--')

grid on
xlabel('Frequency (Hz)')
ylabel('Phase (degrees)')
title('One Pole vs Two Poles - Phase')
legend('1 pole','2 poles','Location','best')