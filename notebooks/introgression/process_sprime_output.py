import numpy as np
import pandas as pd
import sys

in_file = sys.argv[1]
out_file = sys.argv[2]

# read in the data - the SPrime output
df = pd.read_csv(in_file, delimiter="\t")

# drop columns that are not needed
df2 = df.drop(['ID', 'REF', 'ALT', 'ALLELE'], axis=1)

# add columns START and END with the highest ans lowest position of each chromosome, segment and score
df2['START'] = df2.groupby(['CHROM', 'SCORE', 'SEGMENT'])['POS'].transform(min)
df2['END'] = df2.groupby(['CHROM', 'SCORE', 'SEGMENT'])['POS'].transform(max)

# group by chromosome, segment and score - drop the column position
df3 = df2.loc[df2.groupby(["CHROM", "SCORE", "SEGMENT"])["POS"].idxmax()]
df4 = df3.drop(['POS'], axis=1)

# get the right order (for the bed file)
df_final = df4[['CHROM','START','END','SEGMENT','SCORE']].sort_values(by=['START', 'SEGMENT'])

np.savetxt(out_file, df_final.values, fmt='%s', delimiter='\t')
