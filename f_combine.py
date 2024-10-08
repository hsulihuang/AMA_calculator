# Combine multiple disability ratings using the formula a + b(1-a).
# Ratings should be provided as percentages (e.g., 30 for 30%).
from decimal import Decimal, ROUND_HALF_UP

def f_combine(ratings):
    ratings = sorted(ratings, reverse=True)
    combined_rating = ratings[0]
    
    for rating in ratings[1:]:
        combined_rating = combined_rating + rating * (1 - combined_rating / 100)
        combined_rating = Decimal(combined_rating).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    
    return combined_rating

# Example usage
if __name__ == "__main__":
    # Example input
    ratings = [10, 30, 20]
    final_rating = f_combine(ratings)
    print(f"Combined Final Rating: {final_rating}%")