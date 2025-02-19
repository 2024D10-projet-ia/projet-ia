import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import tree
import plotly.express as px
import matplotlib.pyplot as plt
import math
import utils.training as train

def set_new_params(model):
    models = train.get_models()
    if isinstance(model, LogisticRegression):
        new_c = float(st.session_state.get('C', model.C))
        new_solver = st.session_state.get('solver', model.solver)
        
        new_model = LogisticRegression(
            C=new_c,
            solver=new_solver,
            max_iter=1000
        )
        
        models["Logistic Regression"] = new_model
    
    elif isinstance(model, tree.DecisionTreeClassifier):
        new_p_max = int(st.session_state.get('p_max', model.max_depth))
        new_f_max = int(st.session_state.get('f_max', model.max_features))
        
        new_model = tree.DecisionTreeClassifier(
            max_depth=new_p_max,
            max_features=new_f_max,
        )
        
        models["Decision Tree"] = new_model

    elif isinstance(model, RandomForestClassifier):
        new_n_trees = int(st.session_state.get('n_trees', model.n_estimators))
        new_max_depth = int(st.session_state.get('rf_max_depth', model.max_depth))
        
        new_model = RandomForestClassifier(
            n_estimators=new_n_trees,
            max_depth=new_max_depth,
        )
        
        models["Forest"] = new_model
    
    train.run_model(new_model)


@st.dialog(f"Gérer les paramètres du modèle")
def open_modale(smn:str):
    models = train.get_models()
    model = models[smn]

    if isinstance(model, LogisticRegression):
        st.text_input("C", value=model.C, key="C")
        st.selectbox("Solver", 
        ["lbfgs", "liblinear", "newton-cg", "newton-cholesky", "sag", "saga"],
            key="solver"
        )
        st.button("Changer", on_click=lambda : set_new_params(model))

    elif isinstance(model, tree.DecisionTreeClassifier):
        st.number_input("Profondeur Max", value=model.max_depth, key="p_max")
        st.number_input("Max Features", value=model.max_features, key="f_max")
        st.button("Changer", on_click=lambda : set_new_params(model))

    elif isinstance(model, RandomForestClassifier):
        st.number_input("Nombre d'arbres", value=model.n_estimators, key="n_trees")
        st.number_input("Profondeur Max", value=model.max_depth, key="rf_max_depth")
        st.button("Changer", on_click=lambda : set_new_params(model))


def main():
    models = train.get_models()
    st.title("🍷 Entrainement des modèles de classification du vin")
    
    st.markdown("""
    Cette page a pour but de vous permettre de choisir un modèle pour l'entrainer à prédire le type du vin en fonction de ses caractéristiques.

    Vous pouvez choisir différents modèles dans la barre de sélection à gauche
    """)
    
    # Sidebar
    st.sidebar.header("Sélection des modèles")
    selected_model_name = st.sidebar.selectbox(
        "Choisissez un modèle",
        list(models.keys())
    )
    st.sidebar.button("Personnaliser", on_click=lambda : open_modale(selected_model_name))
    
    model = models[selected_model_name]
    train.run_model(model)


main()