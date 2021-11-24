library("dataDownloader")
library(broom)
library(fs)
source("R/Load packages.R")
# source("https://raw.githubusercontent.com/jogaudard/common/master/fun-fluxes.R")

#function to match the fluxes with the record file
match.flux <- function(raw_flux, field_record){
  co2conc <- full_join(raw_flux, field_record, by = c("datetime" = "start"), keep = TRUE) %>% #joining both dataset in one
    fill(PAR, temp_air, temp_soil, turfID, type, campaign, start, date, end, start_window, end_window) %>% #filling all rows (except Remarks) with data from above
    group_by(date, turfID, type) %>% #this part is to fill Remarks while keeping the NA (some fluxes have no remark)
    fill(comments) %>% 
    ungroup() %>% 
    mutate(fluxID = group_indices(., date, turfID, type)) %>% #assigning a unique ID to each flux, useful for plotting uzw
    filter(
      datetime <= end
      & datetime >= start) #%>% #cropping the part of the flux that is after the End and before the Start
  
  
  return(co2conc)
}


measurement <- 210 #the length of the measurement taken on the field in seconds
startcrop <- 10 #how much to crop at the beginning of the measurement in seconds
endcrop <- 40 #how much to crop at the end of the measurement in seconds

#download and unzip files from OSF
get_file(node = "pk4bg",
         file = "Three-D_cflux_2021.zip",
         path = "data/c-flux/summer_2021",
         remote_path = "RawData/C-Flux")

get_file(node = "pk4bg",
         file = "Three-D_field-record_2021.csv",
         path = "data/c-flux/summer_2021",
         remote_path = "RawData/C-Flux")

get_file(node = "pk4bg",
         file = "Three-D_cutting_2021.csv",
         path = "data/c-flux/summer_2021",
         remote_path = "RawData/C-Flux")

# Unzip files
zipFile <- "data/c-flux/summer_2021/Three-D_cflux_2021.zip"
if(file.exists(zipFile)){
  outDir <- "data/c-flux/summer_2021"
  unzip(zipFile, exdir = outDir)
}

#importing fluxes data
location <- "data/c-flux/summer_2021" #location of datafiles

fluxes <-
  dir_ls(location, regexp = "*CO2*") %>% 
  map_dfr(read_csv,  na = c("#N/A", "Over")) %>% 
  rename( #rename the column to get something more practical without space
    CO2 = "CO2 (ppm)",
    temp_air = "Temp_air ('C)",
    temp_soil = "Temp_soil ('C)",
    PAR = "PAR (umolsm2)",
    datetime = "Date/Time"
  ) %>%  
  mutate(
    datetime = dmy_hms(datetime)
  ) %>%
  select(datetime,CO2, PAR, temp_air, temp_soil)


#import the record file from the field

record <- read_csv("data/c-flux/summer_2021/Three-D_field-record_2021.csv", na = c(""), col_types = "cctDfc") %>% 
  drop_na(starting_time) %>% #delete row without starting time (meaning no measurement was done)
  mutate(
    start = ymd_hms(paste(date, starting_time)), #converting the date as posixct, pasting date and starting time together
    end = start + measurement, #creating column End
    start_window = start + startcrop, #cropping the start
    end_window = end - endcrop #cropping the end of the measurement
  ) 

#matching the CO2 concentration data with the turfs using the field record
co2_fluxes <- match.flux(fluxes,record)

#filtering the soil respiration data
co2_fluxes_soil <- co2_fluxes %>% 
  filter(
    type == "SoilR"
  )

