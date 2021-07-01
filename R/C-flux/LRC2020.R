library("dataDownloader")
source("R/Load packages.R")


#download data from OSF and read it
get_file(node = "pk4bg",
         file = "Three-D_c-flux_2020.csv",
         path = "data/C-Flux/summer_2020",
         remote_path = "C-Flux")

lrc_flux <- read_csv("data/C-Flux/summer_2020/Three-D_c-flux_2020.csv") %>% 
  filter(campaign == "LRC")
