import streamlit as st
import pandas as pd

st.set_page_config(page_title="测试集review工具", layout="wide")

st.title("🖼️ 测试集review工具")

# 1. 文件上传
uploaded_file = st.sidebar.file_uploader("上传 Excel 文件", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # --- 侧边栏筛选 ---
    st.sidebar.header("筛选与配置")
    all_labels = df['label'].unique().tolist()
    selected_labels = st.sidebar.multiselect("选择 Label", all_labels, default=all_labels)

    page_size = st.sidebar.slider("每页展示数量", 5, 50, 10)

    # 筛选数据
    filtered_df = df[df['label'].isin(selected_labels)]
    total_rows = len(filtered_df)
    total_pages = (total_rows // page_size) + (1 if total_rows % page_size > 0 else 0)

    if total_pages > 0:
        current_page = st.sidebar.number_input("页码", min_value=1, max_value=total_pages, value=1)

        # 计算当前页数据
        start_idx = (current_page - 1) * page_size
        end_idx = min(start_idx + page_size, total_rows)
        display_df = filtered_df.iloc[start_idx:end_idx]

        st.write(f"正在查看第 {current_page} 页，共 {total_rows} 条结果")
        st.divider()

        # --- 循环渲染大图卡片 ---
        for index, row in display_df.iterrows():
            # 创建两列，左侧放图片，右侧放文字信息
            col1, col2 = st.columns([1, 2])  # 比例可以根据需要调整

            with col1:
                # 这里的 use_column_width=True 会让图片填满列宽
                st.image(row['url'], caption=f"SKC: {row['skc']}", use_container_width=True)

            with col2:
                st.subheader(f"数据索引: #{index}")
                st.write(f"**SKC:** `{row['skc']}`")

                # 根据 label 显示不同颜色的状态
                label_color = "green" if row['label'] == 'positive' else "red"
                st.markdown(f"**Label:** :{label_color}[{row['label']}]")

                st.write(f"**图片地址:** [点击查看原图]({row['url']})")

                # 加一个分割线，区分下一条
                st.divider()
    else:
        st.warning("无匹配数据")
else:
    st.info("💡 请先在左侧上传 Excel 文件。")
