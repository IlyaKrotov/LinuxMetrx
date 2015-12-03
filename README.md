# LinuxMetrx
This script helps to read a lot of system information from ProcFS

Function readStatsTo() takes as an argument the name of the file, which will be recorded metrics, also returns some features of disk, and other features.

Example:

disk_stats, other_stats = readStatsTo(nameOfFile)
