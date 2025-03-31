function showResults2
%=======================================================================BHC
%
% 102 Questions for RAG1 ?
% 110 Questions for RAG2 ?
% 
% 2025-03-21 
%
%=======================================================================BHC

clc
clear
close all

%=======================================================================BHC

strFile    = 'run_DB_1_gpt-4o-mini.csv';
strFileRAG = 'run_DB_1_rag_gpt-4o-mini.csv';
strDB = 'DB1';
strRAG = 'RAG1';

%=======================================================================BHC

strFile    = 'run_DB_2_gpt-4o-mini.csv';
strFileRAG = 'run_DB_2_rag_gpt-4o-mini.csv';
strDB = 'DB2';
strRAG = 'RAG2';

%=======================================================================BHC

strFile    = 'run_DB_1_gpt-4o-mini.csv';
strDB = 'DB1';
strFile    = 'run_DB_2_gpt-4o-mini.csv';
strDB = 'DB2';

strFileRAG = 'run_DB_12_gpt-4o-mini.csv';
strRAG = 'RAG1+RAG2';

%=======================================================================BHC

strFC = 'Factual Correctness';
strRagFC = 'Factual Correctness RAG';
strAR = 'Answer Relevancy';
strRagAR ='Answer Relevancy RAG';
strSS = 'Semantic Similarity';
strRagSS ='Semantic Similarity RAG';

Tbl    = readtable(strFile);
TblRAG = readtable(strFileRAG);

[nNbQuestions, nNbColumns] = size(Tbl);
disp(['nNbQuestions = ' num2str(nNbQuestions)])
disp(['nNbColumns = ' num2str(nNbColumns)])

fMetrics1 = cell2mat(table2cell(Tbl(:,5)));
fMetrics2 = cell2mat(table2cell(Tbl(:,6)));
fMetrics3 = cell2mat(table2cell(Tbl(:,7)));

fMetricsRag1 = cell2mat(table2cell(TblRAG(:,5)));
fMetricsRag2 = cell2mat(table2cell(TblRAG(:,6)));
fMetricsRag3 = cell2mat(table2cell(TblRAG(:,7)));

fAvgMetrics1 = mean(fMetrics1);
fAvgMetrics2 = mean(fMetrics2);
fAvgMetrics3 = mean(fMetrics3);

fAvgMetricsRag1 = mean(fMetricsRag1);
fAvgMetricsRag2 = mean(fMetricsRag2);
fAvgMetricsRag3 = mean(fMetricsRag3);

switch(strDB)
    case 'DB1'
        nTick1 = 0:1:102;
    case 'DB2'
        nTick1 = 0:1:110;
end

switch(strRAG)
    case 'RAG1'
        nTick2 = 0:1:102;
    case 'RAG2'
        nTick2 = 0:1:110;
    case 'RAG1+RAG2'
        nTick2 = 0:1:102+110;
end
%return

%=======================================================================BHC

figure
set(gcf , 'Position', [1 49 2560 1315])
set(gcf, 'Color', 'White')

subplot(6,1,1)
bar(fMetrics1)
hold on
plot([1 max(nTick1)], [fAvgMetrics1 fAvgMetrics1], 'r-')
ylabel(strFC)
xlabel('Question #')
set(gca, 'XTick', nTick1)
set(gca, 'XTickLabel', num2str(nTick1'))
set(gca, 'YTick', 0.0:0.1:1.0)
title({['Results for gpt-4o-mini with 3 metrics over ' num2str(nNbQuestions) ' questions'],['Using ' strRAG ' on ' strDB ' (' strFile ')']}, 'Interpreter', 'Latex', 'FontSize', 18)
grid on
box on

subplot(6,1,2)
bar(fMetricsRag1)
hold on
plot([1 max(nTick2)], [fAvgMetricsRag1 fAvgMetricsRag1], 'r-')
ylabel(strRagFC)
xlabel('Question #')
set(gca, 'XTick', nTick2)
set(gca, 'XTickLabel', num2str(nTick2'))
set(gca, 'YTick', 0.0:0.1:1.0)
grid on
box on

subplot(6,1,3)
bar(fMetrics2)
hold on
plot([1 max(nTick1)], [fAvgMetrics2 fAvgMetrics2], 'r-')
ylabel(strAR)
xlabel('Question #')
set(gca, 'XTick', nTick1)
set(gca, 'XTickLabel', num2str(nTick1'))
set(gca, 'YTick', 0.0:0.1:1.0)
grid on
box on

subplot(6,1,4)
bar(fMetricsRag2)
hold on
plot([1 max(nTick2)], [fAvgMetricsRag2 fAvgMetricsRag2], 'r-')
ylabel(strRagAR)
xlabel('Question #')
set(gca, 'XTick', nTick2)
set(gca, 'XTickLabel', num2str(nTick2'))
set(gca, 'YTick', 0.0:0.1:1.0)
grid on
box on

subplot(6,1,5)
bar(fMetrics3)
hold on
plot([1 max(nTick1)], [fAvgMetrics3 fAvgMetrics3], 'r-')
ylabel(strSS)
xlabel('Question #')
set(gca, 'XTick', nTick1)
set(gca, 'XTickLabel', num2str(nTick1'))
set(gca, 'YTick', 0.0:0.1:1.0)
grid on
box on

subplot(6,1,6)
bar(fMetricsRag3)
hold on
plot([1 max(nTick2)], [fAvgMetricsRag3 fAvgMetricsRag3], 'r-')
ylabel(strRagSS)
xlabel('Question #')
set(gca, 'XTick', nTick2)
set(gca, 'XTickLabel', num2str(nTick2'))
set(gca, 'YTick', 0.0:0.1:1.0)
grid on
box on

saveas(gcf, ['Fig_Bar-w-wo-' strRAG '-' strDB], 'epsc')
saveas(gcf, ['Fig_Bar-w-wo-' strRAG '-' strDB], 'png')

%=======================================================================BHC

[nCounts1] = funcCountAll(fMetrics1, nNbQuestions);
[nCounts2] = funcCountAll(fMetrics2, nNbQuestions);
[nCounts3] = funcCountAll(fMetrics3, nNbQuestions);

[nCountsRag1] = funcCountAll(fMetricsRag1, nNbQuestions);
[nCountsRag2] = funcCountAll(fMetricsRag2, nNbQuestions);
[nCountsRag3] = funcCountAll(fMetricsRag3, nNbQuestions);

figure
set(gcf , 'Position', [1 49 1315 1315-49-1])
axis square
set(gca, 'XTick', 0.0:0.1:1.0)
set(gca, 'YTick', 0.0:0.1:1.0)
set(gcf, 'Color', 'White')
hold on

plot(nCounts1(:,1), nCounts1(:,2), 'ko-', 'MarkerFaceColor', 'k')
plot(nCountsRag1(:,1), nCountsRag1(:,2), 'kd-', 'MarkerFaceColor', 'k')

plot(nCounts2(:,1), nCounts2(:,2), 'ro-', 'MarkerFaceColor', 'r')
plot(nCountsRag2(:,1), nCountsRag2(:,2), 'rd-', 'MarkerFaceColor', 'r')

plot(nCounts3(:,1), nCounts3(:,2), 'bo-', 'MarkerFaceColor', 'b')
plot(nCountsRag3(:,1), nCountsRag3(:,2), 'bd-', 'MarkerFaceColor', 'b')

xlabel('Threshold', 'FontSize', 12)
ylabel(['Counting (Normalized over ' num2str(nNbQuestions) ' questions'], 'FontSize', 12)

title(['Thresholding to assess performance improvement over ' num2str(nNbQuestions) ' questions'], 'FontSize', 18)

lgd = legend(strFC, strRagFC, strAR, strRagAR, strSS, strRagSS);
lgd.Location = 'southwest';
lgd.FontSize = 12;

grid on
box on

saveas(gcf, ['Fig_Thresholding-' strRAG '-' strDB], 'epsc')
saveas(gcf, ['Fig_Thresholding-' strRAG '-' strDB], 'png')

%=======================================================================BHC

fPercent = 100*sum(abs(nCounts1(:,2)-nCountsRag1(:,2))) / length(nCountsRag1);
disp([strRagFC ' improved by ' num2str(fPercent, '%2.2f'), '%'])
fPercent = 100*sum(abs(nCounts2(:,2)-nCountsRag2(:,2))) / length(nCountsRag2);
disp([strRagAR ' improved by ' num2str(fPercent, '%2.2f'), '%'])
fPercent = 100*sum(abs(nCounts3(:,2)-nCountsRag3(:,2))) / length(nCountsRag3);
disp([strRagSS ' improved by ' num2str(fPercent, '%2.2f'), '%'])
disp(' ')

disp(' \hline')
disp(' \hline')
disp([' ' strRAG ' / ' strDB ' & Mean & Median & Std \\ '])
disp(' \hline')
disp(' \hline')
strMean   = num2str(mean(fMetrics1), '%2.3f');
strMedian = num2str(median(fMetrics1), '%2.3f');
strStd    = num2str(std(100*fMetrics1), '%2.3f');
disp([' ' strFC ' & ' strMean ' & ' strMedian ' & ' strStd ' \\ '])
strMean   = num2str(mean(fMetricsRag1), '%2.3f');
strMedian = num2str(median(fMetricsRag1), '%2.3f');
strStd    = num2str(std(fMetricsRag1), '%2.3f');
disp([' ' strFC ' RAG & ' strMean ' & ' strMedian ' & ' strStd ' \\ '])

strMeanShow = num2str(mean(fMetricsRag1)-mean(fMetrics1), '%2.3f');
if(mean(fMetricsRag1)-mean(fMetrics1) > 0)
    strMeanShow = ['\textbf{' strMeanShow '}'];
end
strMedianShow = num2str(median(fMetricsRag1)-median(fMetrics1), '%2.3f');
if(median(fMetricsRag1)-median(fMetrics1) > 0)
    strMedianShow = ['\textbf{' strMedianShow '}'];
end
disp([' RAG Improvement & ' strMeanShow ' & ' strMedianShow ' & \\ '])
disp(' \hline')

strMean   = num2str(mean(fMetrics2), '%2.3f');
strMedian = num2str(median(fMetrics2), '%2.3f');
strStd    = num2str(std(100*fMetrics2), '%2.3f');
disp([' ' strAR ' & ' strMean ' & ' strMedian ' & ' strStd ' \\ '])
strMean   = num2str(mean(fMetricsRag2), '%2.3f');
strMedian = num2str(median(fMetricsRag2), '%2.3f');
strStd    = num2str(std(fMetricsRag2), '%2.3f');
disp([' ' strAR ' RAG & ' strMean ' & ' strMedian ' & ' strStd ' \\ '])

strMeanShow = num2str(mean(fMetricsRag2)-mean(fMetrics2), '%2.3f');
if(mean(fMetricsRag2)-mean(fMetrics2) > 0)
    strMeanShow = ['\textbf{' strMeanShow '}'];
end
strMedianShow = num2str(median(fMetricsRag2)-median(fMetrics2), '%2.3f');
if(median(fMetricsRag2)-median(fMetrics2) > 0)
    strMedianShow = ['\textbf{' strMedianShow '}'];
end
disp([' RAG Improvement & ' strMeanShow ' & ' strMedianShow ' & ' strStd ' \\ '])
disp(' \hline')

strMean   = num2str(mean(fMetrics3), '%2.3f');
strMedian = num2str(median(fMetrics3), '%2.3f');
strStd    = num2str(std(100*fMetrics3), '%2.3f');
disp([' ' strSS ' & ' strMean ' & ' strMedian ' & ' strStd ' \\ '])
strMean   = num2str(mean(fMetricsRag3), '%2.3f');
strMedian = num2str(median(fMetricsRag3), '%2.3f');
strStd    = num2str(std(fMetricsRag3), '%2.3f');
disp([' ' strSS ' RAG & ' strMean ' & ' strMedian ' & ' strStd ' \\ '])

strMeanShow = num2str(mean(fMetricsRag3)-mean(fMetrics3), '%2.3f');
if(mean(fMetricsRag3)-mean(fMetrics3) > 0)
    strMeanShow = ['\textbf{' strMeanShow '}'];
end
strMedianShow = num2str(median(fMetricsRag3)-median(fMetrics3), '%2.3f');
if(median(fMetricsRag3)-median(fMetrics3) > 0)
    strMedianShow = ['\textbf{' strMedianShow '}'];
end
disp([' RAG Improvement & ' strMeanShow ' & ' strMedianShow ' & ' strStd ' \\ '])




