options(repos = c(CRAN = "https://cran.r-project.org"))
if (!requireNamespace("devtools", quietly = TRUE)) {
  install.packages("devtools")
}
print("Starting Code...")
file_path <-"input_data.txt"
file_content <- readLines(file_path)
cred_path <-"credentials.txt"
cred_content <- readLines(cred_path)
Sys.sleep(1)
if (!require(GISAIDR)) {
  message("GISAIDR package not found. Installing from GitHub...")
  devtools::install_github("Wytamma/GISAIDR")
  library(GISAIDR)
} else {
  library(GISAIDR)
}

username <- cred_content[1]
password <- cred_content[2]
database <- cred_content[3]
credentials <- login(username, password, database)

start_date <- file_content[2]
end_date <- file_content[3]
location <- file_content[4]
mutation <- file_content[5]

df <- suppressMessages(
  query(
    credentials = credentials,
    location = location,
    from_subm = start_date,
    to_subm = end_date,
    aa_substitution = mutation,
    fast = TRUE
  )
)

if (nrow(df) > -1) {
    total_viruses <- nrow(df)
    print(paste(total_viruses, "viruses found"))

    summary_table <- data.frame(
      Total_Viruses_Found = total_viruses
    )
    
    print(summary_table)
    
    write.table(summary_table, "GISAID_search_summary.csv", sep = ",", col.names = FALSE, row.names = FALSE, quote = TRUE)
    print("File Written Successfully")
}else {
  print("No viruses found for the specified query parameters.")
}
