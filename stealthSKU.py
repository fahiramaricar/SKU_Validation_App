import streamlit as st
import pandas as pd
# Streamlit UI for File Upload
st.title("SKU Validation Tool")

main_file = st.file_uploader("Upload Main File (Excel/CSV)", type=["xlsx", "csv"])
sku_list_file = st.file_uploader("Upload SKU List File (Excel/CSV)", type=["xlsx", "csv"])

if main_file and sku_list_file:
    df_main = pd.read_excel(main_file) if main_file.name.endswith(".xlsx") else pd.read_csv(main_file)
    df_sku = pd.read_excel(sku_list_file) if sku_list_file.name.endswith(".xlsx") else pd.read_csv(sku_list_file)

    # Ensure SKU matching is case-sensitive
    df_main["Manufacturer Sku"] = df_main["Manufacturer Sku"].astype(str)
    df_sku["Sample SKU"] = df_sku["Sample SKU"].astype(str)

    # Count of distinct Sample SKUs
    distinct_sku_count = df_sku["Sample SKU"].nunique()
    st.write(f"Distinct Sample SKU count: {distinct_sku_count}")

    # Check if all Sample SKUs are in the main file
    unmatched_skus = set(df_sku["Sample SKU"]) - set(df_main["Manufacturer Sku"])
    
    if unmatched_skus:
        st.warning(f"Warning: {len(unmatched_skus)} Sample SKU(s) from SKU list are missing in the main file.")

    # Check for extra SKUs in the main file that are not in the SKU list
    extra_skus = set(df_main["Manufacturer Sku"]) - set(df_sku["Sample SKU"])
    if extra_skus:
        st.warning(f"Warning: {len(extra_skus)} Manufacturer SKU(s) in the main file are not found in the SKU list.")
