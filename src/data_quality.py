def apply_data_quality_rules(df):
    """
    Cleans invalid data instead of failing the pipeline.
    Returns cleaned dataframe + quality report.
    """

    report = {
        "invalid_quantity_rows": 0,
        "invalid_shipment_rows": 0,
        "rows_dropped": 0
    }

    initial_rows = len(df)

    # Rule 1: prod_qty must be > 0
    invalid_qty = df[df["prod_qty"] <= 0]
    report["invalid_quantity_rows"] = len(invalid_qty)
    df = df[df["prod_qty"] > 0]

    # Rule 2: shipped_at must be >= order_date OR NULL
    invalid_ship = df[
        (df["shipped_at"].notnull()) &
        (df["shipped_at"] < df["order_date"])
    ]
    report["invalid_shipment_rows"] = len(invalid_ship)

    df = df[
        (df["shipped_at"].isnull()) |
        (df["shipped_at"] >= df["order_date"])
    ]

    report["rows_dropped"] = initial_rows - len(df)

    return df, report
