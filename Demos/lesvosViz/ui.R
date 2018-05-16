rm(list=ls())

library(shiny)
library(shinydashboard)
library(plotly)

header <- dashboardHeader(
    title = 'Facebook Targeted Ads Numbers'
)

body <- dashboardBody(
    fluidRow(
        column(width=12,
               tabBox(id='tabvals', width=NULL,
                      tabPanel('Time Series', plotlyOutput('time'), value=1)
               )
        )
    ),
    status="danger",
    tags$head(tags$style(HTML('
                              /* logo */
                              .skin-blue .main-header .logo {
                              background-color: #070B19;
                              }
                              
                              /* logo when hovered */
                              .skin-blue .main-header .logo:hover {
                              background-color: #070B19;
                              }
                              
                              /* navbar (rest of the header) */
                              .skin-blue .main-header .navbar {
                              background-color: #070B19;
                              }
                              
                              /* main sidebar */
                              .skin-blue .main-sidebar {
                              background-color: #070B19;
                              }
                              
                              /* active selected tab in the sidebarmenu */
                              .skin-blue .main-sidebar .sidebar .sidebar-menu .active a{
                              background-color: #ff0000;
                              }
                              
                              /* other links in the sidebarmenu */
                              .skin-blue .main-sidebar .sidebar .sidebar-menu a{
                              background-color: #00ff00;
                              color: #000000;
                              }
                              
                              /* other links in the sidebarmenu when hovered */
                              .skin-blue .main-sidebar .sidebar .sidebar-menu a:hover{
                              background-color: #DF0101;
                              }
                              /* toggle button when hovered  */
                              .skin-blue .main-header .navbar .sidebar-toggle:hover{
                              background-color: #DF0101;
                              }
                              /* Highlighted Tab Color*/
                              .nav-tabs-custom .nav-tabs li.active {
                              border-top-color: #DF0101;
                              }')))
)




sidebar <- dashboardSidebar(
    conditionalPanel(condition="input.tabvals==1",
    selectInput('expat', 'Expat', c(TRUE, FALSE)),
    selectInput('recent', 'Recent', c(TRUE, FALSE)),
    selectInput('arabic', 'Arabic', c(TRUE, FALSE)),
    selectInput('estimates', 'Estimates', c("mau", "dau"), selected=c("dau"),
                multiple=TRUE)
    )
)

dashboardPage(
    header,
    sidebar,
    body
)