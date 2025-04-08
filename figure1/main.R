library(tidyverse)
options(echo=TRUE)
args <- commandArgs(trailingOnly = TRUE)

blast = read_tsv(args[1]) %>%
  filter(numSeqs > 50) %>%
  filter(numConserved <= 50) %>%
  filter(numConserved > 0)
complete = read_tsv(args[2]) %>%
  filter(numSeqs > 50) %>%
  filter(numConserved <= 50) %>%
  filter(numConserved > 0)
single = read_tsv(args[3]) %>%
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
  facet_wrap(~Group, nrow = 1) +
  ggtitle("Conserved Residues by Clustering Method") +
  labs(x = "Number of Conserved Residues", y = "Number of Clusters") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5))

ggsave("figure1.png")