"""
Will take a selection or excel, with row index as FULL provider names, and columns as the shift name in the form F.N, F.D, or F.D-F.N and output a csv file with row of shifts on the left with each provider's shift admin shorthand name in each cell for the designated day.

Template file should be local...downloaded each time?
"""
import pandas as pd
import os
import numpy as np


def main():
    prompt = input(
        f"Copy your selection. Make sure to include row of days.  Press enter when ready. Or enter path of excel file: "
    )

    df = check_prompt(prompt)
    d_psd1 = create_dict_provshift_dates(df)
    d_psd2 = process(d_psd1)
    write_df_csv(d_psd2)

    print(f"Done, it is NOW SAVED TO YOUR CLIPBOARD.  Paste starting with 'shift'")


def check_prompt(prompt):
    if not prompt:
        print(f"Taken off Clipboard! ")
        df = read_selection()

    else:
        prompt = prompt.strip()[1:-1]
        formats = (".xls", "xlsx")
        if prompt.endswith(formats):
            df = read_excel_to_df(prompt)
        else:
            print(f"file error")
    return df


def read_selection():
    return pd.read_clipboard(skiprows=[1])


def read_excel_to_df(PATH_1):
    return pd.read_excel(PATH_1, index_col=0)


def path_to_csv_template():
    prompt = input(f"Please enter path to this month's csv template: ")
    return os.path.abspath(fr"{prompt.strip()[1:-1]}")


def get_csv_template_df():
    # read csv template data and send as df
    prompt = input(f"Please enter path to this month's csv template: ")
    PATH = os.path.abspath(fr"{prompt.strip()[1:-1]}")
    return pd.read_csv(PATH, header=9, index_col=1)


def clean_up(inp):
    # cleans up text if there's a 24 or lower case or period at the start or end
    s = inp
    if s:
        s = s.upper().strip()
        if s.endswith("."):
            s = s[:-1]

        if s.startswith("."):
            s = s[1:]

        if "24" in s or ".-" in s:
            s = "F.D-F.N"

    return s


def create_dict_provshift_dates(df):

    provider_sadmin_names = {
        "Christopher Cheng": "C. Cheng",
        "Waseya Cornell": "W. Cornell",
        "Jeffery Gardner": "J. Gardner",
        "Scott Ferguson": "S. Ferguson",
        "Caleb Anderson": "C. Anderson",
        "Peter Fuller": "P. Fuller",
        "Shilpa Gupta": "S. Gupta",
        "Michael Hixson": "M. Hixson",
        "Stephen Hunt": "S. Hunt",
        "Rocky Jedick": "R. Jedick",
        "Jason Kim": "J. Kim",
        "Angelo Kim": "A. Kim",
        "Tim Kuo": "T. Kuo",
        "Nicholas Leaver": "N. Leaver",
        "Jaclyn Matsuura": "J. Matsuura",
        "Cameron Macadams": "C. Macadams",
        "Roger Martinez": "R. Martinez",
        "Ashkan Morim": "A. Morim",
        "Quin Newby": "Q. Newby",
        "David Notley": "D. Notley",
        "Stephanos Orphanidis": "S. Orphanidis",
        "Daniel Pendleton": "D. Pendleton",
        "Kevin Slaughter": "K. Slaughter",
        "Irena Vitkovitsky": "I. Vitkovitsky",
        "Franklin Alconcel": "F. Alconcel",
        "Lian Farino": "L. Farino",
        "Nelson Huang": "N. Huang",
        "John Jobes": "J. Jobes",
        "Joseph Kim": "J.Y. Kim",
        "Jason Klein": "J. Klein",
        "Michael Koroscil": "M. Koroscil",
        "Eduardo Lacalle": "E. Lacalle",
        "Norlan Maltez": "N. Maltez",
        "Patrick Noone": "P. Noone",
        "Krystal Ribeiro": "K. Ribeiro",
        "Anne Sinnott": "A. Sinnott",
        "Michael Tang": "M. Tang",
        "Sabrina Taylor": "S. Taylor",
        "Joseph Tran": "Jo. Tran",
        "Kyle Vanstone": "K. Vanstone",
        "Harold Woo": "H. Woo",
        "Lance Allgower": "L. Allgower",
        "Samuel Bergin": "S. Bergin",
        "Vincent Boyd": "V. Boyd",
        "Jefferson Bracey": "J. Bracey",
        "Kenneth Chang": "K. Chang",
        "Elizabeth Chen": "E. Chen",
        "Todd Christensen": "T. Christensen",
        "Patrick Flaherty": "P. Flaherty",
        "Daniel Gowhari": "D. Gowhari",
        "William Halacoglu": "W. Halacoglu",
        "Brett Hansen": "B. Hansen",
        "Bryce Hoer": "B. Hoer",
        "Hayden Maag": "H. Maag",
        "Dennis Martinez": "D. Martinez",
        "Grace Sasaki": "G. Sasaki",
        "Andrew Sheep": "A. Sheep",
        "Kathryn Sulkowski": "K. Sulkowski",
        "Jesse Tran": "J. Tran",
        "Shuai Zhao": "S. Zhao",
        "Donald Bennett": "D. Bennett",
        "Adam Berkovits": "A. Berkovits",
        "Frederick Griffith": "F. Griffith",
        "Joshua Imakyure": "J. Imakyure",
        "Daniel Inglish": "D. Inglish",
        "Jason Jones": "J.P. Jones",
        "Juan Jones": "J.C. Jones",
        "Patricia Kahn": "P. Kahn",
        "Eugene Kang": "E. Kang",
        "John Kim": "J. Kim",
        "Brandi Landis": "B. Landis",
        "Joseph Lo": "J. Lo",
        "Peter Malamet": "P. Malamet",
        "Heber Phillips": "H. Phillips",
        "Raanan Pokroy": "R. Pokroy",
        "Juan Reynoso": "J. Reynoso",
        "Schon Roberts": "S. Roberts",
        "Jesse Wells": "J. Wells",
    }
    # Creates a dictionary with User and names of shift
    df = df.replace(r"^\s*$", np.nan, regex=True)
    df["provider"] = df.User
    df.provider = df["provider"].map(lambda x: provider_sadmin_names.get(x, None))
    df = df.set_index("provider")
    df = df.drop(columns="User")
    df = df.replace({np.nan: None})

    d_psd = {row[0]: row[1].tolist() for row in df.iterrows()}
    return d_psd


def process(d_psd):

    shift_names = [
        "F.D",
        "F.N",
        "B.D",
        "B.N",
        "S.D",
        "S.N",
        "C.D",
        "C.N",
        "F.24",
        "F.D-F.N",
    ]

    # modifies the list to only include shift names or None
    for k, v in d_psd.items():
        temp_v = []
        for elem in v:
            if clean_up(elem) in shift_names:
                temp_v.append(clean_up(elem))

            else:
                temp_v.append(None)
        d_psd[k] = temp_v

    return d_psd


def write_df_csv(d_psd):
    csv_code = {
        "F.D": "SRDHWF F.D",
        "F.N": "SRDHWF F.N",
        "B.D": "SRDHBD B.D",
        "B.N": "SRDHBD B.N",
        "S.D": "SRDHS S.D",
        "S.N": "SRDHS S.N",
        "C.D": "SRDHNL C.D",
        "C.N": "SRDHNL C.N",
        None: None,
    }

    df_csv = get_csv_template_df()

    # writes into df_csv
    for provider, list_shifts in d_psd.items():
        for day, p_shift in enumerate(list_shifts, start=1):
            if p_shift:

                if "-" in p_shift:
                    p_shift1, p_shift2 = tuple(p_shift.split("-"))
                    df_csv.at[csv_code[p_shift1], str(day)] = provider
                    df_csv.at[csv_code[p_shift2], str(day)] = provider

                else:
                    df_csv.at[csv_code[p_shift], str(day)] = provider

    df_csv = df_csv.drop(columns=["ID"])

    df_csv.to_clipboard()


if __name__ == "__main__":
    main()

