#!/usr/bin/env Rscript

users = commandArgs(trailingOnly=TRUE)

if (length(args) == 0) {
  stop("At least one user should be provided as an argument.", call.=FALSE)
} else if (length(args) > 15) {
  stop("Twitter API can't handle more than 15 users.")
}
    
library(tweetscores)
source("eval_ideo_settings.R")

estimates <- list()

print(users)

for (user in users){
    cat(paste("Fetching the friend list of", user))
    cat("\n")
    
    tryCatch(
             {friends <- getFriends(screen_name=user, oauth=my_oauth)

              cat(paste("Measuring ideology of", user))
              cat("\n")
    
              results <- estimateIdeology(user, friends)

              #estimates[[user]] <- results
              
              write.table(data.frame(user, summary(results)[,"mean"][2]),
                          file = "retweeter_ideo.csv", sep = ",",
                          append = TRUE, quote = FALSE, 
                          col.names = FALSE, row.names = FALSE) 

              summary(results)
             },
             error = function(cond){
                 message(cond)
             })
}

# How to return...?

