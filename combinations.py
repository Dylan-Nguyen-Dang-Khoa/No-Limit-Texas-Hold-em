def combinations(n, k):
    # Initial combination: first k indices
    combo = list(range(k))
    while True:
        yield combo.copy()
        # Find the rightmost index that can be incremented
        for i in reversed(range(k)):
            if combo[i] != i + n - k:
                break
        else:
            # No more combinations possible
            return
        # Increment this index
        combo[i] += 1
        # Reset all following indices
        for j in range(i + 1, k):
            combo[j] = combo[j - 1] + 1

# Example usage:
for c in combinations(7, 5):
    print(c)
