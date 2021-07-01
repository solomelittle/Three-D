library("dataDownloader")
source("R/Load packages.R")


#download data from OSF and read it
get_file(node = "pk4bg",
         file = "Three-D_c-flux_2020.csv",
         path = "data/C-Flux/summer_2020",
         remote_path = "C-Flux")

lrc_flux <- read_csv("data/C-Flux/summer_2020/Three-D_c-flux_2020.csv") %>% 
  filter(campaign == "LRC")

#graph each light response curves
ggplot(lrc_flux, aes(x = PARavg, y = flux, color = turf_ID)) +
  geom_point(size = 0.1) +
  # geom_smooth(method = "lm", se = FALSE)
  geom_smooth(method = "lm", formula = y ~ poly(x, 2), se = FALSE)

#grouping per treatment instead of turfs
#need to add a treatment column
lrc_flux <- lrc_flux %>% 
  mutate(
    treatment = case_when(
      str_detect(turf_ID, "W") ~ "W",
      TRUE ~ "A"
    )
  )
#plotting
ggplot(lrc_flux, aes(x = PARavg, y = flux, color = treatment)) +
  geom_point(size = 0.1) +
  # geom_smooth(method = "lm", se = FALSE)
  geom_smooth(method = "lm", formula = y ~ poly(x, 2), se = FALSE)

