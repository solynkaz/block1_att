import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import ttest_ind, chi2_contingency, mannwhitneyu
import io


def run_numeric(column, data, color):
    data[column] = pd.to_numeric(data[column], errors='coerce')
    data[column] = data[column].dropna()

    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], color=color, kde=True)
    plt.title(f"Гистограмма с KDE для колонки: {column}")
    plt.xlabel(column)
    plt.ylabel("Частота")
    st.pyplot(plt)


def run_categorial(column, data, color):
    category_counts = data[column].value_counts()

    # Построение пай-чарта
    plt.figure(figsize=(8, 8))
    plt.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%", startangle=140)
    plt.title(f"Pie-chart: {column}")
    st.pyplot(plt)


def run(column, data, color):
    numeric = pd.to_numeric(data[column], errors='coerce')
    if (numeric.count() == 0 or data[column].nunique() < 10):
        st.write(f"Колонка: {column} CATEGORIAL")
        run_categorial(column, data, color)
    else:
        st.write(f"Колонка: {column} NUMERIC")
        run_numeric(column, data, color)


def show_info(data):
    buffer = io.StringIO()
    data.info(buf=buffer)
    info_string = buffer.getvalue()

    # Вывод информации о датафрейме как строки
    st.write("Информация о датафрейме:")
    st.text(info_string)
    # Вывод первых нескольких строк
    st.write("Первые строки файла:")

    st.write(data.head())


def main():
    # Заголовок приложения
    st.title("Анализ распределения данных")

    # Загрузка файла
    uploaded_file = st.file_uploader("Выберите файл (CSV)", type=["csv"])

    # Обработка файла
    if uploaded_file is not None:
        # Чтение данных из CSV файла
        data = pd.read_csv(uploaded_file)
        if st.button("Показать информацию о датафрейме"):
            show_info(data)

        st.markdown("<h2>Выберите столбцы для анализа распределения:</h2>", unsafe_allow_html=True)
        selected_columns = st.multiselect("Выберите столбцы для анализа распределения:", data.columns,
                                          label_visibility='hidden')
        for column in selected_columns:
            run(column, data, 'red')

        st.markdown("<h2 align=\"center\">Статистический анализ</h2>", unsafe_allow_html=True)
        hypotheses = ['T Test', 'Mann-whitney U-test', 'Chi-square']

        hypothesis = st.selectbox("Выберите гипотезу", hypotheses)

        # Выбор гипотезы
        if hypothesis == 'T Test':
            st.markdown(f"<h3 align=\"center\">{hypothesis} гипотеза</h3>", unsafe_allow_html=True)
            t_test(data)

        if hypothesis == 'Mann-whitney U-test':
            st.markdown(f"<h3 align=\"center\">{hypothesis} гипотеза</h3>", unsafe_allow_html=True)
            u_test(data)

        if hypothesis == 'Chi-square':
            st.markdown(f"<h3 align=\"center\">{hypothesis} гипотеза</h3>", unsafe_allow_html=True)
            chi_square(data)


def t_test(data):
    compare = st.selectbox("Выберите 1 столбец для анализа:", data.columns)

    fileds_in_compare = st.multiselect("Выберите значение 2 по которым будете сравнивать\n:" +
                                       f"(здесь перечислины все уникальные значения {compare})",
                                       data[compare].unique())

    if len(fileds_in_compare) == 2:
        criteries = st.multiselect("Выберите критерий сравнения", data.columns.drop(compare))
        for critery in criteries:
            res = ttest_ind(data[data[compare] == fileds_in_compare[0]][critery],
                            data[data[compare] == fileds_in_compare[1]][critery],
                            equal_var=False)
            st.write(f'p-value для {critery}: {res.pvalue / 2:.4f}')


def u_test(data):
    compare = st.selectbox("Выберите 1 столбец для анализа:", data.columns)

    fileds_in_compare = st.multiselect("Выберите значение 2 по которым будете сравнивать\n:" +
                                       f"(здесь перечислины все уникальные значения {compare})",
                                       data[compare].unique())

    if len(fileds_in_compare) == 2:
        criteries = st.multiselect("Выберите критерий сравнения", data.columns.drop(compare))
        for critery in criteries:
            res = mannwhitneyu(data[data[compare] == fileds_in_compare[0]][critery],
                               data[data[compare] == fileds_in_compare[1]][critery])
            st.write(f'p-value для {critery}: {res.pvalue / 2:.4f}')


def chi_square(data):
    columns = st.selectbox("Выберите columns столбец для анализа:", data.columns)
    values = st.selectbox("Выберите values столбец для анализа:", data.columns)
    cross_tab = pd.crosstab(data[columns], data[values], margins=True)
    cross_tab = cross_tab.drop(columns=["All"], index=["All"])
    st.write("cross_tab")
    st.write(cross_tab)

    chisq, pvalue = chi2_contingency(cross_tab)
    st.write(f'Observed chi2: {chisq:.4f}')
    st.write(f'p-value: {pvalue:.4f}')


main()