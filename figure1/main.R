library(tidyverse)

#These files are the zipped files found in this same directory, just unzip them and run the code
blast = read_tsv('proportionConservedBlastOutput.tsv') %>%
  filter(numSeqs > 50) %>%
  filter(numConserved <= 50) %>%
  filter(numConserved > 0)
complete = read_tsv('proportionConservedCompleteLinkage.tsv') %>%
  filter(numSeqs > 50) %>%
  filter(numConserved <= 50) %>%
  filter(numConserved > 0)
single = read_tsv('proportionConservedSingleLinkage.tsv') %>%
  filter(numSeqs > 50) %>%
  filter(numConserved <= 50) %>%
  filter(numConserved > 0)


numConserved1 = pull(blast, numConserved)
numConserved2 = pull(complete, numConserved)
numConserved3 = pull(single, numConserved)

df1 = data.frame(values = numConserved1)
df2 = data.frame(values = numConserved2)
df3 = data.frame(values = numConserved3)

combined = bind_rows(
  mutate(df1, Group = "Blast Clusters"),
  mutate(df2, Group = "Complete Linkage"),
  mutate(df3, Group = "Single Linkage")
)

ggplot(data = combined, aes(x = values)) +#, fill = Group)) + 
  geom_histogram(binwidth = 1) + 
  facet_wrap(~Group, nrow = 1, scale = "free_y") +
  ggtitle("Conserved Residues by Clustering Method") +
  labs(x = "Number of Conserved Residues", y = "Number of Clusters") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5))
