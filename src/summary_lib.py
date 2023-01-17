# summary_lib.py

# Module Imports
import pandas as pd

from pandas import DataFrame

"""
Filtering Functions
"""

# Filter Summary data
def filter_summary_data(df: DataFrame, filter_type: str) -> DataFrame:
    # All Data
    if filter_type.lower() == "all":
        return df[df["Type"] == "all"]
    # Resident Type Data
    elif filter_type.lower() == "resident_type":
        return df[df["Type"] == "resident_type"]
    # Building Name Data
    elif filter_type.lower() == "building_name":
        return df[df["Type"] == "building_name"]
    # Building Floor Data
    elif filter_type.lower() == "building_floor":
        return df[df["Type"] == "building_floor"]
    # Resident Length Data
    elif filter_type.lower() == "resident_length":
        return df[df["Type"] == "resident_length"]


"""
Metric Functions
"""
# All residents
def metric_residents_all(df: DataFrame) -> int:
    return int(df[(df["Description"] == "Responses") & (df["Type"] == "all")]["Number"])


# Contactable residents
def metric_residents_contactable(df: DataFrame) -> int:
    return int(
        df[(df["Description"] == "Contactable") & (df["Type"] == "all")]["Number"]
    )


# Leaseholder (%)
def metric_residents_leaseholder(df: DataFrame) -> int:
    total_all = metric_residents_all(df)
    total_leaseholder = int(
        df[(df["Description"] == "Leaseholder") & (df["Type"] == "resident_type")][
            "Number"
        ]
    )
    return int(round((total_leaseholder / total_all) * 100, 0))


# Tenant (%)
def metric_residents_tenant(df: DataFrame) -> int:
    total_all = metric_residents_all(df)
    total_tenant = int(
        df[(df["Description"] == "Tenant") & (df["Type"] == "resident_type")]["Number"]
    )
    return int(round((total_tenant / total_all) * 100, 0))
