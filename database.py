from tkinter import messagebox
import os

class DBMS:
    def __init__(self):
        self.indexes_file = "index.txt"
        self.block_files = self.load_block_files()
        self.block_data = {}
        self.comparisons = 0

    def load_block_files(self):
        if os.path.exists(self.indexes_file):
            with open(self.indexes_file, "r") as f:
                return [f"blocks/{i + 1}.txt" for i, _ in enumerate(f.readlines())]
        return []

    def get_index_file_data(self):
        try:
            with open(self.indexes_file, "r") as f:
                return f.read()
        except Exception as error:
            messagebox.showerror("Error", f"Failed to read index file: {error}")
            return ""

    def load(self, file):
        if os.path.exists(file):
            try:
                with open(file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            key, value = line.split(":", 1)
                            self.block_data[int(key)] = value
            except Exception as error:
                messagebox.showerror("Error", f"Failed to load database: {error}")
                self.block_data = {}
        else:
            self.block_data = {}

    def save(self, file):
        try:
            with open(file, "w") as f:
                for key, value in self.block_data.items():
                    f.write(f"{key}:{value}\n")
        except Exception as error:
            messagebox.showerror("Error", f"Failed to save data: {error}")

    def add_record(self, key, value):
        block_num = self.find_block(key)
        if block_num == -1:
            block_num = self.create_new_block(key)
        curr_block = self.block_files[block_num]
        self.load(curr_block)

        if key in self.block_data:
            raise ValueError("Key already exists!")
        self.block_data[key] = value
        self.sort_records()

        self.save(curr_block)
        self.block_data = {}

    def create_new_block(self, key):
        new_block_num = len(self.block_files) + 1
        new_block_name = f"blocks/{new_block_num}.txt"
        os.makedirs("blocks", exist_ok=True)
        with open(new_block_name, "w") as f:
            pass

        new_block_start = key - (key % 1000)
        with open(self.indexes_file, "a") as f:
            f.write(f"{new_block_start}:1000:{new_block_num - 1}\n")

        self.block_files.append(new_block_name)
        return new_block_num - 1

    def sort_records(self):
        self.block_data = dict(sorted(self.block_data.items()))

    def find_block(self, key):
        try:
            with open(self.indexes_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        start, num, block_num = map(int, line.split(":"))
                        if start <= key < start + num:
                            return block_num
        except Exception as e:
            messagebox.showerror("Error", f"Failed to find block: {e}")
        return -1

    def delete_record(self, key):
        block_num = self.find_block(key)
        if block_num == -1:
            raise ValueError("Error: Failed to find a valid block for the given key.")
        curr_block = self.block_files[block_num]
        self.load(curr_block)

        if key not in self.block_data:
            raise KeyError("Key not found!")
        del self.block_data[key]
        self.save(curr_block)
        self.block_data = {}

    def binary_search(self, key):
        keys = list(self.block_data.keys())
        low, high = 0, len(keys) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_key = keys[mid]
            self.comparisons += 1
            if mid_key == key:
                print('Comparisons:', self.comparisons)
                return self.block_data[mid_key]
            elif mid_key < key:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def search_record(self, key):
        block_num = self.find_block(key)
        if block_num == -1:
            raise ValueError("Error: Failed to find a valid block for the given key.")
        curr_block = self.block_files[block_num]
        self.load(curr_block)
        self.comparisons = 0
        result = self.binary_search(key)
        self.block_data = {}
        if result is not None:
            return result
        else:
            messagebox.showinfo("Search Result", f"Record with key {key} not found.")
            return None

    def edit_record(self, key, value):
        block_num = self.find_block(key)
        if block_num == -1:
            raise ValueError("Error: Failed to find a valid block for the given key.")
        curr_block = self.block_files[block_num]
        self.load(curr_block)
        if key not in self.block_data:
            raise KeyError("Key not found!")
        self.block_data[key] = value
        self.save(curr_block)
        self.block_data = {}

    def get_max_index(self):
        index_data = self.get_index_file_data()
        if not index_data.strip():
            return -1
        lines = index_data.strip().split("\n")
        max_index = -1
        for line in lines:
            start_idx, count, _ = map(int, line.split(":"))
            last_index = start_idx + count - 1
            if last_index > max_index:
                max_index = last_index
        return max_index