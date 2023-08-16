library(shiny)
library(magrittr)

ui <- shinyServer(fluidPage(
  plotOutput("first_column")
))