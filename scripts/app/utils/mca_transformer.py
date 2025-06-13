import joblib
import pandas as pd


class MCATransformer:
    def __init__(self, excel_path: str, mca_path: str):
        # 🔹 Excel verisi ve MCA modeli yüklenir
        self.df = pd.read_excel(excel_path)
        self.mca = joblib.load(mca_path)

        # 🔸 Kategorik ve sayısal kolonlar
        self.categorical_cols = [
            'Sex', 'Migratory_Pain', 'Lower_Right_Abd_Pain', 'Contralateral_Rebound_Tenderness',
            'Coughing_Pain', 'Nausea', 'Loss_of_Appetite', 'Neutrophilia', 'Ketones_in_Urine',
            'RBC_in_Urine', 'WBC_in_Urine', 'Dysuria', 'Stool', 'Peritonitis', 'Psoas_Sign',
            'Ipsilateral_Rebound_Tenderness', 'Appendix_Diameter_Categorized'
        ]

        self.numerical_cols = [
            'Age', 'BMI', 'Height', 'Weight', 'Length_of_Stay', 'Body_Temperature',
            'WBC_Count', 'Neutrophil_Percentage', 'RBC_Count', 'Hemoglobin', 'RDW',
            'Thrombocyte_Count', 'CRP', 'Appendix_Diameter'
        ]

    def transform_single_input(self, input_dict: dict) -> pd.DataFrame:
        """
        Tek bir hasta girdisini alıp MCA + sayısal özniteliklere dönüştürür.
        """
        # 🔹 Dict → DataFrame
        row = pd.DataFrame([input_dict])

        # 🔹 Sayısal verileri dönüştür
        for col in self.numerical_cols:
            if col in row.columns:
                row[col] = pd.to_numeric(row[col], errors='coerce').fillna(0)

        # 🔹 Kategorik verileri temizle
        for col in self.categorical_cols:
            if col in row.columns:
                row[col] = row[col].astype(str).str.strip().str.lower()

        # 🔹 MCA dönüşümü
        mca_input = row[self.categorical_cols]
        mca_array = self.mca.transform(mca_input)
        mca_col_names = [str(i) for i in range(mca_array.shape[1])]
        mca_df = pd.DataFrame(
            mca_array, columns=mca_col_names, index=row.index)

        # 🔹 Sayısal verilerle birleştir
        numeric_df = row[self.numerical_cols].reset_index(drop=True)
        final_df = pd.concat([mca_df, numeric_df], axis=1)

        return final_df
