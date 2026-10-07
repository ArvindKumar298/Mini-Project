import pandas as pd
import sys
import os

def load_data(filepath='students.csv'):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found!")
        sys.exit(1)
    df = pd.read_csv(filepath)
    df['Name_Clean'] = df['Name'].str.strip()
    df['First_Letter'] = df['Name_Clean'].str[0].str.upper()
    df['Words_Count'] = df['Name_Clean'].apply(lambda x: len(x.split()))
    df['Roll_Last_Digit'] = df['Roll No'].astype(str).str[-1].astype(int)
    df['Roll_Tens_Digit'] = df['Roll No'].astype(str).str[-2].astype(int)
    df['Second_Letter'] = df['Name_Clean'].apply(lambda x: x[1].upper() if len(x) > 1 else '')
    return df

def run_simulation(df):
    print("=" * 70)
    print("      SEQUENTIAL FILTERING SIMULATION (80 STUDENTS)")
    print("=" * 70)
    print("Order of questions:")
    print("  Q1. Gender (Male / Female)")
    print("  Q2. First letter of name (A / B / C / D)")
    print("  Q3. Number of words in name (1 / 2 / 3)")
    print("  Q4. Last digit of roll number (0-9)")
    print("  Q5. Previous section (CSE11 - CSE20)")
    print("=" * 70)

    found_steps = {1: [], 2: [], 3: [], 4: [], 5: [], 'ambiguous': []}
    
    for _, student in df.iterrows():
        # Q1: Gender
        q1 = df[df['Gender'] == student['Gender']]
        if len(q1) == 1:
            found_steps[1].append(student['Roll No'])
            continue

        # Q2: First Letter
        q2 = q1[q1['First_Letter'] == student['First_Letter']]
        if len(q2) == 1:
            found_steps[2].append(student['Roll No'])
            continue

        # Q3: Word Count
        q3 = q2[q2['Words_Count'] == student['Words_Count']]
        if len(q3) == 1:
            found_steps[3].append(student['Roll No'])
            continue

        # Q4: Roll Last Digit
        q4 = q3[q3['Roll_Last_Digit'] == student['Roll_Last_Digit']]
        if len(q4) == 1:
            found_steps[4].append(student['Roll No'])
            continue

        # Q5: Previous Section
        q5 = q4[q4['Previous Section'] == student['Previous Section']]
        if len(q5) == 1:
            found_steps[5].append(student['Roll No'])
        else:
            found_steps['ambiguous'].append(student['Roll No'])

    def get_names(roll_list):
        return df[df['Roll No'].isin(roll_list)]['Name_Clean'].tolist()

    print(f"\n[+] Total Students: {len(df)}")
    print(f" • Identified after Q1 (Gender):          {len(found_steps[1]):2d} students")
    print(f" • Identified after Q2 (First Letter):     {len(found_steps[2]):2d} students -> {get_names(found_steps[2])}")
    print(f" • Identified after Q3 (Word Count):       {len(found_steps[3]):2d} students -> {get_names(found_steps[3])}")
    print(f" • Identified after Q4 (Roll Last Digit):  {len(found_steps[4]):2d} students")
    print(f" • Identified after Q5 (Previous Section): {len(found_steps[5]):2d} students")
    
    total_found = sum(len(found_steps[i]) for i in range(1, 6))
    print("-" * 70)
    print(f" TOTAL IDENTIFIED BY Q5: {total_found} / {len(df)} ({total_found / len(df) * 100:.1f}%)")
    print(f" REMAINING AMBIGUOUS:    {len(found_steps['ambiguous'])} students (4 pairs of identical attributes)")
    print("-" * 70)

    # Details of ambiguous
    print("\n[!] The 4 Ambiguous Pairs that share identical answers across all 5 questions:")
    amb_df = df[df['Roll No'].isin(found_steps['ambiguous'])]
    for (gender, flet, words, last_d, sec), group in amb_df.groupby(['Gender', 'First_Letter', 'Words_Count', 'Roll_Last_Digit', 'Previous Section']):
        names = group['Name_Clean'].tolist()
        rolls = group['Roll No'].tolist()
        print(f"  • Signature: Gender={gender}, Starts With={flet}, Words={words}, Roll Ends With={last_d}, Section={sec}")
        for n, r in zip(names, rolls):
            print(f"      - {n} (Roll: {r})")
        print("    --> Tie-breaker (2nd Letter of Name):", " vs ".join([f"{n} ('{n[1]}')" for n in names]))
        print("    --> Tie-breaker (Tens Digit of Roll):", " vs ".join([f"{n} ('{str(r)[-2]}')" for n, r in zip(names, rolls)]))
        print()

def interactive_akinator(df):
    print("\n" + "=" * 60)
    print("      AKINATOR GAME: GUESS THE CSE-15 STUDENT")
    print("=" * 60)
    print("Think of any student from the CSE-15 batch (80 students).")
    print("Answer the questions below, and I will guess who it is!\n")
    
    current_candidates = df.copy()

    # Question 1: Gender
    print("Q1: Is the student Male or Female?")
    print("    [M] Male  |  [F] Female")
    while True:
        ans1 = input("Your answer (M/F): ").strip().upper()
        if ans1 in ['M', 'F']:
            break
        print("Invalid choice. Please enter M or F.")
    
    current_candidates = current_candidates[current_candidates['Gender'] == ans1]
    print(f"-> Candidates remaining: {len(current_candidates)}")
    if len(current_candidates) == 1:
        print_found(current_candidates.iloc[0], "Q1 (Gender)")
        return

    # Question 2: First Letter
    avail_letters = sorted(current_candidates['First_Letter'].unique())
    print(f"\nQ2: Which one is the first letter of their name? ({', '.join(avail_letters)})")
    while True:
        ans2 = input(f"Your answer ({'/'.join(avail_letters)}): ").strip().upper()
        if ans2 in avail_letters:
            break
        print(f"Invalid choice. Choose from: {', '.join(avail_letters)}")

    current_candidates = current_candidates[current_candidates['First_Letter'] == ans2]
    print(f"-> Candidates remaining: {len(current_candidates)}")
    if len(current_candidates) == 1:
        print_found(current_candidates.iloc[0], "Q2 (First Letter)")
        return

    # Question 3: Number of words
    avail_words = sorted(current_candidates['Words_Count'].unique())
    words_str = [str(w) for w in avail_words]
    print(f"\nQ3: How many words are there in the student's name? ({', '.join(words_str)})")
    while True:
        ans3 = input(f"Your answer ({'/'.join(words_str)}): ").strip()
        if ans3.isdigit() and int(ans3) in avail_words:
            ans3 = int(ans3)
            break
        print(f"Invalid choice. Choose from: {', '.join(words_str)}")

    current_candidates = current_candidates[current_candidates['Words_Count'] == ans3]
    print(f"-> Candidates remaining: {len(current_candidates)}")
    if len(current_candidates) == 1:
        print_found(current_candidates.iloc[0], "Q3 (Word Count)")
        return

    # Question 4: Last digit of roll number
    avail_digits = sorted(current_candidates['Roll_Last_Digit'].unique())
    digits_str = [str(d) for d in avail_digits]
    print(f"\nQ4: What is the last digit of the student's roll number? ({', '.join(digits_str)})")
    while True:
        ans4 = input(f"Your answer ({'/'.join(digits_str)}): ").strip()
        if ans4.isdigit() and int(ans4) in avail_digits:
            ans4 = int(ans4)
            break
        print(f"Invalid choice. Choose from: {', '.join(digits_str)}")

    current_candidates = current_candidates[current_candidates['Roll_Last_Digit'] == ans4]
    print(f"-> Candidates remaining: {len(current_candidates)}")
    if len(current_candidates) == 1:
        print_found(current_candidates.iloc[0], "Q4 (Last Digit of Roll No.)")
        return

    # Question 5: Previous section
    avail_sections = sorted(current_candidates['Previous Section'].unique())
    print(f"\nQ5: Which is their previous section? ({', '.join(avail_sections)})")
    while True:
        ans5 = input(f"Your answer ({'/'.join(avail_sections)}): ").strip().upper()
        if ans5 in avail_sections:
            break
        print(f"Invalid choice. Choose from: {', '.join(avail_sections)}")

    current_candidates = current_candidates[current_candidates['Previous Section'] == ans5]
    print(f"-> Candidates remaining: {len(current_candidates)}")
    
    if len(current_candidates) == 1:
        print_found(current_candidates.iloc[0], "Q5 (Previous Section)")
        return
    elif len(current_candidates) > 1:
        print("\n" + "!" * 50)
        print("AMBIGUITY DETECTED! Both students match all 5 questions:")
        for idx, row in current_candidates.iterrows():
            print(f"  - {row['Name_Clean']} (Roll: {row['Roll No']}, Mobile: {row['Student Mobile No']})")
        print("\nAsking Tie-Breaker Question (Q6: Second letter of first name):")
        avail_sec_letters = sorted(current_candidates['Second_Letter'].unique())
        while True:
            ans6 = input(f"What is the second letter of their first name? ({'/'.join(avail_sec_letters)}): ").strip().upper()
            if ans6 in avail_sec_letters:
                break
            print(f"Invalid choice. Choose from: {', '.join(avail_sec_letters)}")
        current_candidates = current_candidates[current_candidates['Second_Letter'] == ans6]
        if len(current_candidates) == 1:
            print_found(current_candidates.iloc[0], "Q6 (Tie-breaker: Second Letter)")
    else:
        print("No student matched the criteria.")

def print_found(student_row, step_name):
    print("\n" + "*" * 60)
    print(f"🎉 BINGO! Student Identified at {step_name}!")
    print(f"   Name:             {student_row['Name_Clean']}")
    print(f"   Roll No:          {student_row['Roll No']}")
    print(f"   Mobile No:        {student_row['Student Mobile No']}")
    print(f"   Current Section:  {student_row['New Section']}")
    print(f"   Previous Section: {student_row['Previous Section']}")
    print(f"   Gender:           {student_row['Gender']}")
    print("*" * 60 + "\n")

if __name__ == '__main__':
    df = load_data('students.csv')
    run_simulation(df)
    if len(sys.argv) > 1 and sys.argv[1] == '--play':
        interactive_akinator(df)
