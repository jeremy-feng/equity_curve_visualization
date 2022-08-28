from plot_equity_curve import *
import streamlit as st
import streamlit.components.v1 as components

st.markdown("""
功能：上传资产价格或收益率，生成可交互的回测曲线。
"""
            )

uploaded_file = st.file_uploader("上传文件（支持csv和xlsx格式）", type=["csv", "xlsx"])
if uploaded_file is not None:
    file_name = uploaded_file.name
    # 求文件的后缀名
    file_ext = file_name.split('.')[-1]
    if file_ext == 'csv':
        data = pd.read_csv(uploaded_file, index_col=0)
    elif file_ext == 'xlsx':
        data = pd.read_excel(uploaded_file, index_col=0)
    else:
        st.error("不支持的文件格式！")
        data = None
    st.write("上传的文件")
else:
    st.write("示例文件（组合和基准指数的收益率）")
    data = pd.read_csv('data/returns.csv', index_col=0)
st.dataframe(data)

data_type = st.radio(
    "数据类型",
    ('收益率', '价格'))

if data_type == '收益率':
    returns_data = True
else:
    returns_data = False

# 绘制回测曲线
html_string = draw_equity_curve(data, returns_data=returns_data,
                                output_path='Equity Curve', title='Equity Curve')

components.html(html_string, height=400)
