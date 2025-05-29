#! /usr/bin/env python3

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
        
pio.kaleido.scope.chromium_args = (
        "--headless",
        "--no-sandbox",
        "--single-process",
        "--disable-gpu"
)  # tuple with chromium args


def preprocess_pin_data(title, prefix, ref_elipticity_neg=None, ref_elipticity_pos=None):

     """ Take the relevant sequence and get the appropriate files for plotting 
     pin, bend, bubble
     calculates elipticity - can normalise against a reference
     
     """

     df_pin = pd.read_csv(f"{prefix}/reWrLINE/combined.csv")
     df_bend = pd.read_csv(f"{prefix}/SerraLINE/bendangle.csv")
     df_bubble_pos = pd.read_csv(f"{prefix}/bubble/base1_counts_pos.csv")
     df_bubble_neg = pd.read_csv(f"{prefix}/bubble/base1_counts_neg.csv")
    
     neg_cols = [col for col in df_pin.columns if "t" in col and any(str(num) in col for num in range(26, 39) if num < 32)]
     pos_cols = [col for col in df_pin.columns if "t" in col and any(str(num) in col for num in range(26, 39) if num > 32)]

     df_pin["Mean_Negitive"] = df_pin[neg_cols].mean(axis=1)
     df_pin["Mean_Positive"] = df_pin[pos_cols].mean(axis=1)

     df_pin['Average circle_neg'] = float(df_pin['Mean_Negitive'].mean())
     df_pin['Average circle_pos'] = float(df_pin['Mean_Positive'].mean())
     
     df_pin['Diff squared_neg'] = (df_pin['Average circle_neg'] - df_pin['Mean_Negitive']) ** 2
     elipticity_neg = df_pin['Diff squared_neg'].sum()

     df_pin['Diff squared_pos'] = (df_pin['Average circle_pos'] - df_pin['Mean_Positive']) ** 2
     elipticity_pos = df_pin['Diff squared_pos'].sum()

     norm_elipticity_neg = elipticity_neg / ref_elipticity_neg if ref_elipticity_neg else elipticity_neg
     norm_elipticity_pos = elipticity_pos / ref_elipticity_pos if ref_elipticity_pos else elipticity_pos

     df_pin.insert(loc=0, column='bp', value=(np.arange(len(df_pin)) + 1))

     pos_cols_bend = []
     neg_cols_bend = []

     for n in range(26, 39): 
          for r in range(1, 4):
               col_name = f't{n}r{r}'
               
               if col_name in df_bend.columns:
                         if n > 32:
                              pos_cols_bend.append(col_name)
                         elif n < 32:
                              neg_cols_bend.append(col_name)

     df_bend['Mean_bend_neg'] = df_bend[neg_cols_bend].mean(axis=1)
     df_bend['Mean_bend_pos'] = df_bend[pos_cols_bend].mean(axis=1)

     df_bubble_pos['Occurrences_norm'] = df_bubble_pos['Occurrences'] / df_bubble_pos['Occurrences'].sum()
     df_bubble_neg['Occurrences_norm'] = df_bubble_neg['Occurrences'] / df_bubble_neg['Occurrences'].sum()

     df_pin['Mean_Negitive_norm'] = df_pin['Mean_Negitive'] / df_pin['Mean_Negitive'].sum()
     df_pin['Mean_Positive_norm'] = df_pin['Mean_Positive'] / df_pin['Mean_Positive'].sum()

     return{
           'df': title,
           'bp': df_pin['bp'].astype(int),
           'bubble_pos': df_bubble_pos['Occurrences_norm'],
           'bubble_neg': df_bubble_neg['Occurrences_norm'],
           'bend_pos': df_bend['Mean_bend_pos'],
           'bend_neg': df_bend['Mean_bend_neg'],
           'pin_pos': df_pin['Mean_Positive_norm'],
           'pin_neg': df_pin['Mean_Negitive_norm'],
           'elipticity_pos': norm_elipticity_pos,
           'elipticity_neg': norm_elipticity_neg,



     }

def make_fig(*args):

     """ Make a figure with plotly subplots - rows equal to number of args
     Two col: Plot positive on left, negitive on right - bubble, bend, pin
     Title is labelled with epliticity values
     Ensure control is inputed as "control" if want elipticity presented as 1
     
     """
      
     n = len(args)

     subplot_titles = []
     
     for arg in args:
           
               elip_pos = 1 if arg == control else f"{arg['elipticity_pos']:.2f}"  ##### Show 1 for control if relative pinning 
               elip_neg = 1 if arg == control else f"{arg['elipticity_neg']:.2f}"
           
               subplot_titles.extend([
                    f"{arg['df']}: σ > 0, p = {elip_pos}",   
                    f"{arg['df']}: σ < 0, p = {elip_neg}"
                    ])

     fig = make_subplots(rows=n, cols=2,  specs=[[{"secondary_y": True}, {"secondary_y": True}] for _ in range(n)],
                         horizontal_spacing=0, shared_yaxes=False, vertical_spacing=0.03, shared_xaxes=True, 
                         subplot_titles=subplot_titles, x_title='Position Along Minicircle')

     for r in range(1, n+1):
          fig.update_layout(margin=dict(l=2, b=200), width=2600, height=(800*n), paper_bgcolor="#fff", plot_bgcolor="#fff",
                **{
                      f'xaxis{(2*r)-1}': dict(
                         anchor=f'y{(4*r)-3}',                                  ##### X axis increases left to right and then down rows
                         domain=[0.24, 0.55],
                         tickvals=[1, 107, 339],
                         tickfont_size=40,
                         showline=True,
                         linewidth=3,
                         linecolor='black',
                         mirror=True,
                         color='black',
                    ),
                    f'xaxis{2*r}': dict(
                         anchor=f'y{(4*r)-1}',
                         domain=[0.58, 0.89],
                         tickvals=[1, 107, 339],
                         tickfont_size=40,
                         showline=True,
                         linewidth=3,
                         linecolor='black',
                         mirror=True,
                         color='black',
                    ),
                    f'yaxis{(4*r)-3}': dict(                                       ##### Y axis increases with two y axis per plot, then extra axis numbering starts again on first plot from second axis on last row
                         title_text='Bubble Density',
                         color='#B0C4DE',
                         nticks=5,
                         title_font=dict(size=50),
                         showline=True,
                         linewidth=3,
                         linecolor='black',
                         position=0.19,
                         mirror=True,
                         tickfont_size=40,
                    ),
                    f'yaxis{(4*r)-2}': dict(
                         title_text='Bend Angle',
                         title_font=dict(size=50),
                         side='left',
                         position=0.14,
                         anchor='free',
                         nticks=5,
                         color='grey',
                         tickfont_size=40,
                    ),
                    f'yaxis{(4*n)+(2*(r-1))+1}': dict(
                         anchor='free',
                         overlaying=f'y{(4*r)-3}',
                         position=0.08,
                         side='left',
                         title_text='Pinning Propensity',
                         title_font=dict(size=50),
                         title_standoff=40,
                         nticks=5,
                         color='black',
                         tickfont_size=40,
                    ),
                    f'yaxis{(4*r)-1}': dict(
                         color='#B0C4DE',
                         side='right',
                         nticks=5,
                         showline=True,
                         linewidth=3,
                         linecolor='black',
                         mirror=True,
                         position=0.89,
                         tickfont_size=40,
                    ),
                    f'yaxis{4*r}': dict(
                         side='right',
                         anchor='free',
                         position=0.95,
                         nticks=5,
                         color='grey',
                         tickfont_size=40,
                    ),
                    f'yaxis{(4*n)+(2*(r-1))+2}': dict(
                         anchor='free',
                         overlaying=f'y{(4*r)-1}',
                         position=1,
                         side='right',
                         nticks=5,
                         color='black',
                         tickfont_size=40,
                    ),
               }
          )

     for idx, arg in enumerate(args):

          r = idx + 1

          fig.add_trace(go.Scatter(
               x=arg['bp'],
               y=arg['bubble_pos'],
               name='Bubble',
               xaxis=f'x{(2*r)-1}',
               yaxis=f'y{(4*r)-3}',
               fill='tozeroy',
               fillcolor = '#B0C4DE',
               showlegend=False,                                    
               line=dict(color='#B0C4DE', width=4)), secondary_y=False, row=r, col=1)

          fig.add_trace(go.Scatter(
               y=arg['bend_pos'],
               x=arg['bp'],
               name='Bend',
               xaxis=f'x{(2*r)-1}',
               yaxis=f'y{(4*r)-2}',
               showlegend=False,
               line=dict(color='grey', width=5)), secondary_y=True, row=r, col=1)

          fig.add_scatter(
               y=arg['pin_pos'],
               x=arg['bp'],
               name='Pin',
               yaxis=f'y{(4*n)+(2*(r-1))+1}',
               xaxis=f'x{(2*r)-1}',
               showlegend=False,
               line=dict(color='black', width=5))

          fig.add_trace(go.Scatter(
               x=arg['bp'],
               y=arg['bubble_neg'],
               name='Bubble',
               xaxis=f'x{(2*r)}',
               yaxis=f'y{(4*r)-1}',
               fill='tozeroy',
               fillcolor = '#B0C4DE',
               showlegend=False,
               line=dict(color='#B0C4DE', width=4)), secondary_y=False, row=r, col=2)

          fig.add_trace(go.Scatter(
               y=arg['bend_neg'],
               x=arg['bp'],
               name='Bend',
               xaxis=f'x{(2*r)}',
               yaxis=f'y{(4*r)}',
               showlegend=False,
               line=dict(color='grey', width=5)), secondary_y=True, row=r, col=2)

          fig.add_scatter(
               y=arg['pin_neg'],
               x=arg['bp'],
               name='Pin',
               yaxis=f'y{(4*n)+(2*(r-1))+2}',
               xaxis=f'x{(2*r)}',
               line=dict(color='black', width=5),
               showlegend=False,)


          fig.layout.annotations[2*idx].update(x=0.405, font=dict(color='black', size=50))
          fig.layout.annotations[2*idx+1].update(x=0.74, font=dict(color='black', size=50))
          fig.layout.annotations[-1].update(x=0.575, y=-0.02, font=dict(color='black', size=50))

     return fig

### No pinning control
control = preprocess_pin_data("Control339", "/mnt/k/Work/Controls/np339_implicit_v2")

ref_neg = control['elipticity_neg']
ref_pos = control['elipticity_pos']

### Compared to strong and mid pinning sequence
two_gg = preprocess_pin_data("2bp (GG)", "/mnt/h/Work/np2bpGG/", ref_neg, ref_pos)
two_tt = preprocess_pin_data("2bp (TT)", "/mnt/h/Work/np2bpTT/", ref_neg, ref_pos)
three = preprocess_pin_data("3bp (CTG)", "/mnt/h/Work/np3bp/", ref_neg, ref_pos)

fig = make_fig(control,two_gg, two_tt, three )

fig.write_image("np_multibp.pdf")
fig.write_image("np_multibp.pdf")     #### Write twice because plotly displays a loading bar on first pdf export

