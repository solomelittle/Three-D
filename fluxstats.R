library("dataDownloader")
library(broom)
library(fs)
source("R/Load packages.R")


fluxes2021 <- read_csv("data/c-flux/summer_2021/Three-D_c-flux_2021.csv", na = c(""), col_select = c("turfID","temp_soilavg", "flux"), col_types = "cicccnnncici")
#fluxes2021 <- as.numeric(fluxes2021[,3])
cor(fluxes[,2], fluxes2021, method = c("pearson"))