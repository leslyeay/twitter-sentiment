postscript("graphs.eps")

results <- read.csv("/export/scratch/masli/courses/fall09/csci8980/DataAnalysis/twitter-sentiment/trunk/results/combined-results.txt", sep = "\t")

plot(results$Followers, results$Happy)
plot(results$Friends, results$Happy)
plot(results$Friends, results$Followers)

hist(results$Happy)
hist(results$Sad)

