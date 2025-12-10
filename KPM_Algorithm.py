import time
import random
import string
import matplotlib.pyplot as plt


def compute_lps(pattern):
    """
    Compute the Longest Proper Prefix which is also Suffix array

    Args:
        pattern: The pattern string

    Returns:
        lps: Array of length equal to pattern length
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # length of previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text, pattern):
    """
    Knuth-Morris-Pratt pattern matching algorithm

    Args:
        text: The text string to search in
        pattern: The pattern string to search for

    Returns:
        indices: List of starting indices where pattern is found
    """
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return []

    # Compute LPS array
    lps = compute_lps(pattern)

    indices = []
    i = 0  # index for text
    j = 0  # index for pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            # Pattern found at index i - j
            indices.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return indices


def generate_test_data(n, pattern_length=100):
    """Generate random text and pattern for testing"""
    text = ''.join(random.choices(string.ascii_uppercase, k=n))
    pattern = ''.join(random.choices(string.ascii_uppercase, k=pattern_length))
    return text, pattern


def test_kmp(n):
    """Test KMP algorithm with dataset of size n"""
    text, pattern = generate_test_data(n)

    start_time = time.time()
    indices = kmp_search(text, pattern)
    end_time = time.time()

    execution_time = (end_time - start_time) * 1000  # Convert to ms

    return execution_time, len(indices)


# Main execution
if __name__ == "__main__":
    # Testing with different dataset sizes
    test_sizes = [1000, 10000, 100000, 1000000, 10000000, 100000000]

    print("KMP Algorithm Performance Testing")
    print("=" * 60)
    print(f"{'Dataset Size (n)':<20} {'Execution Time (ms)':<25} {'Matches Found'}")
    print("=" * 60)

    # Store results for plotting
    sizes = []
    times = []

    for n in test_sizes:
        exec_time, matches = test_kmp(n)
        print(f"{n:<20} {exec_time:<25.4f} {matches}")
        sizes.append(n)
        times.append(exec_time)

    print("=" * 60)

    # Plotting the results
    plt.figure(figsize=(12, 7))

    # Main plot
    plt.subplot(1, 2, 1)
    plt.plot(sizes, times, marker='o', linewidth=2, markersize=8, color='#2563eb')
    plt.xlabel('Input Size (n)', fontsize=12, fontweight='bold')
    plt.ylabel('Execution Time (ms)', fontsize=12, fontweight='bold')
    plt.title('KMP Algorithm Performance: Time vs Input Size', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.ticklabel_format(style='scientific', axis='x', scilimits=(0, 0))

    # Log-log plot to verify linear complexity
    plt.subplot(1, 2, 2)
    plt.loglog(sizes, times, marker='s', linewidth=2, markersize=8, color='#059669')
    plt.xlabel('Input Size (n) - Log Scale', fontsize=12, fontweight='bold')
    plt.ylabel('Execution Time (ms) - Log Scale', fontsize=12, fontweight='bold')
    plt.title('KMP Performance: Log-Log Scale\n(Linear slope confirms O(n) complexity)',
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('kmp_performance_graph.png', dpi=300, bbox_inches='tight')
    print("\nGraph saved as 'kmp_performance_graph.png'")
    plt.show()