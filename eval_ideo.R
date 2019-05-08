#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly=TRUE)

users <- args[1]
api_key <- args[2]

if (length(args) < 2) {
  stop("At least one user and API key identifer should be provided as an argument.", call.=FALSE)
} else if (length(args) > 15) {
  stop("Twitter API can't handle more than 15 users.")
}
    
library(tweetscores)
source("eval_ideo_settings.R")

# my_oauth <- get()

estimates <- list()

my_oauth <- get(api_key)
limit <- tweetscores:::getLimitFriends(my_oauth = tweetscores:::getOAuth(my_oauth, verbose = verbose))

if (limit < 2) {
    print(paste(api_key, " is going to sleep for 16 mins."))
    Sys.sleep(60 * 16)
}

#print(users)

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
                 sys.sleep(60 * 15)
             })
}


