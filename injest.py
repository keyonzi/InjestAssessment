import paramiko
import pandas as pd
import numpy as np

# making sure we can see the whole table
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 50)



SFTP_HOST="s-8eb19e5d5f41419fa.server.transfer.us-east-1.amazonaws.com"

SFTP_USER="keyon_hedayati"

SFTP_PASS="hTFulGIsiSfe"

SFTP_PORT=22

## COMMENTING OUT BECAUSE DON'T NEED CONNECTION ANYMORE ####
# open connection and get the file
transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
transport.connect(username = SFTP_USER, password = SFTP_PASS)
sftp = paramiko.SFTPClient.from_transport(transport)

# download copy of file
sftp.get('sample_orders.csv', 'injest_sample_orders.csv')


df = pd.read_csv('injest_sample_orders.csv')

# get non-voided rows
df = df.loc[df['order_is_void'] != True]

# try to convert to currency
df['order_total'] = df['order_subtotal'].replace('[\$,]', '', regex=True).astype(float)

# test if duplicate ids
df = df.drop_duplicates(subset=['order_id'])

# group by then sum
df_grouped = df.groupby(['restaurant_id'])['order_total'].agg('sum')

print(df_grouped)

