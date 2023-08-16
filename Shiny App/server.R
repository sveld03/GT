library(shiny)
library(magrittr)

library(shiny)
library(magrittr)

ui <- shinyServer(fluidPage(
  plotOutput("first_column")
))

full_data <<- read.csv("test20.csv", header = TRUE)

x <- 1

server <- shinyServer(function(input, output, session){
  # Function to get new observations
  get_new_data <- function(){
    data <- full_data[x:(x+4),] %>% rbind %>% data.frame
    return(data)
  }

  # Initialize my_data
  my_data <<- get_new_data()

  # Function to update my_data
  update_data <- function(){
    my_data <<- rbind(my_data, get_new_data())
    x <<- x + 5
  }

  # Plot the 30 most recent values
  output$first_column <- renderPlot({
    print("Render")
    invalidateLater(1000, session)
    update_data()
    print(my_data)
    plot(B1 ~ 1, data=my_data, ylim=c(-3, 3), las=1, type="l")
  })
})

# shinyApp(ui=ui, server=server)