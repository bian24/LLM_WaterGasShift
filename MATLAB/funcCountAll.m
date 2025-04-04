function [nCounts] = funcCountAll(fMetrics, nNbQuestions)

nCounts = [ ...
[1.00 sum(fMetrics > 1.00) / nNbQuestions] ; ...
[0.99 sum(fMetrics > 0.99) / nNbQuestions] ; ...
[0.98 sum(fMetrics > 0.98) / nNbQuestions] ; ...
[0.97 sum(fMetrics > 0.97) / nNbQuestions] ; ...
[0.96 sum(fMetrics > 0.96) / nNbQuestions] ; ...
[0.95 sum(fMetrics > 0.95) / nNbQuestions] ; ...
[0.94 sum(fMetrics > 0.94) / nNbQuestions] ; ...
[0.93 sum(fMetrics > 0.93) / nNbQuestions] ; ...
[0.92 sum(fMetrics > 0.92) / nNbQuestions] ; ...
[0.91 sum(fMetrics > 0.91) / nNbQuestions] ; ...
[0.90 sum(fMetrics > 0.90) / nNbQuestions] ; ...
[0.89 sum(fMetrics > 0.89) / nNbQuestions] ; ...
[0.88 sum(fMetrics > 0.88) / nNbQuestions] ; ...
[0.87 sum(fMetrics > 0.87) / nNbQuestions] ; ...
[0.86 sum(fMetrics > 0.86) / nNbQuestions] ; ...
[0.85 sum(fMetrics > 0.85) / nNbQuestions] ; ...
[0.84 sum(fMetrics > 0.84) / nNbQuestions] ; ...
[0.83 sum(fMetrics > 0.83) / nNbQuestions] ; ...
[0.82 sum(fMetrics > 0.82) / nNbQuestions] ; ...
[0.81 sum(fMetrics > 0.81) / nNbQuestions] ; ...
[0.80 sum(fMetrics > 0.80) / nNbQuestions] ; ...
[0.79 sum(fMetrics > 0.79) / nNbQuestions] ; ...
[0.78 sum(fMetrics > 0.78) / nNbQuestions] ; ...
[0.77 sum(fMetrics > 0.77) / nNbQuestions] ; ...
[0.76 sum(fMetrics > 0.76) / nNbQuestions] ; ...
[0.75 sum(fMetrics > 0.75) / nNbQuestions] ; ...
[0.74 sum(fMetrics > 0.74) / nNbQuestions] ; ...
[0.73 sum(fMetrics > 0.73) / nNbQuestions] ; ...
[0.72 sum(fMetrics > 0.72) / nNbQuestions] ; ...
[0.71 sum(fMetrics > 0.71) / nNbQuestions] ; ...
[0.70 sum(fMetrics > 0.70) / nNbQuestions] ; ...
[0.65 sum(fMetrics > 0.65) / nNbQuestions] ; ...
[0.60 sum(fMetrics > 0.60) / nNbQuestions] ; ...
[0.55 sum(fMetrics > 0.55) / nNbQuestions] ; ...
[0.50 sum(fMetrics > 0.50) / nNbQuestions] ; ...
[0.45 sum(fMetrics > 0.45) / nNbQuestions] ; ...
[0.40 sum(fMetrics > 0.40) / nNbQuestions] ; ...
[0.35 sum(fMetrics > 0.35) / nNbQuestions] ; ...
[0.30 sum(fMetrics > 0.30) / nNbQuestions] ; ...
[0.25 sum(fMetrics > 0.25) / nNbQuestions] ; ...
[0.20 sum(fMetrics > 0.20) / nNbQuestions] ; ...
[0.15 sum(fMetrics > 0.15) / nNbQuestions] ; ...
[0.10 sum(fMetrics > 0.10) / nNbQuestions] ; ...
[0.05 sum(fMetrics > 0.05) / nNbQuestions] ; ...
[0.00 sum(fMetrics > 0.00) / nNbQuestions] ; ...
]

%sum(fMetrics > 0.50)
%sum(fMetrics > 0.50) / nNbQuestions
