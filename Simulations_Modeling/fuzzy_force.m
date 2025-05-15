% Δημιουργία FIS
fis = mamfis('Name', 'GripperFIS');

% ------------------------
% Input: Weight (grammars)
% ------------------------
fis = addInput(fis, [0 500], 'Name', 'Weight');
fis = addMF(fis, 'Weight', 'gbellmf', [40 2 50], 'Name', 'VeryLight');
fis = addMF(fis, 'Weight', 'gbellmf', [60 2 150], 'Name', 'Light');
fis = addMF(fis, 'Weight', 'gbellmf', [60 2 300], 'Name', 'Medium');
fis = addMF(fis, 'Weight', 'gbellmf', [40 2 450], 'Name', 'Heavy');

% ------------------------
% Input: Hardness (in [0,1])
% ------------------------
fis = addInput(fis, [0 1], 'Name', 'Hardness');
fis = addMF(fis, 'Hardness', 'gbellmf', [0.1 2 0.0], 'Name', 'VerySoft');
fis = addMF(fis, 'Hardness', 'gbellmf', [0.1 2 0.33], 'Name', 'Soft');
fis = addMF(fis, 'Hardness', 'gbellmf', [0.1 2 0.66], 'Name', 'Hard');
fis = addMF(fis, 'Hardness', 'gbellmf', [0.1 2 1.0], 'Name', 'VeryHard');

% ------------------------
% Output (in arbitrary units)
% ------------------------
fis = addOutput(fis, [0 10], 'Name', 'Force');
fis = addMF(fis, 'Force', 'gbellmf', [1.5 2 1], 'Name', 'VeryLow');
fis = addMF(fis, 'Force', 'gbellmf', [1.5 2 3.5], 'Name', 'Low');
fis = addMF(fis, 'Force', 'gbellmf', [1.5 2 6], 'Name', 'Medium');
fis = addMF(fis, 'Force', 'gbellmf', [1.5 2 8.5], 'Name', 'High');

% ------------------------
% Fuzzy Rules 4x4
% ------------------------
ruleList = [
    "If Weight is VeryLight and Hardness is VerySoft then Force is VeryLow"
    "If Weight is VeryLight and Hardness is Soft then Force is Low"
    "If Weight is VeryLight and Hardness is Hard then Force is Low"
    "If Weight is VeryLight and Hardness is VeryHard then Force is Medium"

    "If Weight is Light and Hardness is VerySoft then Force is Low"
    "If Weight is Light and Hardness is Soft then Force is Medium"
    "If Weight is Light and Hardness is Hard then Force is Medium"
    "If Weight is Light and Hardness is VeryHard then Force is High"

    "If Weight is Medium and Hardness is VerySoft then Force is Medium"
    "If Weight is Medium and Hardness is Soft then Force is Medium"
    "If Weight is Medium and Hardness is Hard then Force is High"
    "If Weight is Medium and Hardness is VeryHard then Force is High"

    "If Weight is Heavy and Hardness is VerySoft then Force is Medium"
    "If Weight is Heavy and Hardness is Soft then Force is High"
    "If Weight is Heavy and Hardness is Hard then Force is High"
    "If Weight is Heavy and Hardness is VeryHard then Force is High"
];

fis = addRule(fis, ruleList);

% ------------------------
% Projection FIS
% ------------------------
figure;
plotfis(fis);
title('Fuzzy Inference System Structure');
grid on;

% Calculation (300g, hardness 0.4)
output = evalfis(fis, [300, 0.4]);
disp(['Force output: ', num2str(output)]);

% ------------------------
% membership functions
% ------------------------
figure;
plotmf(fis, 'input', 1);
title('Membership Functions for Weight');
xlabel('Weight (g)');
ylabel('Membership Degree');
grid on;

figure;
plotmf(fis, 'input', 2);
title('Membership Functions for Hardness');
xlabel('Hardness');
ylabel('Membership Degree');
grid on;


figure;
plotmf(fis, 'output', 1);
title('Membership Functions for Force');
xlabel('Force');
ylabel('Membership Degree');
grid on;
% ------------------------
% Surface plot
% ------------------------
[W, H] = meshgrid(0:10:500, 0:0.02:1);
Z = zeros(size(W));

for i = 1:size(W,1)
    for j = 1:size(W,2)
        Z(i,j) = evalfis(fis, [W(i,j), H(i,j)]);
    end
end

figure;
surf(W, H, Z);
xlabel('Weight (g)');
ylabel('Hardness');
zlabel('Force');
title('Fuzzy Surface Output');
