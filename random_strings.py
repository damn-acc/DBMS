import string
import random

def generate_random_text(length=30):
    words = random.choices(string.ascii_lowercase + ' ', k=length)
    return ''.join(words)


output_lines = [f"{i}:{generate_random_text()}" for i in range(7000, 8000)]

file_path = "blocks/8.txt"
with open(file_path, "w", encoding="utf-8") as file:
    file.write("\n".join(output_lines))

print(f"Файл згенеровано та збережено за адресою: {file_path}")
