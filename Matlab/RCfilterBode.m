clear
clc
close all

%% RC low-pass filter parameters
R = 1000;          % Resistance [ohm]
C = 100e-9;        % Capacitance [F]

%% Cutoff frequency
fc = 1/(2*pi*R*C);

fprintf('Cutoff frequency fc = %.2f Hz\n', fc);

%% Frequency vector
% 10 Hz to 100 kHz, logarithmically spaced
f = logspace(1, 5, 1000);

omega = 2*pi*f;

%% Transfer function
% H(jw) = 1 / (1 + jwRC)
H = 1 ./ (1 + 1j*omega*R*C);

%% Magnitude
mag = abs(H);
mag_dB = 20*log10(mag);

%% Phase
phase_deg = angle(H) * 180/pi;

%% Measured oscilloscope data
f_meas    = [100 1592 10000];      % [Hz]
Vin_meas  = [1.008 0.984 0.960];   % [Vpp]
Vout_meas = [1.000 0.720 0.184];   % [Vpp]

gain_meas = Vout_meas ./ Vin_meas;
gain_meas_dB = 20*log10(gain_meas);

%% Display measured results
fprintf('\nMeasured data:\n');
fprintf('Frequency [Hz]   Vin [Vpp]   Vout [Vpp]   Gain [dB]\n');

for k = 1:length(f_meas)
    fprintf('%10.0f       %6.3f      %6.3f      %7.3f\n', ...
        f_meas(k), Vin_meas(k), Vout_meas(k), gain_meas_dB(k));
end

%% Asymptotic Bode magnitude approximation

mag_asym_dB = zeros(size(f));

below_fc = f <= fc;
above_fc = f > fc;

mag_asym_dB(below_fc) = 0;

mag_asym_dB(above_fc) = ...
    -20*log10(f(above_fc)/fc);

%% Magnitude Bode plot
figure

semilogx(f, mag_dB, ...
    'LineWidth', 1.5, ...
    'DisplayName', 'Theory')

hold on

semilogx(f, mag_asym_dB, '--', ...
    'LineWidth', 1.2, ...
    'DisplayName', 'Asymptotic approximation')

semilogx(f_meas, gain_meas_dB, 'o', ...
    'MarkerSize', 8, ...
    'LineWidth', 1.5, ...
    'DisplayName', 'Measured')

xline(fc, '--', 'Cutoff frequency', ...
    'HandleVisibility', 'off')

yline(-3.0103, '--', '-3.01 dB', ...
    'HandleVisibility', 'off')

grid on
xlabel('Frequency (Hz)')
ylabel('Magnitude (dB)')
title('RC Low-Pass Filter - Magnitude')
legend('Location', 'best')

%% Measured phase data
f_phase_meas = 1592;          % Hz
dt_meas = 72e-6;              % measured time delay [s]

T_meas = 1/f_phase_meas;      % period [s]

phase_meas = -360 * dt_meas / T_meas;

fprintf('\nMeasured phase:\n');
fprintf('dt = %.1f us\n', dt_meas*1e6);
fprintf('T  = %.1f us\n', T_meas*1e6);
fprintf('Phase = %.2f deg\n', phase_meas);

%% Measured resistor-capacitor phase difference

dt_RC = 156e-6;                 % measured VR-to-VC delay [s]
phase_RC = 360 * dt_RC / T_meas;

fprintf('\nMeasured VR-VC phase difference:\n');
fprintf('dt = %.1f us\n', dt_RC*1e6);
fprintf('Phase = %.2f deg\n', phase_RC);

%% Asymptotic phase approximation

phase_asym = zeros(size(f));

low_phase  = f < 0.1*fc;
mid_phase  = f >= 0.1*fc & f <= 10*fc;
high_phase = f > 10*fc;

phase_asym(low_phase) = 0;

phase_asym(mid_phase) = ...
    -45 * log10(f(mid_phase)/(0.1*fc));

phase_asym(high_phase) = -90;

%% Phase Bode plot
figure

semilogx(f, phase_deg, ...
    'LineWidth', 1.5, ...
    'DisplayName', 'Theory')

hold on

semilogx(f, phase_asym, '--', ...
    'LineWidth', 1.2, ...
    'DisplayName', 'Asymptotic approximation')

semilogx(f_phase_meas, phase_meas, 'o', ...
    'MarkerSize', 8, ...
    'LineWidth', 1.5, ...
    'DisplayName', 'Measured')

xline(fc, '--', 'Cutoff frequency', ...
    'HandleVisibility', 'off')

yline(-45, '--', '-45 deg', ...
    'HandleVisibility', 'off')

grid on
xlabel('Frequency (Hz)')
ylabel('Phase (degrees)')
title('RC Low-Pass Filter - Phase')
legend('Location', 'best')

%% Theoretical values at measured frequencies
omega_meas = 2*pi*f_meas;

H_theory_meas = 1 ./ (1 + 1j*omega_meas*R*C);

mag_theory_meas = abs(H_theory_meas);
mag_theory_meas_dB = 20*log10(mag_theory_meas);
phase_theory_meas = angle(H_theory_meas)*180/pi;

fprintf('\nTheory at measured frequencies:\n');
fprintf('Frequency [Hz]   Gain [dB]   Phase [deg]\n');

for k = 1:length(f_meas)
    fprintf('%10.0f       %7.3f      %8.2f\n', ...
        f_meas(k), ...
        mag_theory_meas_dB(k), ...
        phase_theory_meas(k));
end