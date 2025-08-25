import matplotlib.pyplot as plt
import seaborn as sns


def plot_subject_averages(df, return_fig=False):
    averages = df.mean(numeric_only=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=averages.index, y=averages.values, ax=ax, palette="viridis")
    ax.set_title("Subject Averages")
    ax.set_ylabel("Average Score")

    if return_fig:
        return fig
    else:
        plt.show()


def plot_distribution(df, subject, return_fig=False):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df[subject], kde=True, bins=10, ax=ax, color="skyblue")
    ax.set_title(f"Distribution of {subject}")
    ax.set_xlabel("Scores")
    ax.set_ylabel("Frequency")

    if return_fig:
        return fig
    else:
        plt.show()


def plot_grade_distribution(df, return_fig=False):
    grade_counts = df["Grade"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    grade_counts.plot(kind="bar", color="coral", ax=ax)
    ax.set_title("Grade Distribution")
    ax.set_ylabel("Number of Students")
    ax.set_xlabel("Grade")

    if return_fig:
        return fig
    else:
        plt.show()
