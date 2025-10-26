import pandas as pd
import pathlib

def main():
    run_program = True

    while run_program:
        # load path
        path = input("Path: ").strip()
        df = load_data(path)
        
        if df is None:
            continue

        # select cleanup option
        print("\nWhat type of cleanup would you like?")
        print("1. Missing values")
        print("2. Fix/drop wrong data types")
        print("3. Duplicates")

        cleanup_choice = input("Input: ").strip()
        if not cleanup_choice.isnumeric():
            print("Error: Please enter a valid cleanup option.")
            continue
        cleanup_choice = int(cleanup_choice)
        if cleanup_choice not in [1, 2, 3]:
            print("Error: Please enter a valid cleanup option.")
            continue

        # cleanup dataframe
        select_option(cleanup_choice, df)
        print("\nDone!")


        # select export option
        print("\nCleanup done! How would you like to export?")
        print("1. csv")
        print("2. xlsx")
        print("3. json")
        print("4. html")

        export_choice = input("Input: ").strip()
        if not export_choice.isnumeric():
            print("Error: Please enter a valid export option.")
            continue
        export_choice = int(export_choice)

        # export dataframe
        df_export(df, export_choice)
        print("\n\n")

        loop_again = input("Would you like to clean again? [y/N]").lower().strip()
        if loop_again == 'n':
            run_program = False


def load_data(file_path):
    path = pathlib.Path(file_path)

    if not path.exists():
        print("Error: file not found.")
        return None

    sfx = path.suffix.lower()
    if sfx == ".csv":
        df = pd.read_csv(path)
    elif sfx in [".xls", ".xlsx"]:
        df = pd.read_excel(path)
    elif sfx == ".json":
        df = pd.read_json(path)
    else:
        print(f"Unsupported file type: {sfx}")
        return None

    print("Loaded " + str(len(df)) + " rows and " + str(len(df.columns)) + " columns.")

    return df


def missing_values(df):
    initial = len(df)
    print("\nDropping missing values...")

    df.dropna(inplace=True)
    print("\nDropped " + str(initial - len(df)) + " missing rows!")


def wrong_data_type(df):
    print("\nEliminating values with wrong data types...")

    for col in df.columns:
        # skip if column has id/code/number
        if any(x in col.lower() for x in ["id", "code", "number"]):
            continue

        # convert non numeric to NaN
        numeric = pd.to_numeric(df[col], errors='coerce')
        if numeric.notna().sum() > 0:
            df[col] = numeric
            continue

        # convert non datetime to NaN
        datetime = pd.to_datetime(df[col], errors='coerce')
        if datetime.notna().sum() > 0:
            df[col] = datetime
            continue

    # drop rows with NaN values
    df.dropna(inplace=True)


def duplicate_values(df):
    initial = len(df)
    print("\nDropping duplicate values...")

    df.drop_duplicates(inplace=True)
    print("\nDropped " + str(initial - len(df)) + " duplicate rows!")


def select_option(selected_option, df):
    if selected_option == 1:
        missing_values(df)
    elif selected_option == 2:
        wrong_data_type(df)
    elif selected_option == 3:
        duplicate_values(df)

    
def df_export(df, export_type):
    if export_type == 1:
        df.to_csv("pycliner_output.csv", index=False)
    elif export_type == 2:
        df.to_excel("pycliner_output.xlsx", index=False)
    elif export_type == 3:
        df.to_json("pycliner_output.json")
    elif export_type == 4:
        df.to_html("pycliner_output.html", index=False)


if __name__ == '__main__':
    main()
