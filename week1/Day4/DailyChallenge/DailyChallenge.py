# Instructions: Pagination System
# 📄 What is Pagination?
# In web development, pagination helps break large lists into smaller, manageable chunks (pages), making it easier to navigate content like search results, product listings, or articles.

import math
class Pagination:

    def __init__(self, items=None, page_size=10):
        self.items = items if items is not None else []
        self.page_size = page_size
        self.current_idx = 0
        self.total_pages = math.ceil(len(self.items) / page_size)

    def get_visible_items(self):
        start = self.current_idx * self.page_size
        end = start + self.page_size
        return self.items[start:end]

    def go_to_page(self, page_num):
        idx = int(page_num) - 1
        if not (0 <= idx < self.total_pages):
            raise ValueError(f"Page {page_num} out of range (1–{self.total_pages})")
        self.current_idx = idx
        return self

    def first_page(self):
        self.current_idx = 0
        return self

    def last_page(self):
        self.current_idx = self.total_pages - 1
        return self

    def next_page(self):
        if self.current_idx < self.total_pages - 1:
            self.current_idx += 1
        return self

    def previous_page(self):
        if self.current_idx > 0:
            self.current_idx -= 1
        return self

    def __str__(self):
        return "\n".join(self.get_visible_items())


# ── Tests ──────────────────────────────────────────────────────────────────────

alphabetList = list("abcdefghijklmnopqrstuvwxyz")
p = Pagination(alphabetList, 4)

print(p.get_visible_items())
# ['a', 'b', 'c', 'd']

p.next_page()
print(p.get_visible_items())
# ['e', 'f', 'g', 'h']

p.last_page()
print(p.get_visible_items())
# ['y', 'z']

print("\n-- go_to_page errors --")
try:
    p.go_to_page(10)
except ValueError as e:
    print(f"ValueError: {e}")

try:
    p.go_to_page(0)
except ValueError as e:
    print(f"ValueError: {e}")

# Bonus: method chaining
print("\n-- method chaining --")
result = Pagination(alphabetList, 4).first_page().next_page().next_page().next_page().get_visible_items()
print(result)
# ['m', 'n', 'o', 'p']

# Bonus: __str__
print("\n-- __str__ --")
p2 = Pagination(alphabetList, 4)
print(str(p2))
# a
# b
# c
# d