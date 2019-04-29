#!/usr/bin/env Rscript

users = commandArgs(trailingOnly=TRUE)

if (length(args) == 0) {
  stop("At least one user should be provided as an argument.", call.=FALSE)
} else if (length(args) > 15) {
  stop("Twitter API can't handle more than 15 users.")
}
    
library(tweetscores)

estimates <- list()

print(users)

for (user in users){
    cat(paste("Fetching the friend list of", user))
    cat("\n")
    friends <- getFriends(screen_name=user, oauth="~/retweeters")

    cat(paste("Measuring ideology of", user))
    cat("\n")
    results <- estimateIdeology(user, friends)

    estimates[[user]] <- results

    summary(results)
}

# How to return...?

