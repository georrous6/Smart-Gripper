% PID initial values
Kp = 100;
Ki = 50;
Kd = 0.1;

% Learning rate
learning_rate = 0.0001;

% Desired output (target)
target_value = 5.4394;
desired_settling_time = 1; % sec

% Time parameters
dt = 0.001;
max_time = 0.5;
t_vec = 0:dt:max_time;

% PID variable initialization
integral = 0;
previous_error = 0;

% History for settling time
output_history = zeros(size(t_vec));
time_history = zeros(size(t_vec));
y = 0; % Initial system value

% Model: 1st order system (e.g. RC circuit)

% ---------------- BLDC PARAMETERS -------------------
R = 50;      % Ohm
L = 0.1;     % Henry
Ke = 1;      % V/(rad/s)
Kt = 1;      % Nm/A
J = 1e-2;    % kg*m^2
B = 1e-3;    % N*m*s

% ---------------- INITIAL VALUES ---------------------
omega = 0;        % speed (rad/s)
current = 0;      % current (A)

for i = 1:length(t_vec)
    t = t_vec(i);

    % ---------------- PID CONTROL -------------------
    error = target_value - omega;
    integral = integral + error * dt;
    derivative = (error - previous_error) / dt;
    V_in = Kp * error + Ki * integral + Kd * derivative; % voltage control

    % ---------------- BLDC MODEL -------------------
    % Electrical equation: di/dt = (V - R*i - Ke*ω) / L
    di = (V_in - R * current - Ke * omega) / L;
    current = current + di * dt;

    % Mechanical equation: dω/dt = (Kt*i - B*ω) / J
    domega = (Kt * current - B * omega) / J;
    omega = omega + domega * dt;

    % ---------------- UPDATE ---------------------
    previous_error = error;

    % History
    y = omega+0.05*randn(1,1);  % our "output" is the speed
    output_history(i) = y;
    time_history(i) = t;

    % Settling time
    settling_time = calculateSettlingTime(output_history(1:i), time_history(1:i), target_value);

    % Gradient descent for PID tuning
    error2 = desired_settling_time - settling_time;
    grad = 0.1 * (error + error2);

    Kp = Kp - learning_rate * grad;
    Ki = Ki - learning_rate * grad;
    Kd = Kd - learning_rate * grad;

    % Display
    fprintf('t=%.2f, omega=%.2f, settling=%.2f, Kp=%.2f, Ki=%.2f, Kd=%.2f\n', ...
            t, omega, settling_time, Kp, Ki, Kd);
end

% Plot
figure;
plot(t_vec, output_history, 'b-', 'LineWidth', 2);
hold on;
yline(target_value, 'r--', 'Target');
xlabel('Time (s)');
ylabel('Output');
title('System Response with Adaptive PID');
grid on;


% Time instances
t = 0:0.001:0.5;

% Taking output data (we took that data from optimized control)
noisy_signal = output_history;

% ----------------------
% Implementation of Wiener filter
% ----------------------
filtered_signal = wiener2(noisy_signal, [1 10]); % Wiener filter for 150 samples per estimation

% ----------------------
% Drawing
% ----------------------
figure;
plot(t, filtered_signal, 'b', 'LineWidth', 1.5);
legend('Wiener Filtered');
xlabel('Time (s)');
ylabel('Amplitude');
title('Wiener Filtering on Noisy Signal');
grid on;




function settling_time = calculateSettlingTime(output, time, target)
    tolerance = 0.05; % ±5% margin
    lower_bound = target * (1 - tolerance);
    upper_bound = target * (1 + tolerance);

    % Find time points within bounds
    idx = find(output >= lower_bound & output <= upper_bound);

    % If it has recently stabilized
    if isempty(idx)
        settling_time = time(end); % not yet settled
    else
        % Check if it remains within bounds from a certain point onward
        last_idx = idx(find(diff(idx) > 1, 1, 'last') + 1); % start of continuous section
        if isempty(last_idx)
            last_idx = idx(1);
        end
        if all(output(last_idx:end) >= lower_bound & output(last_idx:end) <= upper_bound)
            settling_time = time(last_idx);
        else
            settling_time = time(end);
        end
    end
end
