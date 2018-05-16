library(dplyr)
library(ggplot2)
library(lubridate)
library(jsonlite)
library(tidyr)
library(plotly)

extractVar <- function(DF, var){
    datur <- c()
    for(x in DF$data){
        if(var %in% names(x)){
            datur <- c(datur, x[[var]])
        }
        else{
            datur <- c(datur, NA)
        }
    }
    datur
}

lesvosDF <- fromJSON(txt="../../data/lesvos.json") %>%
    select(-targeting_spec, -error) %>%
    mutate(dau=extractVar(., "estimate_dau")) %>%
    mutate(mau=extractVar(., "estimate_mau")) %>%
    select(-data) %>%
    mutate(time2=as_datetime(time)) %>%
    gather(key="Estimator", value="Estimate", dau:mau)

shinyServer(function(input,output){
    
    output$time <- renderPlotly({
        DF <- lesvosDF %>%
            filter(expat==input$expat & 
                   recent==input$recent & 
                   arabicOnly==input$arabic) %>%
            filter(Estimator %in% input$estimates)
        
        p <- DF %>%
            ggplot(aes(x=time2, y=Estimate, color=Estimator,
                       text=paste0("Time: ", DF$time, 
                                   "<br>Estimate: ", DF$Estimate))) +
            labs(x="Time", y="Population Estimate") +
            geom_point() + theme_classic()
        ggplotly(p, tooltip="text")
    })
})