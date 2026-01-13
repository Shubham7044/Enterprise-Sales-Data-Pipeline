import time
from extract import extract_new_orders
from data_quality import apply_data_quality_rules
from transform import transform_orders
from load import load_to_sqlite
from metadata import get_last_processed_date, log_pipeline_run

DATA_PATH = "data/raw/E-Commerce DataSet.csv"

def run_pipeline():
    start = time.time()

    print("========================================")
    print(" ORDER FULFILLMENT DATA PIPELINE START ")
    print("========================================")

    last_date = get_last_processed_date()
    df = extract_new_orders(DATA_PATH, last_date)

    df, dq_report = apply_data_quality_rules(df)

    print("📊 Data Quality Summary:")
    for k, v in dq_report.items():
        print(f"  - {k}: {v}")

    if df.empty:
        print("⚠ No valid new records to process")
        log_pipeline_run(0, "SUCCESS", last_date)
        return

    analytics_df = transform_orders(df)
    load_to_sqlite(analytics_df, "daily_fulfillment_metrics")

    new_last_date = df["order_date"].max().date().isoformat()
    log_pipeline_run(len(df), "SUCCESS", new_last_date)

    with open("outputs/pipeline_logs.txt", "a") as f:
        f.write(
            f"\nRun Time: {time.ctime()}\n"
            f"Rows Processed: {len(df)}\n"
            f"Data Quality: {dq_report}\n"
        )

    print(f"⏱ Pipeline completed in {time.time() - start:.2f} seconds")
    print("PIPELINE EXECUTED SUCCESSFULLY ✅")

if __name__ == "__main__":
    run_pipeline()
