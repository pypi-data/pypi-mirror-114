import alchemlyb.parsing.amber
import alchemtest.amber
dataset = alchemtest.amber.load_bace_example()
df = alchemlyb.parsing.amber.extract_u_nk(dataset['data']['complex']['vdw'][0], T=300)
df
df.names
df.columns
u_nk = pd.concat([alchemlyb.parsing.amber.extract_u_nk(fn, T=300) for fn in dataset['data']['complex']['vdw']])
import pandas as pd
u_nk = pd.concat([alchemlyb.parsing.amber.extract_u_nk(fn, T=300) for fn in dataset['data']['complex']['vdw']])
u_nk.columns
u_nk.shape
u_nk[:3]
df.shape
import alchemlyb.parsing.gmx
import alchemtest.gmx
gmx_u_nk = pd.concat([alchemlyb.parsing.gmx.extract_u_nk(fn, T=300) for fn in alchemtest.gmx.load_benzene['data']['VDW']])
gmx_u_nk = pd.concat([alchemlyb.parsing.gmx.extract_u_nk(fn, T=300) for fn in alchemtest.gmx.load_benzene()['data']['VDW']])
gmx_u_nk.shape
gmx_u_nk.columns
gmx_u_nk.columns[0]
gmx_u_nk.columns[1]
type(gmx_u_nk.columns[1])
type(u_nk.columns[1])
u_nk.describe()
u_nk.columns
%hist -f tst.py
