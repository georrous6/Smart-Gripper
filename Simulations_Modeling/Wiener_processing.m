% Time instances
t = 0:0.001:10;

% Taking output data (we took that data from optimized control)
noisy_signal = output_history;

% ----------------------
% Implementation of Wiener filter
% ----------------------
filtered_signal = wiener2(noisy_signal, [1 50]); % Wiener filter for 150 samples per estimation

% ----------------------
% Drawing
% ----------------------
figure;
plot(t, noisy_signal, 'r:');
hold on;
plot(t, filtered_signal, 'b', 'LineWidth', 1.5);
legend('Noisy', 'Wiener Filtered');
xlabel('Time (s)');
ylabel('Amplitude');
title('Wiener Filtering on Noisy Signal');
grid on;
