# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="In Silico De Novo Molecule Design", layout="wide")

st.title("🧬 IN SILICO DE NOVO MOLECULE DESIGN")
st.markdown("---")

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def demo_dataframe(n: int = 10) -> pd.DataFrame:
    return pd.DataFrame({
        "Molecule ID": [f"Ligand-{str(i).zfill(3)}" for i in range(1, n + 1)],
        "SMILES": [
            "C1=CC=C(C=C1)C(=O)O",
            "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
            "C1=CC=C2C(=C1)C=CC=N2",
            "CC1=CC=C(C=C1)NC(=O)C",
            "C1=CC(=CC=C1O)C(=O)O",
            "CC(C)NCC(C1=CC(=C(C=C1)O)CO)O",
            "C1=CC=C(C=C1)CCNC(=O)C",
            "CC(C)(C)NCC(C1=CC=CC=C1)O",
            "C1=CC=C(C=C1)C=CC(=O)O",
            "CC1=CC=C(C=C1)S(=O)(=O)N",
        ],
        "MW (Da)": [320, 298, 256, 310, 275, 342, 288, 305, 294, 318],
        "Binding Affinity (kcal/mol)": [-9.2, -8.8, -8.5, -8.3, -8.1, -7.9, -7.7, -7.5, -7.3, -7.1],
        "Docking Score": [8.9, 8.5, 8.2, 8.0, 7.8, 7.6, 7.4, 7.2, 7.0, 6.8],
        "Druggability Score": [0.82, 0.78, 0.75, 0.71, 0.68, 0.65, 0.62, 0.59, 0.56, 0.53],
    })


def safe_bar_chart(x, y, title, x_title, y_title, height=400, texts=None):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=x,
            y=y,
            text=texts if texts is not None else y,
            textposition="outside",
        )
    )
    fig.update_layout(title=title, xaxis_title=x_title, yaxis_title=y_title, height=height)
    return fig


# ------------------------------------------------------------
# Sidebar - Inputs
# ------------------------------------------------------------
with st.sidebar:
    st.header("📋 PROJECT INFORMATION")

    proje_adi = st.text_input("Project Name", "Project_001")

    st.subheader("🎯 Target Protein")
    pdb_file = st.file_uploader("Upload PDB File", type=["pdb"])

    st.subheader("🔍 Binding Site")
    binding_method = st.selectbox(
        "Binding Site Selection Method",
        [
            "Automatic detection (pocket finder)",
            "Grid box coordinates",
            "Reference ligand",
            "Amino acid list",
        ],
    )

    if binding_method == "Grid box coordinates":
        col1, col2 = st.columns(2)
        with col1:
            center_x = st.number_input("Center X", value=0.0)
            center_y = st.number_input("Center Y", value=0.0)
            center_z = st.number_input("Center Z", value=0.0)
        with col2:
            size_x = st.number_input("Size X", value=20.0)
            size_y = st.number_input("Size Y", value=20.0)
            size_z = st.number_input("Size Z", value=20.0)

    blind_docking = st.checkbox("Blind Docking (Scan whole protein)")

    st.subheader("🔬 Target Conformation")
    konformasyon = st.selectbox(
        "Conformation Type",
        ["Active (agonist-like)", "Inactive (antagonist-like)", "Unknown", "Allosteric Modulator"],
    )

    istenen_etki = st.radio(
        "Desired Pharmacological Effect",
        ["Agonist", "Antagonist", "Modulator", "Allosteric modulator", "Unknown"],
    )

    st.subheader("👥 Target Population")
    populasyon = st.selectbox(
        "Age Group for Drug Use",
        ["0-2", "2-18", "18-45", "45-65", "65-85", "85+", "Unknown"],
    )

    st.subheader("💉 Administration Route")
    uygulama = st.selectbox(
        "Drug Administration Route",
        ["Oral", "Intravenous", "Intramuscular", "Inhalation", "Dermal", "Subcutaneous", "Other"],
    )

    st.subheader("⚙️ Method Selection")
    yontem = st.selectbox(
        "De Novo Design Method",
        [
            "Fragment-based",
            "SMILES-based generative model (RNN/Transformer)",
            "GA (genetic algorithm)",
            "Ligand growing",
            "Reaction-based enumeration",
        ],
    )

    seed_file = st.file_uploader("Initial Molecule (optional)", type=["sdf", "mol2"])

    molekul_sayisi = st.select_slider(
        "Number of Molecules to Generate",
        options=["1-5", "5-10", "10-50", "50-100"],
    )

    st.markdown("---")
    run_button = st.button("🚀 START ANALYSIS", type="primary", use_container_width=True)

# ------------------------------------------------------------
# Main Content (with error handling)
# ------------------------------------------------------------
try:
    np.random.seed(42)
    demo_df = demo_dataframe(10)

    if run_button and not pdb_file:
        st.warning("Please upload a PDB file first.")

    if pdb_file and run_button:
        st.success(f"✅ {getattr(pdb_file, 'name', 'PDB')} file successfully uploaded!")

        with st.spinner("Running analysis... Please wait..."):
            import time
            time.sleep(2)

        st.success("✨ Analysis complete!")

        df = demo_dataframe(10)

        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 General Results",
            "🔬 Docking Results",
            "💊 Druggability Score",
            "🎨 3D Visualization",
        ])

        # ---------------- Tab 1 ----------------
        with tab1:
            st.header("📊 GENERAL RESULTS")

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Generated Molecules", "47")
            with c2:
                st.metric("Successful Docking", "42")
            with c3:
                st.metric("Average Binding Affinity", "-8.3 kcal/mol")
            with c4:
                st.metric("Best Druggability Score", "0.82")

            st.subheader("Top 10 Molecule Candidates")
            st.dataframe(df, use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                fig1 = safe_bar_chart(
                    x=df["Molecule ID"],
                    y=df["Binding Affinity (kcal/mol)"],
                    title="Binding Affinity Comparison",
                    x_title="Molecule ID",
                    y_title="Binding Affinity (kcal/mol)",
                    height=400,
                )
                st.plotly_chart(fig1, use_container_width=True)

            with c2:
                fig2 = safe_bar_chart(
                    x=df["Molecule ID"],
                    y=df["Druggability Score"],
                    title="Druggability Score Comparison",
                    x_title="Molecule ID",
                    y_title="Druggability Score",
                    height=400,
                )
                st.plotly_chart(fig2, use_container_width=True)

        # ---------------- Tab 2 ----------------
        with tab2:
            st.header("🔬 DOCKING RESULTS")

            selected_ligand = st.selectbox("Select Molecule", df["Molecule ID"].tolist())
            idx = df.index[df["Molecule ID"] == selected_ligand][0]

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Binding Affinity", f"{df.iloc[idx]['Binding Affinity (kcal/mol)']} kcal/mol")
            with c2:
                st.metric("Docking Score", f"{df.iloc[idx]['Docking Score']}")
            with c3:
                st.metric("Molecular Weight", f"{df.iloc[idx]['MW (Da)']} Da")

            st.subheader("🔗 Ligand-Amino Acid Interactions")
            interactions_df = pd.DataFrame({
                "Amino Acid": ["ASP102", "HIS57", "SER195", "GLY216", "TRP215", "VAL213"],
                "Interaction Type": [
                    "Hydrogen Bond",
                    "π-π Stacking",
                    "Hydrogen Bond",
                    "Hydrophobic",
                    "π-π Stacking",
                    "Hydrophobic",
                ],
                "Distance (Å)": [2.8, 3.5, 2.9, 4.2, 3.8, 4.1],
                "Energy Contribution (kcal/mol)": [-2.5, -1.8, -2.3, -1.2, -1.5, -1.0],
            })
            st.dataframe(interactions_df, use_container_width=True)

            st.subheader("📌 Binding Site Information")
            st.info(
                """
                **Active Site Amino Acids:** ASP102, HIS57, SER195, GLY216, TRP215, VAL213, ARG204

                **Binding Coordinates:**
                - X: 15.3 Å
                - Y: 22.7 Å  
                - Z: 8.9 Å

                **Pocket Volume:** 458.3 Ų
                """
            )

            st.subheader("📊 Conformational Clustering Analysis")
            cluster_df = pd.DataFrame(
                {
                    "Cluster": ["Cluster 1", "Cluster 2", "Cluster 3"],
                    "Pose Count": [15, 8, 4],
                    "Average Energy (kcal/mol)": [-9.2, -8.5, -7.8],
                    "RMSD (Å)": [1.2, 2.1, 3.5],
                }
            )
            st.dataframe(cluster_df, use_container_width=True)

        # ---------------- Tab 3 ----------------
        with tab3:
            st.header("💊 DRUGGABILITY SCORE DETAILS")

            selected_ligand_drug = st.selectbox(
                "Select Molecule ", df["Molecule ID"].tolist(), key="drug_select"
            )
            idx = df.index[df["Molecule ID"] == selected_ligand_drug][0]

            score = float(df.iloc[idx]["Druggability Score"])
            if score >= 0.6:
                color = "green"
                status = "✅ HIGH DRUGGABILITY"
            elif score >= 0.3:
                color = "orange"
                status = "⚠️ MEDIUM DRUGGABILITY"
            else:
                color = "red"
                status = "❌ LOW DRUGGABILITY"

            st.markdown(f"## <span style='color:{color}'>{score:.2f}</span>", unsafe_allow_html=True)
            st.markdown(f"### {status}")

            st.info(
                """
                **Description:** Calculated considering the molecule’s binding potential, pharmacokinetic properties, and toxicity profile.
                """
            )

            st.subheader("🧪 Molecular Properties")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("MW", f"{df.iloc[idx]['MW (Da)']} Da", help="Molecular Weight (ideal: 150-500 Da)")
            with c2:
                st.metric("LogP", "3.1", help="Lipophilicity (optimum: 0-5)")
            with c3:
                st.metric("H-Bond Donor", "2", help="Number of hydrogen bond donors")
            with c4:
                st.metric("H-Bond Acceptor", "5", help="Number of hydrogen bond acceptors")

            c5, c6, c7 = st.columns(3)
            with c5:
                st.metric("Rotatable Bonds", "4", help="Number of rotatable bonds (ideal: ≤10)")
            with c6:
                st.metric("PSA", "75 Ų", help="Polar Surface Area")
            with c7:
                st.metric("SMILES", df.iloc[idx]["SMILES"][:20] + "...", help="Chemical structure code")

            st.subheader("📊 Property Distribution (Radar Chart)")
            categories = ["MW", "LogP", "H-Bond", "PSA", "Rotatable Bonds", "ADME Compliance"]
            values = [0.85, 0.75, 0.90, 0.80, 0.88, 0.82]
            fig_radar = go.Figure()
            fig_radar.add_trace(
                go.Scatterpolar(r=values, theta=categories, fill="toself", name=selected_ligand_drug)
            )
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, height=500
            )
            st.plotly_chart(fig_radar, use_container_width=True)

            st.subheader("📈 Molecule Comparison")
            fig_compare = go.Figure()
            top5 = df.head(5)
            fig_compare.add_trace(
                go.Bar(x=top5["Molecule ID"], y=top5["Druggability Score"], 
                       text=top5["Druggability Score"], textposition="outside")
            )
            fig_compare.update_layout(
                title="Top 5 Molecules Druggability Score Comparison",
                xaxis_title="Molecule ID",
                yaxis_title="Druggability Score",
                height=400,
            )
            st.plotly_chart(fig_compare, use_container_width=True)

            st.subheader("💊 ADME-Tox Profile")
            adme_df = pd.DataFrame(
                {
                    "Property": ["Absorption", "Distribution", "Metabolism", "Elimination", "Toxicity"],
                    "Evaluation": ["Good", "Moderate", "Good", "Good", "Low Risk"],
                    "Score": [0.85, 0.65, 0.80, 0.78, 0.90],
                }
            )
            st.dataframe(adme_df, use_container_width=True)

            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                rapor = "Report: Sample analysis results\nProject: " + proje_adi
                st.download_button("📄 Download Report (TXT)", rapor, file_name="report.txt")
            with c2:
                st.download_button(
                    "📊 Download CSV", df.to_csv(index=False), file_name="results.csv", mime="text/csv"
                )

        # ---------------- Tab 4 ----------------
        with tab4:
            st.header("🎨 3D VISUALIZATION")
            st.info("🔬 3D visualization of the protein-ligand complex (sample simulation)")
            selected_ligand_3d = st.selectbox(
                "Select Molecule to Visualize", df["Molecule ID"].tolist(), key="3d_select"
            )

            fig_3d = go.Figure(
                data=[
                    go.Scatter3d(
                        x=np.random.randn(100),
                        y=np.random.randn(100),
                        z=np.random.randn(100),
                        mode="markers",
                        marker=dict(size=5, color=np.random.randn(100), showscale=True),
                    )
                ]
            )
            fig_3d.update_layout(
                title="Protein-Ligand Complex (Simulation)",
                scene=dict(xaxis_title="X (Å)", yaxis_title="Y (Å)", zaxis_title="Z (Å)"),
                height=600,
            )
            st.plotly_chart(fig_3d, use_container_width=True)

            st.markdown("---")
            st.download_button("💾 Download PDB File (Sample)", "Sample PDB content", file_name="complex.pdb")

    else:
        st.info("👈 Upload a PDB file from the sidebar and press **START ANALYSIS**. Below is a sample view.")

        st.subheader("Top 10 Molecule Candidates (Sample)")
        st.dataframe(demo_df, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(
                safe_bar_chart(
                    x=demo_df["Molecule ID"],
                    y=demo_df["Binding Affinity (kcal/mol)"],
                    title="Binding Affinity Comparison (Sample)",
                    x_title="Molecule ID",
                    y_title="Binding Affinity (kcal/mol)",
                ),
                use_container_width=True,
            )
        with c2:
            st.plotly_chart(
                safe_bar_chart(
                    x=demo_df["Molecule ID"],
                    y=demo_df["Druggability Score"],
                    title="Druggability Score Comparison (Sample)",
                    x_title="Molecule ID",
                    y_title="Druggability Score",
                ),
                use_container_width=True,
            )

    st.markdown("---")
    st.markdown(
        "💡 **Note:** This interface works with sample outputs. Real calculations will be provided via backend integration."
    )

except Exception as e:
    st.error("An error occurred while running the app. Details below:")
    st.exception(e)
