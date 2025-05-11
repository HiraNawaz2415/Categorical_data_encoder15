import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder
import io

# Custom CSS styling
def local_css():
    st.markdown("""
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #F0F4F8;
                color: #333333;
            }
            .stButton>button {
                background-color: #0066cc;
                color: white;
                border-radius: 12px;
                padding: 12px 24px;
                font-weight: bold;
                border: none;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #004d99;
                box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.2);
            }
            .stSelectbox, .stMultiselect {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 10px;
                box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
            }
            .stTextInput input {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 10px;
                box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
            }
            .stTextInput>div>label {
                font-weight: bold;
            }
            .main {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
                margin-top: 30px;
            }
            .stDataFrame {
                padding: 20px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #0066cc;
                font-size: 2.5rem;
                text-align: center;
            }
            h2 {
                color: #333333;
            }
            .stFileUploader {
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
                padding: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

local_css()

# App title
st.title("🔤 Categorical Data Encoder App")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Original Data")
    
    # Show the entire dataset
    st.dataframe(df)

    # Find categorical columns
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    if not cat_cols:
        st.warning("No categorical columns found in the dataset.")
    else:
        st.success(f"Automatically found categorical columns: {cat_cols}")
        
        # User selects columns to encode
        selected_columns = st.multiselect(
            "Select categorical columns to encode",
            cat_cols,
            default=cat_cols
        )

        # User selects encoding type
        encoding_type = st.selectbox(
            "Select encoding type",
            options=["One-Hot Encoding", "Label Encoding", "Ordinal Encoding"]
        )

        if selected_columns:
            if encoding_type == "One-Hot Encoding":
                # OneHotEncoding
                encoder = OneHotEncoder(drop='first', sparse_output=False)
                try:
                    encoded_array = encoder.fit_transform(df[selected_columns])
                    encoded_df = pd.DataFrame(encoded_array, columns=encoder.get_feature_names_out(selected_columns))

                    # Combine with numerical columns
                    num_df = df.drop(columns=selected_columns).reset_index(drop=True)
                    final_df = pd.concat([num_df, encoded_df], axis=1)

                    # Show encoded data
                    st.subheader("✅ Encoded Data")
                    st.dataframe(final_df)

                    # Prepare CSV download
                    csv = final_df.to_csv(index=False)
                    st.download_button(
                        label="Download Encoded Data as CSV",
                        data=csv,
                        file_name="encoded_data.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Encoding failed: {e}")

            elif encoding_type == "Label Encoding":
                # Label Encoding
                le = LabelEncoder()
                try:
                    for col in selected_columns:
                        df[col] = le.fit_transform(df[col])
                    st.subheader("✅ Label Encoded Data")
                    st.dataframe(df)

                    # Prepare CSV download
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download Encoded Data as CSV",
                        data=csv,
                        file_name="label_encoded_data.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Encoding failed: {e}")

            elif encoding_type == "Ordinal Encoding":
                # Ordinal Encoding
                st.subheader("⚙️ Ordinal Encoding")
                
                # User selects ordinal values (you can customize this further based on the data)
                ord_values = st.text_input("Enter ordinal values in order (comma-separated)", value="Low,Medium,High")
                
                if ord_values:
                    ord_values = ord_values.split(',')
                    ordinal_encoder = OrdinalEncoder(categories=[ord_values])

                    try:
                        # Apply Ordinal Encoding to selected columns
                        for col in selected_columns:
                            df[col] = ordinal_encoder.fit_transform(df[[col]])

                        st.subheader("✅ Ordinal Encoded Data")
                        st.dataframe(df)

                        # Prepare CSV download
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download Encoded Data as CSV",
                            data=csv,
                            file_name="ordinal_encoded_data.csv",
                            mime="text/csv"
                        )
                    except Exception as e:
                        st.error(f"Encoding failed: {e}")
        else:
            st.info("Please select columns to encode.")
