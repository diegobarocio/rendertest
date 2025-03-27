import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables de estado
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0
    status = st.empty()  # Texto animado
    chart_placeholder = st.empty()
    chart_data = []  # Para graficar correctamente

    for i, r in enumerate(trial_outcomes):
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart_data.append(mean)

        chart_df = pd.DataFrame(chart_data, columns=["media"])
        chart_placeholder.line_chart(chart_df)

        status.text(f"Lanzando moneda {i + 1} de {n}...")
        time.sleep(0.05)

    status.text("¡Lanzamiento completo!")

    # Mostrar gráfico de frecuencia (Águila / Sello)
    counts = pd.Series(trial_outcomes).value_counts().sort_index()
    counts.index = ['Sello', 'Águila']
    st.subheader("Frecuencia de resultados:")
    st.bar_chart(counts)

    return mean

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)

    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iteraciones', 'media'])
    ], axis=0)

    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

    # Mostrar resultado final con color
    color = "green" if mean > 0.5 else "red"
    st.markdown(f"<h2 style='color:{color};'>Resultado promedio: {mean:.2f}</h2>", unsafe_allow_html=True)

st.write(st.session_state['df_experiment_results'])