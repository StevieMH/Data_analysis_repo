
import pandas as pd
import os


def calculate_demographic_data(print_data=True):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'adult.data.csv')

    # Read data from file
    df = pd.read_csv(csv_path)

    # How many of each race are represented in this dataset?
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(
        (df['education'] == 'Bachelors').mean() * 100, 1)

    # With and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education_df = df[
        (df['education'] == 'Bachelors') |
        (df['education'] == 'Masters') |
        (df['education'] == 'Doctorate')
    ]
    lower_education_df = df[~(
        (df['education'] == 'Bachelors') |
        (df['education'] == 'Masters') |
        (df['education'] == 'Doctorate')
    )]

    # Salaries >50K
    higher_education_50k = higher_education_df[higher_education_df['salary']
                                               == '>50K'].shape[0]
    lower_education_50k = lower_education_df[lower_education_df['salary']
                                             == '>50K'].shape[0]

    # Percentages with salary >50K
    higher_education_rich = round(
        (higher_education_50k / higher_education_df.shape[0]) * 100, 1)
    lower_education_rich = round(
        (lower_education_50k / lower_education_df.shape[0]) * 100, 1)

    # Minimum number of hours a person works per week
    min_work_hours = df['hours-per-week'].min()

    # Percentage of people working minimum hours who earn >50K
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = round(
        (num_min_workers[num_min_workers['salary'] ==
         '>50K'].shape[0] / num_min_workers.shape[0]) * 100, 1
    )

    # Country with highest percentage of >50K earners
    # Get the percentage of high earners in each country
    country_totals = df['native-country'].value_counts()
    country_high_earners = df[df['salary'] ==
                              '>50K']['native-country'].value_counts()

    # Calculate percentage
    country_percentages = (country_high_earners / country_totals) * 100

    # Get the country with the highest percentage
    highest_earning_country = country_percentages.idxmax()
    highest_earning_country_percentage = round(country_percentages.max(), 1)

    # Most popular occupation for high earners in India
    top_IN_occupation = df[(df['salary'] == '>50K') & (
        df['native-country'] == 'India')]['occupation'].value_counts().index[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(
            f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(
            f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(
            f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(
            f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
