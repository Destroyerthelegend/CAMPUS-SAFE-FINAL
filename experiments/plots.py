import matplotlib.pyplot as plt
 
def plot_priority_delay(results):
    priorities = list(results.keys())
    delays = [results[p] for p in priorities]
 
    plt.figure(figsize=(8, 5))
    plt.bar(priorities, delays)
    plt.xlabel("Priority")
    plt.ylabel("Average End-to-End Delay (ms)")
    plt.title("CAMPUS-SAFE: Delay by Priority")
    plt.tight_layout()
    plt.show()
 
if __name__ == "__main__":
    sample = {
        "LOW": 55,
        "NORMAL": 40,
        "HIGH": 25,
        "CRITICAL": 15,
    }
    plot_priority_delay(sample)
