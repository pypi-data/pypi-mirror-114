def even(a,b):
    x = [i for i in range(a,b+1) if i % 2 == 0 and i > 0]
    print(f"{x}\nFound: {len(x)} even numbers in between {a} to {b} .")