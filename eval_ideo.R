#!/usr/bin/env Rscript

#args = commandArgs(trailingOnly=TRUE)

#if (length(args) != 1) {
#  stop("One argument must be supplied (input file).n", call.=FALSE)
#} 

library(tweetscores)

user <- "p_barbera"
friends <- getFriends(screen_name=user, oauth="~/retweeters")

results <- estimateIdeology(user, friends)

summary(results)

