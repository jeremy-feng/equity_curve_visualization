from plot_equity_curve import *

return_df = pd.read_csv('returns.csv', index_col=0)
draw_equity_curve(return_df, returns_data=True,
                  output_path='Equity Curve', title='Equity Curve')
