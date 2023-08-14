import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, chi2_contingency

st.set_option('deprecation.showPyplotGlobalUse', False)


def load_data(file):
    try:
        data = pd.read_csv(file)
        return data
    except Exception as e:
        st.error(f"Ошибка при загрузке файла: {e}")
        return None


def visualize_distribution(data, column):
    st.subheader(f"Распределение переменной '{column}'")
    plt.figure(figsize=(10, 6))

    if data[column].dtype == "object":
        data[column].value_counts().head(12).plot(kind="pie", autopct="%1.1f%%")
        st.pyplot()
    else:
        sns.histplot(data=data, x=column, kde=True)
        st.pyplot()



def hypothesis_test(data, column1, column2):
    st.subheader("Проверка гипотезы")

    if data[column1].dtype != data[column2].dtype:
        st.error("Выбранные переменные имеют разные типы данных")
    else:
        if data[column1].dtype == "object":
            contingency_table = pd.crosstab(data[column1], data[column2])
            chi2, p, _, _ = chi2_contingency(contingency_table)
            st.write(f"Значение статистики Хи-квадрат: {chi2:.2f}")
            st.write(f"p-value: {p:.4f}")
        else:
            group1 = data[data[column2] == data[column2].unique()[0]][column1]
            group2 = data[data[column2] == data[column2].unique()[1]][column1]
            t_statistic, p_value = ttest_ind(group1, group2)
            st.write(f"Значение t-статистики: {t_statistic:.2f}")
            st.write(f"p-value: {p_value:.4f}")


def main():
    st.title("Анализ данных")

    uploaded_file = st.file_uploader("Загрузите CSV файл", type=["csv"])
    if uploaded_file is not None:
        data = load_data(uploaded_file)

        if data is not None:
            columns = data.columns.tolist()
            column1 = st.selectbox("Выберите первую переменную", columns)
            column2 = st.selectbox("Выберите вторую переменную", columns)

            visualize_distribution(data, column1)
            visualize_distribution(data, column2)

            test_options = ["t-тест", "Хи-квадрат тест"]
            selected_test = st.selectbox("Выберите проверочный алгоритм", test_options)

            if st.button("Выполнить проверку"):
                if data[column1].dtype == data[column2].dtype:
                    if selected_test == "t-тест":
                        hypothesis_test(data, column1, column2)
                    elif selected_test == "Хи-квадрат тест":
                        hypothesis_test(data, column1, column2)
                else:
                    st.warning('У переменных разный тип данных')


main()
